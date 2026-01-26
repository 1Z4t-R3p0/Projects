import os
import secrets
from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app
from flask_login import login_required, current_user
from flask_mail import Message
from models import db, Issue, mail
from werkzeug.utils import secure_filename

citizen_bp = Blueprint('citizen', __name__)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    
    s3_bucket = current_app.config.get('S3_BUCKET')
    if s3_bucket:
        try:
            import boto3
            s3 = boto3.client('s3', region_name=current_app.config.get('AWS_REGION', 'ap-south-1'))
            s3.upload_fileobj(
                form_picture,
                s3_bucket,
                picture_fn,
                ExtraArgs={
                    'ContentType': form_picture.content_type,
                    'ACL': 'public-read'
                }
            )
            return f"https://{s3_bucket}.s3.{current_app.config.get('AWS_REGION', 'ap-south-1')}.amazonaws.com/{picture_fn}", picture_fn
        except Exception as e:
            print(f"S3 Upload failed: {e}")
            # Fallback to local if S3 fails
            pass

    # Local Fallback
    upload_path = os.path.join(current_app.root_path, 'static/uploads')
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
        
    picture_path = os.path.join(upload_path, picture_fn)
    form_picture.save(picture_path)
    return picture_fn, picture_fn

def analyze_image(bucket, key):
    try:
        import boto3
        rekognition = boto3.client('rekognition', region_name=current_app.config.get('AWS_REGION', 'ap-south-1'))
        response = rekognition.detect_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': key}},
            MaxLabels=10,
            MinConfidence=75
        )
        
        labels = [label['Name'].lower() for label in response['Labels']]
        print(f"AI Labels detected: {labels}")
        
        # Define high-risk/dangerous keywords for AI detection
        critical_labels = ['flood', 'fire', 'accident', 'crash', 'natural disaster', 'collapsed building', 'emergency']
        high_labels = ['pothole', 'broken', 'damage', 'pipeline', 'waste', 'pollution']
        
        if any(label in labels for label in critical_labels):
            return 'Critical'
        if any(label in labels for label in high_labels):
            return 'High'
            
        return None # No specific AI-detected priority
    except Exception as e:
        print(f"AI Awareness Failed: {e}")
        return None

@citizen_bp.route('/report', methods=['GET', 'POST'])
@login_required
def report_issue():
    if current_user.role == 'admin':
         flash('Admins cannot report issues.', 'warning')
         return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        title_select = request.form.get('title_select')
        manual_title = request.form.get('manual_title')
        location = request.form.get('location')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        maps_link = request.form.get('maps_link')
        description = request.form.get('description')
        image = request.files.get('image')
        
        title = manual_title if title_select == 'Other' else title_select
        
        if not title or not location or not description:
            flash('Title, Location, and Description are required', 'error')
            return redirect(url_for('citizen.report_issue'))
            
        image_file = None
        image_key = None
        if image and image.filename != '':
             image_file, image_key = save_picture(image)
             
        priority = Issue.calculate_priority(description)
        
        # AI Boost: If priority isn't Critical, let the AI check the image
        if priority != 'Critical' and image_key and current_app.config.get('S3_BUCKET'):
            ai_priority = analyze_image(current_app.config['S3_BUCKET'], image_key)
            if ai_priority:
                print(f"AI detected priority: {ai_priority} (Original: {priority})")
                priority = ai_priority
        issue = Issue(
            title=title, 
            description=description, 
            location=location, 
            latitude=latitude,
            longitude=longitude,
            maps_link=maps_link,
            image_file=image_file, 
            priority=priority, 
            author=current_user
        )
        db.session.add(issue)
        db.session.commit()
        
        # Send SNS Notification for Critical Issues
        if priority == 'Critical' and current_app.config.get('SNS_TOPIC_ARN'):
            try:
                import boto3
                sns = boto3.client('sns', region_name=current_app.config.get('AWS_REGION', 'ap-south-1'))
                subject = f'CRITICAL ISSUE: {title}'
                message = f"""
                A critical issue has been reported:
                
                Title: {title}
                Location: {location}
                Description: {description}
                Reporter: {current_user.username}
                
                View on Google Earth: https://earth.google.com/web/search/{location.replace(' ', '+')}
                """
                sns.publish(
                    TopicArn=current_app.config['SNS_TOPIC_ARN'],
                    Message=message,
                    Subject=subject
                )
                flash('Critical issue reported and admin notified via SMS/Email.', 'success')
            except Exception as e:
                print(f"Failed to send SNS alert: {e}")
                flash('Critical issue reported, but alert notification failed.', 'warning')
        elif priority == 'Critical':
            # Fallback to Flask-Mail if SNS is not configured
            try:
                msg = Message(f'CRITICAL ISSUE: {title}',
                              sender=current_app.config['MAIL_USERNAME'],
                              recipients=[current_app.config['ADMIN_EMAIL']])
                msg.body = f"""
                A critical issue has been reported (SNS not configured):
                
                Title: {title}
                Location: {location}
                Description: {description}
                Reporter: {current_user.username}
                """
                mail.send(msg)
                flash('Critical issue reported and admin notified via email.', 'success')
            except Exception as e:
                print(f"Failed to send backup email: {e}")
                flash('Critical issue reported, but email notification failed.', 'warning')
        else:
            flash('Issue reported successfully!', 'success')
            
        return redirect(url_for('citizen.my_issues'))
        
    return render_template('report_issue.html')

@citizen_bp.route('/my_issues')
@login_required
def my_issues():
    issues = Issue.query.filter_by(author=current_user).order_by(Issue.date_posted.desc()).all()
    return render_template('my_issues.html', issues=issues)
