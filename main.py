from task_manager.cli import CliEnvArgs
from task_manager import TaskManager
from common import LogConfig

import traceback
import logging
import sys


if __name__ == "__main__":

    try:
        LogConfig.configure()
        args = CliEnvArgs.get_args()
        task_manager = TaskManager(args)
        task_manager.run()

    except KeyboardInterrupt:
        sys.exit(130)

    except Exception as e:
        logging.error(
            f"Unexpected Error: {e}\n" +\
            f"Stacktrace:\n{traceback.format_exc()}"
        )
