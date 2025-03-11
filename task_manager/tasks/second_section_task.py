from task_manager.tasks.abstract_task import AbstractTask
from src.field_elements import PrimeFieldElement
from common.entities import SingleMathOperator, PairMathOperator
from common.log import LoggingHandler

from typing import List


class SecondSectionTask(AbstractTask):

    def __init__(self) -> None:
        super().__init__("./data/second_section.yaml")

    def _run(self) -> None:
        elements = self._create_field_elements()
        LoggingHandler.log_elements(elements)
        element_pairs = [(elements[0], elements[1])]

        # run all pair operations: add, sub, mul and div
        for op_type in PairMathOperator:
            LoggingHandler.log_two_elements_operation(
                element_pairs=element_pairs,
                operator_type=op_type
            )

        # run inversion
        # if no inverse exists, return the zero element and print an error message 
        LoggingHandler.log_single_element_operation(
            elements=elements,
            operator_type=SingleMathOperator.INV
        )

    def _create_field_elements(self) -> List[PrimeFieldElement]:
        elements = [
            PrimeFieldElement(a=element["a"], p=element["p"])
            for element in self._data["elements"]
        ]
        return elements
