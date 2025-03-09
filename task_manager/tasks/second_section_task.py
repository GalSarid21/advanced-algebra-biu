from task_manager.tasks.abstract_task import AbstractTask
from src.field_elements import PrimeFieldElement
from common.entities import TaskResult, PairMathOperator, SingleMathOperator

from typing import List


class SecondSectionTask(AbstractTask):

    def __init__(self) -> None:
        super().__init__("./data/second_section.yaml")

    def run(self) -> TaskResult:

        self._log_test_start()
        elements = self._create_field_elements()
        self._log_elements(elements)
        element_pairs = [(elements[0], elements[1])]

        # run all pair operations: add, sub, mul and div
        for op_type in PairMathOperator:
            self._log_two_elements_operation(
                element_pairs=element_pairs,
                operator_type=op_type
            )

        # run inversion
        self._log_single_element_operation(
            elements=elements,
            operator_type=SingleMathOperator.INV
        )

        self._log_test_end()

    def _create_field_elements(self) -> List[PrimeFieldElement]:
        elements = [
            PrimeFieldElement(a=element["a"], p=element["p"])
            for element in self._data["elements"]
        ]
        return elements
