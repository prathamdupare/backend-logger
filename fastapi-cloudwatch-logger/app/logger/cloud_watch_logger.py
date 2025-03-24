import logging
import watchtower
import boto3


class CloudWatchLogger:
    def __init__(
        self,
        log_group: str,
        aws_region: str,
        logger_name: str,
        stream_name: str,
        logging_level: int = logging.DEBUG,
    ) -> None:
        self.log_group = log_group
        self.aws_region = aws_region
        self.logger_name = logger_name
        self.logging_level = logging_level
        self.stream_name = stream_name
        self.logger = None

    def set_logger(self):
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(self.logging_level)
        # Clear any existing handlers to avoid duplicates when reusing
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

    
    def add_cw_handler(self):
        cw_handler = watchtower.CloudWatchLogHandler(
            log_group=self.log_group,
            boto3_client=boto3.client("logs", region_name=self.aws_region),
            stream_name=self.stream_name,
        )
        self.logger.addHandler(cw_handler)

    def add_stream_handler(self):
        # Create a console handler to log to the terminal
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    def create_cw_logger(self):
        self.set_logger()
        self.add_stream_handler()
        self.add_cw_handler()
        return self.logger
