from src.field_elements import(
    AbstractFieldElement,
    PrimeFieldElement,
    FiniteFieldElement
)
from common.entities import TaskResult, TaskResultStatus, TaskType
from src.fields import FiniteField

import common.log.logging_handler as log
import common.consts as consts

from typing import Dict, Any, List, Optional, Union
from abc import ABC, abstractmethod

import yaml


class AbstractTask(ABC):
    _TYPE = None

    @abstractmethod
    def _run(self) -> None:
        """
        Task logic to be ran in the abstract class 'run' function.
        The 'run' function has the basic common steps of logging and
        error handling, internal task logic is implemented in the task
        class and being ran using '_run'.
        """
        pass

    def __init__(self) -> None:
        data_file_path =\
            consts.TASK_DATA_FILE_PATH.format(section=self._TYPE.value)
        self._data = self.read_task_data(data_file_path)

    def run(self) -> TaskResult:
        try:
            log.task_start(self.__class__.__name__)
            self._run()
            log.task_end()
            return TaskResult(status=TaskResultStatus.SUCCESS)

        except Exception as e:
            return TaskResult(
                status=TaskResultStatus.ERROR,
                error_msg=(
                    "*** Process was terminated with unexpected error ***" +
                    f"\nError Message: {e}"
                )
            )

    @classmethod
    def get_type(cls) -> TaskType:
        return cls._TYPE

    def read_task_data(self, data_file_path: str) -> Dict[str, Any]:
        with open(data_file_path, "r") as f:
            data = yaml.safe_load(f)
        return data

    def _create_field_elements(
        self,
        field_element_class: AbstractFieldElement,
        elements_key: Optional[str] = "elements"
    ) -> List[AbstractFieldElement]:

        if issubclass(field_element_class, PrimeFieldElement):
            elements = [
                PrimeFieldElement(a=element["a"], p=element["p"])
                for element in self._data[elements_key]
            ]

        elif issubclass(field_element_class, FiniteFieldElement):
            elements = [
                FiniteFieldElement(
                    a=element["a"],
                    p=element["p"],
                    fx=element["fx"]
                ) for element in self._data[elements_key]
            ]

        else:
            raise TypeError(
                f"Invalid field element: {field_element_class}"
            )

        return elements

    def _log_field_creation_error(
        self,
        field: Union[Dict[str, Any], FiniteField],
        e: Exception,
        end_with_new_line: Optional[bool] = False
    ) -> None:

        if isinstance(field, FiniteField):
            p = field.p
            fx = field.fx
        else:
            p = field["p"]
            fx = field["fx"]

        err_msg = f"{e}\n(P={p} | f(x)={fx})"
        if end_with_new_line is True:
            err_msg += "\n"
        log.error(err_msg)
