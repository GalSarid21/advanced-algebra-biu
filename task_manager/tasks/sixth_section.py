from task_manager.tasks.abstract import AbstractTask
from src.field_elements import(
    FiniteFieldElement,
    PrimeFieldElement,
    AbstractFieldElement
)
from common.entities import TaskType

import common.log.logging_handler as log

from typing import List


class SixthSectionTask(AbstractTask):
    _TYPE = TaskType.SECTION_6

    def __init__(self) -> None:
        super().__init__("./data/sixth_section.yaml")

    def _run(self) -> None:
        exps = [i for i in range(-2, 3, 1)]
        
        k_elements = self._create_field_elements(
            field_element_class=PrimeFieldElement,
            elements_key="k_elements"
        )

        log.info(
            "*** Testing 'exp_by_squaring' for elements in k (PrimeFieldElements)"
        )
        log.elements(k_elements, start_idx=0)
        self._test_exp_by_squaring(elements=k_elements, exps=exps)
        log.info("")

        l_elements = self._create_field_elements(
            field_element_class=FiniteFieldElement,
            elements_key="l_elements"
        )

        log.info(
            "*** Testing 'exp_by_squaring' for elements in l (FiniteFieldElements)"
        )

        log.elements(l_elements, start_idx=0)
        self._test_exp_by_squaring(elements=l_elements, exps=exps)

    def _test_exp_by_squaring(
        self,
        elements: List[AbstractFieldElement],
        exps: List[int]
    ) -> None:

        for i, element in enumerate(elements):
            for exp in exps:
                exp_op_res = element.exp_by_squaring(n=exp)
                if exp_op_res is not None:
                    log_msg = f"'exp_by_squaring' [e{i}**{exp}]: {exp_op_res.a}"
                else:
                    log_msg = "OPERATION FAILED (error message above)"
                log.info(log_msg)
