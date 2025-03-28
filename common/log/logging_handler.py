from src.field_elements import AbstractFieldElement
from common.entities import PairMathOperator, SingleMathOperator
from src.fields import FiniteField

import common.consts as consts

from typing import List, Optional, Tuple

import logging
import numpy as np


def info(msg: str) -> None:
    logging.info(msg)

def error(msg: str) -> None:
    # practically, we don't have a difference between logging.info and
    # logging.error, since we don't add log level to our log.
    # being kept for readability and the best practice.
    logging.error(msg)

def task_start(class_name: str) -> None:
    logging.info(
        consts.LOG_OPEN_HEADER_SEPARATORS +
        f" Start executing {class_name} " +
        consts.LOG_OPEN_HEADER_SEPARATORS
    )

def task_end() -> None:
    logging.info(consts.LOG_HEADER_SEPARATORS_LINE)

def elements(
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
        info(log_msg)

    if end_with_empty_line:
        logging.info("")

def fields(
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

def two_elements_operation(
    element_pairs: List[Tuple[AbstractFieldElement, AbstractFieldElement]],
    operator_type: PairMathOperator,
    end_with_empty_line: Optional[bool] = True
) -> None:

    operator = consts.PAIR_OP_MAP[operator_type]
    operator_symbol = consts.OP_SYMBOL_MAP[operator_type]

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

def single_element_operation(
    elements: List[AbstractFieldElement],
    operator_type: SingleMathOperator,
    start_idx: Optional[int] = 1,
    end_with_empty_line: Optional[bool] = True
) -> None:

    operator = consts.SINGLE_OP_MAP[operator_type]
    # operation_const = consts.SINGLE_OP_CONST_MAP[operator_type]
    operator_symbol = consts.OP_SYMBOL_MAP[operator_type]

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
