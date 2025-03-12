from src.field_elements import AbstractFieldElement
from common.entities import(
    TaskResult, TaskResultStatus,
    PairMathOperator, SingleMathOperator
)
from common.log import LoggingHandler
from common import Consts

from typing import Dict, Any, List, Tuple, Optional
from abc import ABC, abstractmethod

import yaml


class AbstractTask(ABC):

    @abstractmethod
    def _run(self) -> None:
        """
        Task logic to be ran in the abstract class 'run' function.
        The 'run' function has the basic common steps of logging and
        error handling, internal task logic is implemented in the task
        class and being ran using '_run'.
        """
        pass

    def __init__(self, data_file_path: str) -> None:
        self._data = self.read_task_data(data_file_path)

    def run(self) -> TaskResult:
        try:
            LoggingHandler.log_task_start(self.__class__.__name__)
            self._run()
            LoggingHandler.log_task_end()
            return TaskResult(status=TaskResultStatus.SUCCESS)

        except Exception as e:
            return TaskResult(
                status=TaskResultStatus.ERROR,
                error_msg=(
                    "*** Process was terminated with unexpected error ***" +
                    f"\nError Message: {e}"
                )
            )

    def read_task_data(self, data_file_path: str) -> Dict[str, Any]:
        with open(data_file_path, "r") as f:
            data = yaml.safe_load(f)
        return data

    def _log_two_elements_operation(
        self,
        element_pairs: List[Tuple[AbstractFieldElement, AbstractFieldElement]],
        operator_type: PairMathOperator,
        start_idx: Optional[int] = 1
    ) -> None:

        operator = Consts.PAIR_OP_MAP[operator_type]
        operator_symbol = Consts.OP_SYMBOL_MAP[operator_type]

        for i, pair in enumerate(element_pairs, start_idx):
            e1, e2 = pair
            LoggingHandler.log_info(
                f"{operator_type.value} (e{i}{operator_symbol}e{i+1}): " +
                f"{operator(e1, e2).a}"
            )
        LoggingHandler.log_info("")

    def _log_single_element_operation(
        self,
        elements: List[AbstractFieldElement],
        operator_type: SingleMathOperator,
        start_idx: Optional[int] = 1
    ) -> None:

        operator = Consts.SINGLE_OP_MAP[operator_type]
        operation_const = Consts.SINGLE_OP_CONST_MAP[operator_type]
        operator_symbol = Consts.OP_SYMBOL_MAP[operator_type]

        for i, element in enumerate(elements, start_idx):
            LoggingHandler.log_info(
                f"{operator_type.value} (e{i}{operator_symbol}{operation_const}): " +
                f"{operator(element, operation_const).a}"
            )
        LoggingHandler.log_info("")
