from common.entities import TaskType

from argparse import ArgumentParser, Namespace

import logging
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
            default=TaskType.RUN_ALL.value
        )

        args = parser.parse_args()
        logging.info(
            f"{'='*40} Environment Setup {'='*40}" + "\n" +
            "Environment Variables:\n" +
            json.dumps(vars(args), indent=4)
        )
        return args
