from common.entities import PairMathOperator, SingleMathOperator

import operator


class Consts:

    PAIR_OP_MAP = {
        PairMathOperator.ADD: operator.add,
        PairMathOperator.SUB: operator.sub,
        PairMathOperator.MUL: operator.mul,
        PairMathOperator.DIV: operator.truediv,
    }

    SINGLE_OP_MAP = {SingleMathOperator.INV: operator.pow}
    SINGLE_OP_CONST_MAP = {SingleMathOperator.INV:-1}

    OP_SYMBOL_MAP = {
        PairMathOperator.ADD: "+",
        PairMathOperator.SUB: "-",
        PairMathOperator.MUL: "*",
        PairMathOperator.DIV: "/",
        SingleMathOperator.INV: "**"
    }

    LOG_OPEN_HEADER_SEPARATORS = "="*40
    LOG_HEADER_SEPARATORS_LINE = "="*100
