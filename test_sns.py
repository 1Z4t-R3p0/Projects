import boto3
import os

# SNS Configuration
# This ARN matches your deployed infrastructure
SNS_TOPIC_ARN = 'arn:aws:sns:ap-south-1:502713365215:smart-citizen-alerts'
AWS_REGION = 'ap-south-1'

def test_sns():
    print(f"Testing connectivity to SNS Topic: {SNS_TOPIC_ARN}")
    
    try:
        # Initialize SNS Client
        sns = boto3.client('sns', region_name=AWS_REGION)
        
        # Create a test message
        message = """
        [TEST ALERT] Smart Citizen Reporter
        -----------------------------------
        This is a validation message to confirm that your AWS SNS configuration 
        is working correctly.
        
        Status: SUCCESS ✅
        Region: ap-south-1
        Time: Live Test
        """
        
        # Publish to SNS
        response = sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject='🔔 SNS Test Notification - Smart Citizen'
        )
        
        print("\n✅ Message Published Successfully!")
        print(f"Message ID: {response['MessageId']}")
        print("Please check your subscribed Email/SMS for the notification.")
        
    except Exception as e:
        print("\n❌ Failed to publish SNS message.")
        print(f"Error: {e}")

if __name__ == "__main__":
    test_sns()
