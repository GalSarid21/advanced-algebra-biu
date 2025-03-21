from common.entities import TaskType
from common.log import LoggingHandler

from argparse import ArgumentParser, Namespace

import json


class CliEnvArgs:
    
    @staticmethod
    def get_args() -> Namespace:
        parser = ArgumentParser("")

        parser.add_argument(
            "--task",
            help="target task to execute.",
            type=str,
            choices=[task.value for task in TaskType],
            # default=TaskType.RUN_ALL.value
            # TEST:
            default=TaskType.SECTION_6.value
        )

        args = parser.parse_args()
        LoggingHandler.log_info(
            f"{'='*48} Environment Setup {'='*48}" + "\n" +
            "Environment Variables:\n" +
            json.dumps(vars(args), indent=4)
        )
        return args
