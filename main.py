from task_manager.cli.env_args import read_cli_env_args
from common.log.config import configure_log
from task_manager import TaskManager

import common.log.logging_handler as log

import traceback
import sys


if __name__ == "__main__":

    try:
        configure_log()
        args = read_cli_env_args()
        task_manager = TaskManager(args)
        task_manager.run()

    except KeyboardInterrupt:
        sys.exit(130)

    except Exception as e:
        log.error(
            f"Unexpected Error: {e}\n" +\
            f"Stacktrace:\n{traceback.format_exc()}"
        )
