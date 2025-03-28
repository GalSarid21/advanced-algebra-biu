from task_manager.tasks.abstract import AbstractTask
from src.field_elements import PrimeFieldElement
from common.entities import SingleMathOperator, PairMathOperator, TaskType

import common.log.logging_handler as log

from typing import List, Tuple


class SecondSectionTask(AbstractTask):
    _TYPE = TaskType.SECTION_2

    def __init__(self) -> None:
        super().__init__("./data/second_section.yaml")

    def _run(self) -> None:
        elements = self._create_field_elements(PrimeFieldElement)
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

    def _get_element_pairs(
        self,
        elements: List[PrimeFieldElement]
    ) -> List[Tuple[PrimeFieldElement, int, PrimeFieldElement, int]]:
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
