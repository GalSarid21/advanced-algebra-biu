from src.field_elements import AbstractFieldElement
from common.entities import PrintMode
from src.fields import FiniteField

import common.log.logging_handler as log

from typing import List, Union, Optional
from copy import deepcopy

import galois
import numpy as np


class FiniteFieldElement(AbstractFieldElement):
    """
    Represents an element in a finite field defined by a prime power p^n,
    where p is a prime number and n is the degree of the extension.

    This class provides arithmetic operations (addition, subtraction, multiplication,
    division, and exponentiation) within the finite field using modular arithmetic
    and matrix representations. It supports operator overloading to ensure all operations
    respect the field properties.

    Features:
    - Represents finite field elements using matrix embeddings to capture the field structure.
    - Supports arithmetic operations based on matrix representations of elements.
    - Handles element inversion and division, including error handling for division by zero.
    - Supports exponentiation through efficient matrix exponentiation.
    - Computes the multiplicative order of an element.
    - Provides utility methods for pretty-printing elements in various formats (vector, polynomial, matrix).
    - Supports finding a generator (primitive element) of the finite field.

    Attributes:
        a_orig (np.ndarray | List[int]): The original 'a' value before mod operation.
        a (np.ndarray | List[int]): The array of coefficients representing the element in the finite field.
        p (int): The prime number defining the finite field.
        fx (np.ndarray): The irreducible polynomial defining the field extension.
        n (int): The degree of the field extension.
        a_matrix (np.ndarray): The matrix representation of the element.
        field (FiniteField): The finite field associated with this element.
    """
    def __init__(
        self,
        a: Union[np.ndarray, List[int]],
        p: int,
        fx: Union[np.ndarray, List[int]]
    ) -> None:
        super().__init__(p)

        # irreducible polynomia
        self._fx = (
            fx if isinstance(fx, np.ndarray)
            else np.array(fx)
        )
        
        # polynomia degree
        self._n = len(fx) - 1
        self._a_orig = a

        # number of elements in 'a' can't be greater than len(fx)
        if len(a) > len(fx):
            raise ValueError(
                f"Got {len(a)} coefficients for a field of degree {self._n}"
            )

        a_arr = np.array(a) if not isinstance(a, np.ndarray) else a
        a_mod = np.mod(a_arr, self._p)
        # number of elements 'a' can be less than len(fx)
        # in that case - we need to pad 'a'
        if len(a_mod) < len(fx):
            a_mod = np.pad(a_mod, (0, self._n - len(a)), "constant")
        self._a = a_mod

        try:
            # reducible field would raise an error
            self._field = FiniteField(self._p, self._fx)
        except Exception as e:
            # raising a more accurate error
            raise ValueError(
                "FiniteFieldElement creation failed due to a field " +
                f"creation error:\n{e}"
            )

        self._a_matrix = self.element_embedding_GLn(self._a)   

    @property
    def fx(self) -> np.ndarray:
        return self._fx

    @property
    def n(self) -> int:
        return self._n

    @property
    def a_matrix(self) -> np.ndarray:
        return self._a_matrix

    @property
    def field(self) -> FiniteField:
        return self._field

    # OPERATOR OVERLOADING:
    # Defines how basic operations (such addition, subtraction, etc.)
    # of two objects of the class will be performed.
    # Here we're basing our operations on the matrix representation of
    # the element.
    def __add__(self, other: "FiniteFieldElement") -> Optional["FiniteFieldElement"]:
        try:
            self.type_check(other)
            self._check_other_is_from_the_same_field(other, "Addition")
            mat_result = self._a_matrix + other.a_matrix
            result = np.mod(mat_result, self._p) 
            return FiniteFieldElement(result[0, :], self._p, self._fx)
        except Exception as e:
            log.error(e)

    def __sub__(self, other: "FiniteFieldElement") -> Optional["FiniteFieldElement"]:
        try:
            self.type_check(other)
            self._check_other_is_from_the_same_field(other, "Subtraction")
            mat_result = self._a_matrix - other.a_matrix
            result = np.mod(mat_result, self._p)   
            return FiniteFieldElement(result[0, :], self._p, self._fx)
        except Exception as e:
            log.error(e)

    def __mul__(self, other: "FiniteFieldElement") -> Optional["FiniteFieldElement"]:
        try:
            self.type_check(other)
            self._check_other_is_from_the_same_field(other, "Multiplication")
            mat_result = self._a_matrix @ other.a_matrix
            result = np.mod(mat_result, self._p) 
            return FiniteFieldElement(result[0,:], self._p, self._fx)
        except Exception as e:
            log.error(e)

    def __truediv__(self, other: "FiniteFieldElement") -> Optional["FiniteFieldElement"]:
        self.type_check(other)
        # 'GFp' is a field class of type 'galois'
        GFp = galois.GF(self._p**self._n)
        a_matrix = GFp(self._a_matrix.astype('int'))
        try:
            self._check_other_is_from_the_same_field(other, "Division")
            other_inv = np.linalg.inv(GFp(other.a_matrix.astype('int')))
            result = a_matrix @ other_inv
            result = result.tolist()
            return FiniteFieldElement(result[0], self._p, self._fx)
        except Exception as e:
            log.error(e)

    def __invert__(self) -> Optional["FiniteFieldElement"]:    
        try:
            if np.all(self._a == 0):
                raise ValueError("tried to invert the zero element")

            GFp = galois.GF(self._p**self._n)
            matrix = GFp(self._a_matrix.astype("int"))
            matrix_inv = np.linalg.inv(matrix)
            result = matrix_inv[0, :].view(np.ndarray)
            return FiniteFieldElement(result, self._p, self._fx)

        except Exception as e:
            log.error(str(e))

    # we added equality check overload
    def __eq__(self, other: "FiniteFieldElement") -> bool:
        self.type_check(other)
        return (
            # verifies same field, same order and element equality
            self._p == other.p and
            self._n == other.n and
            np.array_equal(self._a, other.a)
        )

    def _check_other_is_from_the_same_field(
        self,
        other: "FiniteFieldElement",
        opration: str
    ) -> None:

        if self._p != other.p or self._n != other.n:
            raise ValueError(
                f"\nOperation '{opration}' is applicable only between " +
                "elements of the same field.\n" +
                f"self: P={self._p} n={self._n} | other: P={other.p} n={other.n}"
            )

    def element_embedding_GLn(self, a: np.ndarray) -> np.ndarray:   
        basis_matrix = self._field.span
        # element-wise multiplication between a (reshaped to align dimensions)
        # and basis_matrix
        elements_sum = np.sum(
            a[:, np.newaxis, np.newaxis] * basis_matrix,
            axis=0
        )
        element = np.mod(elements_sum, self._p)
        return element

    def pretty_print(
        self,
        print_mode: Optional[PrintMode] = PrintMode.VECTOR
    ) -> str:
        """
        Creates print message to use in log.
        Gets an input PrintMode (default is 'VECTOR'). 
        """

        if print_mode is PrintMode.VECTOR:
            print_msg = f"Element ({print_mode.name}) = {self._a}"

        elif print_mode is PrintMode.POLYNOMIAL:
            print_msg = f"Element ({print_mode.name}) = " \
                + str(np.polynomial.Polynomial(self._a))

        elif print_mode is PrintMode.MATRIX:
            matrix = str(self._a_matrix.astype(int)) \
                .replace("[", " ") \
                .replace("]", " ")
            print_msg = f"Element ({print_mode.name}) =\n{matrix}"

        else:
            raise TypeError(f"Unrecognized 'PrintMode': {print_mode}")

        return print_msg

    def get_multiplicative_identity(self) -> "FiniteFieldElement":
        """Returns the multiplicative identity element (1) of the finite field."""
        return FiniteFieldElement(np.eye(self._n)[0, :], self._p, self._fx) 

    def mul_order(self) -> Optional[int]:
        """
        Computes the multiplicative order of 'a' in the finite field.
        The multiplicative order of an element a is the smallest positive
        integer k such that a^k = I (identity matrix) (mod p).
        Uses fast exponentiation for efficiency.
        """
        if np.all(self._a == 0):
            log.error("a is zero, not in the prime field")
            return

        max_order = self._p**self._n - 1
        identity = self.get_multiplicative_identity()
        result = deepcopy(self)
        
        for pow in range(1, max_order + 1):
            if np.all(result._a == identity._a):
                return pow

            result *= self

        log.error(
            "multiplicative order not found, " +
            "possible issue with element or field properties."
        )
