from common.entities import PairMathOperator, SingleMathOperator

import operator


class Consts:

    PAIR_OP_MAP = {
        PairMathOperator.ADD: operator.add,
        PairMathOperator.SUB: operator.sub,
        PairMathOperator.MUL: operator.mul,
        PairMathOperator.DIV: operator.truediv,
        PairMathOperator.EQ: operator.eq
    }

    SINGLE_OP_MAP = {SingleMathOperator.INV: operator.invert}
    SINGLE_OP_CONST_MAP = {SingleMathOperator.INV:-1}

    OP_SYMBOL_MAP = {
        PairMathOperator.ADD: "+",
        PairMathOperator.SUB: "-",
        PairMathOperator.MUL: "*",
        PairMathOperator.DIV: "/",
        PairMathOperator.EQ: "==",
        SingleMathOperator.INV: "~"
    }

    LOG_OPEN_HEADER_SEPARATORS = "="*40
    LOG_HEADER_SEPARATORS_LINE = "="*114
    REDUCIBLE_DEGREES = [2, 3]
