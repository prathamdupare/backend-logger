import os
from .cloud_watch_logger import CloudWatchLogger
from .utils import create_log_stream_name, load_logging_config

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, 'config.yaml')

# Load configuration
config = load_logging_config(config_path)

# Access the values from the YAML file
aws_region = config['aws']['region']
log_group = config['aws']['log_group']
logger_name = config['app_logger']['name']
logging_level = config['app_logger']['level']

# Create stream name
stream_name = create_log_stream_name(logger_name)

# Initialize logger
cw_logger = CloudWatchLogger(log_group, aws_region, logger_name, stream_name, logging_level)
logger = cw_logger.create_cw_logger()

# Log initialization message
logger.info(f"CloudWatch logger initialized with log group: {log_group}, stream: {stream_name}")
