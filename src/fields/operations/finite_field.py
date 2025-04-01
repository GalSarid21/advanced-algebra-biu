from src.field_elements import FiniteFieldElement
from src.fields import FiniteField

import common.log.logging_handler as log

from itertools import product
import numpy as np


def find_generator(field: FiniteField):
    # create an array of field elements, ranging from 0 to p-1
    field_elements = np.arange(field.p)
    # create a list of n copies of the field elements for generating vectors of length n
    field_elements_n = [field_elements for _ in range(field.n)]
    # generate all possible combinations (vectors) of elements in the field, except the zero vector
    vectors = list(product(*field_elements_n))[1:]

    for vector in vectors:
        finite_field_element = FiniteFieldElement(vector, field.p, field.fx)
        order = finite_field_element.mul_order()
        if order is not None and order == field.p**field.n - 1:
            return finite_field_element

    log.error(
        "failed to find generator for field: " +
        f"p = {field.p} | fx = {field.fx}"
    )
