from task_manager.tasks import(
    AbstractTask,
    SecondSectionTask
)
from common.entities import TaskType

from argparse import Namespace
from typing import List


class TaskManager:

    def __init__(self, args: Namespace) -> None:
        self._args = args

    def run(self) -> None:
        tasks = self._get_running_tasks()
        for task in tasks:
            task.run()

    def _get_running_tasks(self) -> List[AbstractTask]:
        # invalid task would raise an error
        task_type = TaskType(self._args.task)

        if task_type == TaskType.RUN_ALL:
            return [
                SecondSectionTask(),
                # ThirdSectionTask(), etc
            ]

        elif task_type == TaskType.SECTION_2:
            return [SecondSectionTask()]
