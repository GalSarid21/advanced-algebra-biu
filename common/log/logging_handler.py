from src.field_elements import AbstractFieldElement
from common.entities import PairMathOperator, SingleMathOperator
from common.consts import Consts
from src.fields import FiniteField

from typing import List, Optional, Tuple

import logging


class LoggingHandler:

    # practically, we don't have a difference between logging.info and
    # logging.error, since we don't add log level to our log.
    # being kept for readability and the best practice.
    @staticmethod
    def log_info(msg: str) -> None:
        logging.info(msg)

    @staticmethod
    def log_error(msg: str) -> None:
        logging.error(msg)

    @staticmethod
    def log_task_start(class_name: str) -> None:
        logging.info(
            Consts.LOG_OPEN_HEADER_SEPARATORS +
            f" Start executing {class_name} " +
            Consts.LOG_OPEN_HEADER_SEPARATORS
        )

    @staticmethod
    def log_task_end() -> None:
        logging.info(Consts.LOG_HEADER_SEPARATORS_LINE)

    @staticmethod
    def log_elements(
        elements: List[AbstractFieldElement],
        start_idx: Optional[int] = 1
    ) -> None:

        for i, element in enumerate(elements, start_idx):
            logging.info(f"Element {i}: {element.a}")
        logging.info("")
    
    @staticmethod
    def log_fields(
        fields: List[FiniteField],
        start_idx: Optional[int] = 1
    ) -> None:

        for i, field in enumerate(fields, start_idx):
            logging.info(f"Field {i}: Degree of f(x) is {field.n}")
        logging.info("")

    @staticmethod
    def log_two_elements_operation(
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

    @staticmethod
    def log_single_element_operation(
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
