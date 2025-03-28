from common.entities import TaskType
import common.log.logging_handler as log

from argparse import ArgumentParser, Namespace
import json


def read_cli_env_args() -> Namespace:
    parser = ArgumentParser("")

    parser.add_argument(
        "--task",
        help="target task to execute.",
        type=str,
        choices=[task.value for task in TaskType],
        default=TaskType.RUN_ALL.value
    )

    args = parser.parse_args()
    log.info(
        f"{'='*48} Environment Setup {'='*48}" + "\n" +
        "Environment Variables:\n" +
        json.dumps(vars(args), indent=4)
    )
    return args
