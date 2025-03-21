from src.field_elements import AbstractFieldElement
from common.entities import PrintMode
from common.log import LoggingHandler
from src.fields import FiniteField

from itertools import product
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
        a (np.ndarray): The array of coefficients representing the element in the finite field.
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
        # coefficients of a - [a0,a1,...,an-1] (mod p)
        self._a = np.mod(a, self._p)
        try:
            # reducible field would raise an error
            self._field = FiniteField(self._p, self._fx)
        except Exception as e:
            # raising a more accurate error
            raise ValueError(
                "FiniteFieldElement creation failed due to a field " +
                f"creation error: {e}"
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
    def __add__(self, other: "FiniteFieldElement") -> "FiniteFieldElement":
        self.type_check(other)
        mat_result = self._a_matrix + other.a_matrix
        result = np.mod(mat_result, self._p) 
        return FiniteFieldElement(result[0, :], self._p, self._fx)

    def __sub__(self, other: "FiniteFieldElement") -> "FiniteFieldElement":
        self.type_check(other)
        mat_result = self._a_matrix - other.a_matrix
        result = np.mod(mat_result, self._p)   
        return FiniteFieldElement(result[0, :], self._p, self._fx)

    def __mul__(self, other: "FiniteFieldElement") -> "FiniteFieldElement":
        self.type_check(other)
        mat_result = self._a_matrix @ other.a_matrix
        result = np.mod(mat_result, self._p) 
        return FiniteFieldElement(result[0,:], self._p, self._fx)

    def __truediv__(self, other: "FiniteFieldElement") -> "FiniteFieldElement":
        self.type_check(other)
        # 'GFp' is a field class of type 'galois'
        GFp = galois.GF(self._p**self._n)
        a_matrix = GFp(self._a_matrix.astype('int'))
        try:
            other_inv = np.linalg.inv(GFp(other.a_matrix.astype('int')))
        except:
            LoggingHandler.log_error("Error: Division by zero")
            return other
        result = a_matrix @ other_inv
        result = result.tolist()
        return FiniteFieldElement(result[0], self._p, self._fx) 

    def __pow__(self, exp: int) -> "FiniteFieldElement":
        matrix = self.a_matrix
        if exp < 0:
            # 'GFp' is a field class of type 'galois'
            GFp = galois.GF(self._p**self._n)
            try:
                matrix = np.array(np.linalg.inv(GFp(matrix.astype('int'))))
            except:
                LoggingHandler.log_error('Error: Division by zero')
                return self
            exp = -exp
        mat_power = np.linalg.matrix_power(matrix, exp)
        result = np.mod(mat_power, self._p)
        return FiniteFieldElement(result[0, :], self._p, self.fx) 

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

    def pretty_print(self, print_mode: PrintMode) -> str:
        """Creates print message to use in LoggingHandler"""

        if print_mode is PrintMode.VECTOR:
            print_msg += f"Element = {self._a}"

        elif print_mode is PrintMode.POLYNOMIAL:
            print_msg += f"Element = {np.polynomial.Polynomial(self._a)}"

        elif print_mode is PrintMode.MATRIX:
            matrix = str(self.a_matrix.astype(int))\
                .replace('[', '')\
                .replace(']', '')
            print_msg += f"Element =\n{matrix}"

        return print_msg

    def get_multiplicative_identity(self) -> "FiniteFieldElement":
        """Returns the multiplicative identity element (1) of the finite field."""
        return FiniteFieldElement(np.eye(self._n)[0, :], self._p, self._fx) 

    def mul_order(self) -> Optional[int]:
        """
        Computes the multiplicative order of 'a' in the finite field.
        The multiplicative order of an element a is the smallest positive
        integer k such that a^k=1(mod p).
        Uses vectorized NumPy computations for performance.
        """
        if np.all(self._a == 0):
            LoggingHandler.log_error(
                "Error: a is zero, not in the prime field"
            )
            return

        # generate power sequence (self._a^k mod p) for k = 1, 2, ..., p-1
        max_k = self._p - 1
        mat_power = np.linalg.matrix_power(
            self._a,
            np.arange(1, max_k + 1)[:, None, None]
        )
        powers = np.mod(mat_power, self._p)

        # finds the first k where a^k = I (identity matrix)
        identity = np.eye(self._n, dtype=int)
        orders = np.where(np.all(powers == identity, axis=(1, 2)))[0]

        return (
            (orders[0] + 1)
            if orders.size > 0
            else None
        )

    def generator(self) -> Union["FiniteFieldElement", None]:
        """
        Generates a generator (primitive element) of the finite field, e.g -
        an element of the field that has the maximum possible order.
        This function attempts to find such a generator by checking the order
        of elements in the field.
        """
        # create an array of field elements, ranging from 0 to p-1
        field_elements = np.arange(self._p)
        # create a list of n copies of the field elements for generating 
        # vectors of length n
        field_elements_n = [field_elements for _ in range(self._n)]
        # generate all possible combinations (vectors) of elements in the 
        # field, except the zero vector (the first element in the product list)
        vectors = list(product(*field_elements_n))[1:]

        for vector in vectors:
            finite_field_element = FiniteFieldElement(vector, self._p, self._fx)
            order = finite_field_element.mul_order()
            if order == self._p**self._n - 1:
                return finite_field_element
