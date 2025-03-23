import boto3
import time
from app.logger.utils import load_logging_config
from app.check_permissions import check_cloudwatch_permissions
import os
import requests

def check_log_delivery(region, log_group, stream_name, test_message):
    """Check if a specific log message was delivered to CloudWatch."""
    logs_client = boto3.client('logs', region_name=region)
    
    # Wait a bit for logs to be delivered
    print("Waiting 10 seconds for logs to be delivered to CloudWatch...")
    time.sleep(10)
    
    try:
        # Get log events
        response = logs_client.get_log_events(
            logGroupName=log_group,
            logStreamName=stream_name,
            limit=10
        )
        
        # Check if our test message is in the logs
        for event in response.get('events', []):
            if test_message in event.get('message', ''):
                print(f"✅ Test message found in CloudWatch logs!")
                return True
        
        print(f"❌ Test message not found in CloudWatch logs.")
        print("Available log messages:")
        for event in response.get('events', []):
            print(f"  - {event.get('message', '')}")
        return False
    
    except Exception as e:
        print(f"Error checking logs: {str(e)}")
        return False

def main():
    # Check AWS permissions
    print("Checking AWS permissions...")
    check_cloudwatch_permissions()
    
    # Load config
    config_path = os.path.join('app', 'logger', 'config.yaml')
    config = load_logging_config(config_path)
    
    region = config['aws']['region']
    log_group = config['aws']['log_group']
    
    # Generate a unique test message
    test_message = f"CloudWatch test message {time.time()}"
    
    # Make sure the app is running
    try:
        # Send a request to generate a log with our test message
        print(f"Sending test request with message: {test_message}")
        response = requests.get(f"http://127.0.0.1:8000/test-info?message={test_message}")
        
        if response.status_code == 200:
            print("✅ Test request sent successfully")
            
            # Get the current stream name from the app
            from app.logger import stream_name
            
            # Check if the log was delivered
            check_log_delivery(region, log_group, stream_name, test_message)
        else:
            print(f"❌ Test request failed with status code: {response.status_code}")
    
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the FastAPI app. Make sure it's running on http://127.0.0.1:8000")

if __name__ == "__main__":
    main()
