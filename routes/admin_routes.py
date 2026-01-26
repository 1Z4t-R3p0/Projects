from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from models import db, Issue

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        flash('Access denied. Admin only.', 'error')
        return redirect(url_for('citizen.my_issues'))
        
    issues = Issue.query.order_by(Issue.date_posted.desc()).all()
    
    # Simple Stats
    total_issues = len(issues)
    pending = sum(1 for i in issues if i.status == 'Pending')
    resolved = sum(1 for i in issues if i.status == 'Resolved')
    
    return render_template('admin_dashboard.html', 
                           issues=issues, 
                           total=total_issues, 
                           pending=pending, 
                           resolved=resolved)

@admin_bp.route('/admin/issue/<int:issue_id>')
@login_required
def issue_detail(issue_id):
    if current_user.role != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('citizen.my_issues'))
        
    issue = Issue.query.get_or_404(issue_id)
    return render_template('issue_detail.html', issue=issue)

@admin_bp.route('/admin/issue/<int:issue_id>/update', methods=['POST'])
@login_required
def update_issue(issue_id):
    if current_user.role != 'admin':
        return redirect(url_for('citizen.my_issues'))
        
    issue = Issue.query.get_or_404(issue_id)
    new_status = request.form.get('status')
    if new_status:
        issue.status = new_status
        db.session.commit()
        flash(f'Issue status updated to {new_status}', 'success')
        
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/admin/issue/<int:issue_id>/delete', methods=['POST'])
@login_required
def delete_issue(issue_id):
     if current_user.role != 'admin':
        return redirect(url_for('citizen.my_issues'))
        
     issue = Issue.query.get_or_404(issue_id)
     db.session.delete(issue)
     db.session.commit()
     flash('Issue record deleted.', 'success')
     return redirect(url_for('admin.dashboard'))
