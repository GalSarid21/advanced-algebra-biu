from src.field_elements import AbstractFieldElement

from typing import Union
from copy import deepcopy

import logging
import galois


class PrimeFieldElement(AbstractFieldElement):
    """
    Represents an element in a prime field, where p is a prime number.

    This class provides arithmetic operations (addition, subtraction,
    multiplication, division, and exponentiation) within the field using
    modular arithmetic.
    It supports operator overloading to ensure all operations respect
    field properties.

    Features:
    - Ensures elements belong to the prime field using the Galois field library.
    - Supports exponentiation using efficient exponentiation by squaring.
    - Computes the multiplicative order of an element.
    - Handles inversion and error cases correctly.

    Attributes:
        a (galois.FieldArray): The field element.
        p (int): The prime number defining the field.
    """
    def __init__(self, a: Union[galois.FieldArray, int], p: int) -> None:
        super().__init__(p)  
        self._gf_p = galois.GF(self._p)

        # a represent the element in the field.
        # can be passed as int or 'galois.FieldArray'.
        # if a is an int, we create a 'galois.FieldArray'
        # object using it and assign as the class value of a.
        if isinstance(a, int):
            self._a = self._gf_p(a % self._p)
        elif isinstance(a, self._gf_p):
            self._a = a
        else:
            raise ValueError(
                "a must be if type 'int' or 'galois.FieldArray'"
            )

    @property
    def gf_p(self) -> galois.FieldArray:
        return self._gf_p

    @property
    def order(self) -> int:
        return (
            self._p if self._a != 0
            else 1
        )

    # OPERATOR OVERLOADING:
    # Defines how basic operations (such addition, subtraction, etc.)
    # of two objects of the class will be performed.
    def __add__(self, other: "PrimeFieldElement") -> "PrimeFieldElement":
        other.type_check(PrimeFieldElement)
        return PrimeFieldElement(self._a + other.a, self._p)

    def __sub__(self, other: "PrimeFieldElement") -> "PrimeFieldElement":
        other.type_check(PrimeFieldElement)
        return PrimeFieldElement(self._a - other.a, self._p)          

    def __mul__(self, other: "PrimeFieldElement"):
        other.type_check(PrimeFieldElement)
        return PrimeFieldElement(self._a * other.a, self._p)

    def __truediv__(self, other: "PrimeFieldElement") -> "PrimeFieldElement":
        other.type_check(PrimeFieldElement)
        return PrimeFieldElement(self._a / other.a, self._p)   

    def __pow__(self, exp: int) -> "PrimeFieldElement":
        # uses only for inversion, hence checking that exp is -1.
        # 'regular' exponential is calculated using the 'exp_by_squaring'
        # function.
        if self._a == 0:
            # in the multiplicative group zero element doesn't exist
            logging.error("Error! 'a' does not have an inverse in 'k' field")
            return self
        if exp != -1:
            raise ValueError(
                "'**' operator is using for inversion only, 'exp' must be -1!"
            )
        return PrimeFieldElement(self._a**exp, self._p)

    def get_multiplicative_identity(self) -> "PrimeFieldElement":
        """Returns the multiplicative identity element (1) of the prime field."""
        return PrimeFieldElement(1, self._p)

    def mul_order(self) -> int:
        """
        Computes the multiplicative order of 'a' in the prime field.
        The multiplicative order of an element a is the smallest positive
        integer k such that a^k=1(mod p).
        This function iteratively computes a^k by multiplying self._a
        (representation of the element in the field) until it cycles
        back to 1.
        """
        if self._a == 0:
            # TODO: consider throwing an error
            # raise ValueError("Error: a is zero, not in the prime field")
            print("Error: a is zero, not in the prime field")
            return
        else:
            pow = 1
            result = deepcopy(self._a)

            while result != 1:
                result = result*self._a
                pow += 1

            return pow
