from task_manager.tasks import(
    AbstractTask,
    SecondSectionTask
)
from common.entities import TaskType, TaskResult, TaskResultStatus

from argparse import Namespace
from typing import List

import importlib
import inspect
import pkgutil
import logging


class TaskManager:

    def __init__(self, args: Namespace) -> None:
        self._args = args

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
            return self._load_task_classes()

        elif task_type == TaskType.SECTION_2:
            return [SecondSectionTask()]

    def _load_task_classes(self) -> List[AbstractTask]:
        """Dynamically loads all concrete Task classes from the tasks folder."""
        task_classes = []
        package = "task_manager.tasks"

        for _, module_name, _ in pkgutil.iter_modules([f"./{package.replace('.', '/')}"]):
            module = importlib.import_module(f"{package}.{module_name}")
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, AbstractTask) and obj is not AbstractTask and not name.lower().startswith("abstract_"):
                    task_classes.append(obj())

        return task_classes

    def _handle_unsuccessful_task(self, result: TaskResult) -> None:

        if result.status == TaskResultStatus.ERROR:
            logging.error(result.error_msg)

        else:
            raise TypeError("Got unrecognized TaskResultStatus")
