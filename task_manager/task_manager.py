from task_manager.tasks import(
    AbstractTask, ALL_TASKS,
    SecondSectionTask,
    ThirdSectionTask,
    FourthSectionTask,
    FifthSectionTask
)
from common.entities import TaskType, TaskResult, TaskResultStatus
from common.log import LoggingHandler

from argparse import Namespace
from typing import List


class TaskManager:

    def __init__(self, args: Namespace) -> None:
        self._args = args
        # mapping dict to choose tasks dynamically at run time
        self._task_mapping = {
            TaskType.SECTION_2: SecondSectionTask,
            TaskType.SECTION_3: ThirdSectionTask,
            TaskType.SECTION_4: FourthSectionTask,
            TaskType.SECTION_5: FifthSectionTask,
        }

    def run(self) -> None:
        tasks = self._get_running_tasks()
        for task in tasks:
            res = task.run()
            if res.status != TaskResultStatus.SUCCESS:
                self._handle_unsuccessful_task(res)

    def _get_running_tasks(self) -> List[AbstractTask]:
        # invalid task would raise an error
        task_type = TaskType(self._args.task)

        if task_type == TaskType.RUN_ALL:
            return [task() for task in ALL_TASKS]

        return [self._task_mapping[task_type]()]

    def _handle_unsuccessful_task(self, result: TaskResult) -> None:

        if result.status == TaskResultStatus.ERROR:
            LoggingHandler.log_error(result.error_msg)

        else:
            raise TypeError("Got unrecognized TaskResultStatus")
