
import requests
import time
import boto3
from app.logger.utils import load_logging_config
import os

def main():
    # Load config
    config_path = os.path.join('app', 'logger', 'config.yaml')
    config = load_logging_config(config_path)
    
    region = config['aws']['region']
    log_group = config['aws']['log_group']
    logger_name = config['app_logger']['name']
    
    # Generate a unique test message
    test_message = f"CloudWatch test message {time.time()}"
    
    print(f"AWS Region: {region}")
    print(f"Log Group: {log_group}")
    
    # Make sure the app is running
    try:
        # Send a request to generate a log
        print(f"Sending test request with message: {test_message}")
        response = requests.get(f"http://127.0.0.1:8000/logging")
        
        if response.status_code == 200:
            print("✅ Test request sent successfully")
            
            # Wait for logs to be delivered
            print("Waiting 10 seconds for logs to be delivered to CloudWatch...")
            time.sleep(10)
            
            # Check if log group exists
            logs_client = boto3.client('logs', region_name=region)
            try:
                log_groups = logs_client.describe_log_groups(logGroupNamePrefix=log_group)
                if log_groups.get('logGroups'):
                    print(f"✅ Log group '{log_group}' exists in CloudWatch")
                    
                    # List log streams
                    streams = logs_client.describe_log_streams(
                        logGroupName=log_group,
                        orderBy='LastEventTime',
                        descending=True,
                        limit=5
                    )
                    
                    if streams.get('logStreams'):
                        print("✅ Log streams found:")
                        for stream in streams['logStreams']:
                            print(f"  - {stream['logStreamName']}")
                            
                            # Get recent logs from this stream
                            events = logs_client.get_log_events(
                                logGroupName=log_group,
                                logStreamName=stream['logStreamName'],
                                limit=10
                            )
                            
                            if events.get('events'):
                                print("  Recent log messages:")
                                for event in events['events']:
                                    print(f"    • {event['message']}")
                            else:
                                print("  No log events found in this stream")
                    else:
                        print("❌ No log streams found in the log group")
                else:
                    print(f"❌ Log group '{log_group}' not found in CloudWatch")
            except Exception as e:
                print(f"❌ Error checking CloudWatch logs: {str(e)}")
        else:
            print(f"❌ Test request failed with status code: {response.status_code}")
    
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the FastAPI app. Make sure it's running on http://127.0.0.1:8000")

if __name__ == "__main__":
    main()
