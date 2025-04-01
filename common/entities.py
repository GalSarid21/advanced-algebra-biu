from src.field_elements import AbstractFieldElement

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class PairMathOperator(Enum):
    ADD = "Addition"
    SUB = "Subtraction"
    MUL = "Multiplication"
    DIV = "Division"
    EQ = "Equality"


class SingleMathOperator(Enum):
    INV = "Inversion"


class PrintMode(Enum):
    VECTOR = 0
    POLYNOMIAL = 1
    MATRIX = 2


class TaskType(Enum):
    RUN_ALL = "run-all"
    SECTION_2 = "section-2"
    SECTION_3 = "section-3"
    SECTION_4 = "section-4"
    SECTION_5 = "section-5"
    SECTION_6 = "section-6"
    SECTION_7 = "section-7"
    SECTION_8 = "section-8"


class TaskResultStatus(Enum):
    SUCCESS = 0
    ERROR = 1


@dataclass
class TaskResult:
    status: TaskResultStatus
    error_msg: Optional[str] = None
