from task_manager.tasks.abstract import AbstractTask
from src.field_elements import FiniteFieldElement
from common.entities import (
    PrintMode, TaskType,
    SingleMathOperator, PairMathOperator
)

import common.log.logging_handler as log

from typing import List, Tuple


class FifthSectionTask(AbstractTask):
    _TYPE = TaskType.SECTION_5

    def __init__(self) -> None:
        super().__init__("./data/fifth_section.yaml")

    def _run(self) -> None:
        elements = self._create_field_elements(FiniteFieldElement)
        log.info(
            "*** Testing 'pretty_print' function of FiniteFieldElement:"
        )

        # elements[0] is the 0-element
        test_single_element = elements[1]
        self._test_default_print_mode(test_single_element)

        for i, print_mode in enumerate(PrintMode):
            # 'pretty_print' returns the log_msg to print
            log_msg = test_single_element.pretty_print(print_mode)
            if i == len(PrintMode) - 1:
                log_msg += "\n"
            log.info(log_msg)

        log.info(
            "*** Testing FiniteFieldElement Operator overloading:"
        )
        log.elements(elements, start_idx=0)
        element_pairs = self._get_element_pairs(elements)

        # run all pair operations: add, sub, mul and div
        for op_type in PairMathOperator:
            log.two_elements_operation(
                element_pairs=element_pairs,
                operator_type=op_type
            )

        # run inversion
        # if no inverse exists, return the zero element and print an error message 
        log.single_element_operation(
            elements=elements,
            operator_type=SingleMathOperator.INV,
            end_with_empty_line=False,
            start_idx=0
        )

    def _test_default_print_mode(self, element: FiniteFieldElement) -> None:
        log_msg = f"Test Default PrintMode:\n{element.pretty_print()}"
        log.info(log_msg)

    def _get_element_pairs(
        self,
        elements: List[FiniteFieldElement]
    ) -> List[Tuple[FiniteFieldElement, int, FiniteFieldElement, int]]:
        return [
            # operation with the 0-element (elements[0])
            (elements[1], 1, elements[0], 0),
            # 'regular' operation
            (elements[1], 1, elements[2], 2),
            # operation of something with itself
            (elements[2], 2, elements[2], 2),
            # operation with element from a different field (elements[-1])
            (elements[3], 3, elements[4], 4),
        ]
