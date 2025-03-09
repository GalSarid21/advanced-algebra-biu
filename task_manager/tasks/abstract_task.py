from src.field_elements import AbstractFieldElement
from common.entities import TaskResult, PairMathOperator, SingleMathOperator
from common import Consts

from typing import Dict, Any, List, Tuple, Optional
from abc import ABC, abstractmethod

import logging
import yaml


class AbstractTask(ABC):

    @abstractmethod
    def run(self) -> TaskResult:
        """Runs the task logic and returns the TaskResult object."""
        pass

    @abstractmethod
    def _create_field_elements(self) -> List[AbstractFieldElement]:
        """Creates the tesk's field elements using the loaded data."""
        pass

    def __init__(self, data_file_path: str) -> None:
        self._data = self.read_task_data(data_file_path)

    def __new__(cls, *args, **kwargs):
        if cls is AbstractTask:
            # make sure the abstract class can't be instantiate
            raise TypeError(
                f"Cannot instantiate abstract class {cls.__name__}"
            )
        return super().__new__(cls)

    def read_task_data(self, data_file_path: str) -> Dict[str, Any]:
        with open(data_file_path, "r") as f:
            data = yaml.safe_load(f)
        return data

    def _log_test_start(self) -> None:
        logging.info(
            Consts.LOG_OPEN_HEADER_SEPARATORS +
            f" Start executing {self.__class__.__name__} " +
            Consts.LOG_OPEN_HEADER_SEPARATORS
        )
    
    def _log_test_end(self) -> None:
        logging.info(Consts.LOG_HEADER_SEPARATORS_LINE)

    def _log_elements(
        self,
        elements: List[AbstractFieldElement],
        start_idx: Optional[int] = 1
    ) -> None:

        for i, element in enumerate(elements, start_idx):
            logging.info(f"Element {i}: {element.a}")
        logging.info("")

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
            logging.info(
                f"{operator_type.value} (e{i}{operator_symbol}e{i+1}): " +
                f"{operator(e1, e2).a}"
            )
        logging.info("")

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
            logging.info(
                f"{operator_type.value} (e{i}{operator_symbol}{operation_const}): " +
                f"{operator(element, operation_const).a}"
            )
        logging.info("")
