from src.field_elements import AbstractFieldElement

import common.log.logging_handler as log

from typing import Union, Optional
from copy import deepcopy

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
        a_orig (galois.FieldArray | int): The original 'a' value before mod operation.
        a (galois.FieldArray | int): The field element.
        p (int): The prime number defining the field.
    """
    def __init__(self, a: Union[galois.FieldArray, int], p: int) -> None:
        super().__init__(p)  
        self._gf_p = galois.GF(self._p)
        self._a_orig = a
        # 'a' represent the element in the field.
        # can be passed as int or 'galois.FieldArray'.
        # if 'a' is an int, we create a 'galois.FieldArray'
        # object using it and assign as the object value of 'a'.
        if isinstance(a, int):
            self._a = self._gf_p(a % self._p)
        elif isinstance(a, galois.FieldArray):
            self._a = a
        else:
            raise ValueError(
                "Input 'a' must be of type 'int' or 'galois.FieldArray'"
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
    def __add__(self, other: "PrimeFieldElement") -> Optional["PrimeFieldElement"]:
        self.type_check(other)
        # both 'self._a' and 'other.a' are 'galois.FieldArray'.
        # the 'galois' package handles modular arithmetic.
        try:
            return PrimeFieldElement(self._a + other.a, self._p)
        except Exception as e:
            log.error(f"Error:\n{e}")

    def __sub__(self, other: "PrimeFieldElement") -> Optional["PrimeFieldElement"]:
        self.type_check(other)
        # both 'self._a' and 'other.a' are 'galois.FieldArray'.
        # the 'galois' package handles modular arithmetic.
        try:
            return PrimeFieldElement(self._a - other.a, self._p)
        except Exception as e:
            log.error(f"Error:\n{e}")   

    def __mul__(self, other: "PrimeFieldElement"):
        self.type_check(other)
        # both 'self._a' and 'other.a' are 'galois.FieldArray'.
        # the 'galois' package handles modular arithmetic.
        try:
            return PrimeFieldElement(self._a * other.a, self._p)
        except Exception as e:
            log.error(f"Error:\n{e}")

    def __truediv__(self, other: "PrimeFieldElement") -> Optional["PrimeFieldElement"]:
        self.type_check(other)
        # both 'self._a' and 'other.a' are 'galois.FieldArray'.
        # the 'galois' package handles modular arithmetic.
        try:
            return PrimeFieldElement(self._a / other.a, self._p)
        except Exception as e:
            log.error(f"Error:\n{e}")
    
    def __invert__(self) -> Optional["PrimeFieldElement"]:
        try:
            return PrimeFieldElement(self._a**-1, self._p)
        except Exception as e:
            log.error(f"Error:\n{e}")

    # we added equality check overload
    def __eq__(self, other: "PrimeFieldElement") -> bool:
        self.type_check(other)
        # verifies same field and element equality
        return self._p == other.p and self._a == other.a

    def get_multiplicative_identity(self) -> Optional["PrimeFieldElement"]:
        """Returns the multiplicative identity element (1) of the prime field."""
        return PrimeFieldElement(1, self._p)

    def mul_order(self) -> Optional[int]:
        """
        Computes the multiplicative order of 'a' in the prime field.
        The multiplicative order of an element a is the smallest positive
        integer k such that a^k=1(mod p).
        This function iteratively computes a^k by multiplying self._a
        (representation of the element in the field) until it cycles
        back to 1.
        """
        if self._a == 0:
            log.error(
                "Error: a is zero, not in the prime field"
            )
            return
        else:
            pow = 1
            # self._a can be int or galois.FieldArray.
            # if its a galois.FieldArray, a deepcopy is needed to 
            # avoid changing self._a while searching the mul_order
            result = (
                self._a if isinstance(self._a, int)
                else deepcopy(self._a)
            )

            while result != 1:
                result = result*self._a
                pow += 1

            return pow
