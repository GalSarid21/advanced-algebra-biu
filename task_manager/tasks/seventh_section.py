from task_manager.tasks.abstract import AbstractTask
from src.field_elements import(
    AbstractFieldElement,
    FiniteFieldElement,
    PrimeFieldElement
)
from common.entities import TaskType

import common.log.logging_handler as log

from typing import List


class SeventhSectionTask(AbstractTask):
    _TYPE = TaskType.SECTION_7

    def _run(self) -> None:

        k_elements = self._create_field_elements(
            field_element_class=PrimeFieldElement,
            elements_key="k_elements"
        )

        log.info(
            "*** Testing 'order' and 'mul_order' for elements in k (PrimeFieldElements)"
        )
        log.elements(k_elements, start_idx=0)
        self._test_field_elements_order(k_elements)
        log.info("")

        l_elements = self._create_field_elements(
            field_element_class=FiniteFieldElement,
            elements_key="l_elements"
        )

        log.info(
            "*** Testing 'order' and 'mul_order' for elements in l (FiniteFieldElements)"
        )
        log.elements(l_elements, start_idx=0)
        self._test_field_elements_order(l_elements)

    def _test_field_elements_order(
        self,
        elements: List[AbstractFieldElement]
    ) -> None:

        for i, element in enumerate(elements):
            msg = f"e{i}: Multiplicative Order = {element.mul_order()}"
            if isinstance(element, PrimeFieldElement):
                msg += f" | Order = {element.order}"
            log.info(msg)
