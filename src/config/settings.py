import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        self.ns_api_url = os.getenv("NS_API_URL")
        self.ns_api_key = os.getenv("NS_API_KEY")

        self.request_timeout = int(
            os.getenv("REQUEST_TIMEOUT", 10)
        )

        self.poll_interval = int(
            os.getenv("POLL_INTERVAL", 30)
        )

        self.eventhub_connection_string = os.getenv(
            "EVENTHUB_CONNECTION_STRING"
        )

        self.eventhub_name = os.getenv(
            "EVENTHUB_NAME"
        )

        self.retry_total = int(
            os.getenv("RETRY_TOTAL", 3)
        )

        self.retry_backoff_factor = float(
            os.getenv("RETRY_BACKOFF_FACTOR", 0.8)
        )

        self.retry_mode = os.getenv(
            "RETRY_MODE", "exponential"
        )

        self.log_level = os.getenv(
            "LOG_LEVEL", "INFO"
        )