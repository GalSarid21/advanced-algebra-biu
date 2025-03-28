from task_manager.tasks import(
    AbstractTask, ALL_TASKS,
    SecondSectionTask,
    ThirdSectionTask,
    FourthSectionTask,
    FifthSectionTask,
    SixthSectionTask
)
from common.entities import TaskType, TaskResult, TaskResultStatus

import common.log.logging_handler as log
import common.consts as consts

from argparse import Namespace
from typing import List, Type


class TaskManager:

    def __init__(self, args: Namespace) -> None:
        self._args = args

    def run(self) -> None:
        task_classes = self._get_running_task_classes()
        for task_cls in task_classes:
            task = task_cls()
            res = task.run()
            if res.status != TaskResultStatus.SUCCESS:
                self._handle_unsuccessful_task(res)

    def _get_running_task_classes(self) -> List[Type[AbstractTask]]:
        task_type = TaskType(self._args.task)
        try:
            task_type = TaskType(self._args.task)
        except Exception:
            # raise readable custom error
            raise ValueError(
                consts.INVALID_ENUM_CREATION_MSG.format(
                    obj=TaskType, arg=self._args.task
                )
            )

        if task_type == TaskType.RUN_ALL:
            return ALL_TASKS

        for task_cls in ALL_TASKS:
            if task_cls.get_type() == task_type:
                return [task_cls]

        raise ValueError(f"Unknown task type: {task_type}")

    def _handle_unsuccessful_task(self, result: TaskResult) -> None:
        if result.status == TaskResultStatus.ERROR:
            log.error(result.error_msg)

        else:
            raise TypeError("Got unrecognized TaskResultStatus")
