from dataclasses import dataclass
from typing import Optional
from enum import Enum


class PairMathOperator(Enum):
    ADD = "Addition"
    SUB = "Subtraction"
    MUL = "Multiplication"
    DIV = "Division"


class SingleMathOperator(Enum):
    INV = "Inversion"


class PrintMode(Enum):
    VECTOR = 0
    POLYNOMIAL = 1
    MATRIX = 2


class TaskType(Enum):
    RUN_ALL = "run-all"
    SECTION_2 = "section-2"


class TaskResultStatus(Enum):
    SUCCESS = 0
    ERROR = 1


@dataclass
class TaskResult:
    status: TaskResultStatus
    error_msg: Optional[str]
