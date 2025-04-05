from task_manager.tasks import AbstractTask, ALL_TASKS
from common.entities import TaskType, TaskResult, TaskResultStatus

import common.log.logging_handler as log
import common.consts as consts

from argparse import Namespace
from typing import List, Type


def run(args: Namespace) -> None:
    """Run the tasks specified by the arguments."""
    task_classes = _get_running_task_classes(args)
    for task_cls in task_classes:
        task = task_cls()
        res = task.run()
        if res.status != TaskResultStatus.SUCCESS:
            _handle_unsuccessful_task(res)


def _get_running_task_classes(args: Namespace) -> List[Type[AbstractTask]]:
    """Get the task classes to run based on the arguments."""
    try:
        task_type = TaskType(args.task)
    except Exception:
        # raise readable custom error
        raise ValueError(
            consts.INVALID_ENUM_CREATION_MSG.format(
                obj=TaskType, arg=args.task
            )
        )

    if task_type == TaskType.RUN_ALL:
        return ALL_TASKS

    for task_cls in ALL_TASKS:
        if task_cls.get_type() == task_type:
            return [task_cls]

    raise ValueError(f"Unknown task type: {task_type}")


def _handle_unsuccessful_task(result: TaskResult) -> None:
    """Handle unsuccessful task results."""
    if result.status == TaskResultStatus.ERROR:
        log.error(result.error_msg)
    else:
        raise TypeError("Got unrecognized TaskResultStatus")
