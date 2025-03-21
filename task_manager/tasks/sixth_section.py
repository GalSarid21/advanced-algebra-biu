from task_manager.tasks.abstract import AbstractTask
from src.field_elements import(
    FiniteFieldElement,
    PrimeFieldElement,
    AbstractFieldElement
)
from common.entities import PrintMode, SingleMathOperator, PairMathOperator
from common.log import LoggingHandler

from typing import List, Tuple


class SixthSectionTask(AbstractTask):

    def __init__(self) -> None:
        super().__init__("./data/sixth_section.yaml")

    def _run(self) -> None:
        exps = [i for i in range(-2, 3, 1)]
        
        k_elements = self._create_field_elements(
            field_element_class=PrimeFieldElement,
            elements_key="k_elements"
        )

        LoggingHandler.log_info(
            "*** Testing 'exp_by_squaring' for elements in k (PrimeFieldElements)"
        )
        LoggingHandler.log_elements(k_elements, start_idx=0)
        self._test_exp_by_squaring(elements=k_elements, exps=exps)
        LoggingHandler.log_info("")

        l_elements = self._create_field_elements(
            field_element_class=FiniteFieldElement,
            elements_key="l_elements"
        )

        LoggingHandler.log_info(
            "*** Testing 'exp_by_squaring' for elements in l (FiniteFieldElements)"
        )

        LoggingHandler.log_elements(l_elements, start_idx=0)
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
                LoggingHandler.log_info(log_msg)
