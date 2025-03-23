import re
from datetime import datetime
import yaml
import os


def create_log_stream_name(logger_name: str) -> str:
    # Sanitize the logger name: remove invalid characters
    sanitized_name = re.sub(r"[^a-zA-Z0-9_-]", "_", logger_name)

    # Get the current date in the desired format
    timestamp = datetime.now().strftime("%y-%m-%d")

    # Create the log stream name
    log_stream_name = f"{sanitized_name}-{timestamp}"
    return log_stream_name


def load_logging_config(file_path: str):
    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Config file not found: {file_path}")

    # Load the YAML configuration file
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)

    return config


def verify_cloudwatch_setup(region, log_group):
    """Verify CloudWatch log group exists or create it."""
    try:
        logs_client = boto3.client("logs", region_name=region)

        # Check if log group exists
        try:
            logs_client.describe_log_groups(logGroupNamePrefix=log_group)
            print(f"✅ Log group '{log_group}' exists in region '{region}'")
            return True
        except logs_client.exceptions.ResourceNotFoundException:
            # Create log group if it doesn't exist
            print(f"⚠️ Log group '{log_group}' not found. Creating it...")
            logs_client.create_log_group(logGroupName=log_group)
            print(f"✅ Created log group '{log_group}' in region '{region}'")
            return True
    except Exception as e:
        print(f"❌ CloudWatch setup error: {str(e)}")
        return False
