from src.field_elements import AbstractFieldElement
from common.entities import PairMathOperator, SingleMathOperator
from common.consts import Consts
from src.fields import FiniteField

from typing import List, Optional, Tuple

import logging
import numpy as np


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
        start_idx: Optional[int] = 1,
        add_element_image: Optional[bool] = False,
        end_with_empty_line: Optional[bool] = True
    ) -> None:

        last_element_idx = (
            len(elements) if start_idx == 1
            else len(elements) - 1
        )

        for i, element in enumerate(elements, start_idx):
            # P and a_orig helps to see if the mod operation is correct
            log_msg = f"Element {i}: {element.a} (P={element.p} | a_orig={element.a_orig})"
            if add_element_image:
                log_msg += f"\nElement image:\n{element.a_matrix}"
                if i != last_element_idx:
                    log_msg += "\n"
            LoggingHandler.log_info(log_msg)

        if end_with_empty_line:
            logging.info("")
    
    @staticmethod
    def log_fields(
        fields: List[FiniteField],
        start_idx: Optional[int] = 1,
        end_with_empty_line: Optional[bool] = True
    ) -> None:

        for i, field in enumerate(fields, start_idx):
            logging.info(
                f"Field {i}: P={field.p} | f(x)={field.fx} | " +
                f"Degree={field.n}"
            )

        if end_with_empty_line:
            logging.info("")

    @staticmethod
    def log_two_elements_operation(
        element_pairs: List[Tuple[AbstractFieldElement, AbstractFieldElement]],
        operator_type: PairMathOperator,
        end_with_empty_line: Optional[bool] = True
    ) -> None:

        operator = Consts.PAIR_OP_MAP[operator_type]
        operator_symbol = Consts.OP_SYMBOL_MAP[operator_type]

        for e1, i1, e2, i2 in element_pairs:
            log_msg = f"{operator_type.value} (e{i1}{operator_symbol}e{i2}): "

            op_res = operator(e1, e2)
            if op_res is not None:
                if type(op_res) in [np.bool, bool]:
                    log_msg += f"{op_res}"
                else:
                    log_msg += f"{op_res.a}"
            else:
                log_msg += "OPERATION FAILED (error message above)"
            logging.info(log_msg)

        if end_with_empty_line:
            logging.info("")

    @staticmethod
    def log_single_element_operation(
        elements: List[AbstractFieldElement],
        operator_type: SingleMathOperator,
        start_idx: Optional[int] = 1,
        end_with_empty_line: Optional[bool] = True
    ) -> None:

        operator = Consts.SINGLE_OP_MAP[operator_type]
        # operation_const = Consts.SINGLE_OP_CONST_MAP[operator_type]
        operator_symbol = Consts.OP_SYMBOL_MAP[operator_type]

        for i, element in enumerate(elements, start_idx):
            log_msg = f"{operator_type.value} ({operator_symbol}e{i}): "
            op_res = operator(element)

            if op_res is not None:
                log_msg += f"{op_res.a}"
            else:
                log_msg += "OPERATION FAILED (error message above)"
            logging.info(log_msg)

        if end_with_empty_line:
            logging.info("")
