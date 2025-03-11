from datetime import datetime
from typing import Optional

import logging
import base64
import uuid
import os


class LogConfig:

    @staticmethod
    def configure(log_dir: Optional[str] = "logs") -> None:
        """Configures the python logger."""
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d")

        uuid_bytes = uuid.uuid4().bytes
        short_uuid = base64.urlsafe_b64encode(
            uuid_bytes
        ).decode().rstrip("=")

        log_file_path = os.path.join(
            log_dir, f"app_{timestamp}_{short_uuid}.log"
        )

        logging.basicConfig(
            filename=log_file_path,
            filemode="w",
            format="%(message)s",
            level=logging.INFO
        )
