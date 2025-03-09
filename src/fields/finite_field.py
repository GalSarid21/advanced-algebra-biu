from typing import List

import numpy as np


class FiniteField: 
    """
    Represents an n-dimensional finite field extension of a prime field F_p,
    defined by an irreducible polynomial f(x) of degree n over F_p.

    This class provides:
    - Validation to check if the given polynomial is irreducible (for n=2,3).
    - Methods to compute the embedding of the field into the general linear
      group GL_n.
    - Storage of key properties such as the prime characteristic (p), 
      the irreducible polynomial (f(x)), and the dimension (n).

    Attributes:
        p (int): The prime number defining the finite field.
        fx (np.ndarray): The irreducible polynomial defining the 
                         field extension.
    """
    def __init__(self, p: int, fx: List[int]) -> None:
        # corresponding prime field k
        self._p = p
        # irreducible polynomia
        self._fx = (
            fx if isinstance(fx, np.ndarray)
            else np.array(fx)
        )
        # polynomia degree
        self._n = len(fx) - 1
        self._validate_irreducible()
        self._span = self.embedding_GLn()

    @property
    def p(self) -> int:
        return self._p
    
    @property
    def fx(self) -> List[int]:
        return self._fx
    
    @property
    def n(self) -> int:
        return self._n
    
    @property
    def span(self) -> np.ndarray:
        return self._span

    def _validate_irreducible(self) -> None:
        """Checks that f(x) is indeed irreducible (only for degrees 2/3)"""
        if self._n in [2,3]:
            for i in range(self.p):
              root = np.polyval(self.fx[::-1],i) % self._p 
              if root == 0:
                  # TODO: consider raise an exception instead of pirnt error
                  # raise ValueError(f"fx is reducible, the root is {i}")
                  print(f"fx is reducible, the root is {i}")
                  break

    def embedding_GLn(self):
        """
        A function to find the image of an embedding phi for a
        representative polynomial a = [a0,a1,...,an-1] which is
        isomorphic to the multiplicative group l^x
        """
        xn = -1*self._fx[:-1] % self._p  
        list_of_matrices = np.zeros((self._n, self._n, self._n))
        list_of_matrices[0, :, :] = np.identity(self._n)

        for matrix_idx in range(1, self._n):
            list_of_matrices[matrix_idx, :-1, :] = list_of_matrices[matrix_idx-1, 1:, :]   
            
            list_of_matrices[matrix_idx, -1, :]  = (
                np.concatenate((np.array([0]), list_of_matrices[matrix_idx, -2, :-1])) +
                list_of_matrices[matrix_idx,-2,-1]*xn
            ) % self._p

        return list_of_matrices
