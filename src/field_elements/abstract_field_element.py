from abc import ABC, abstractmethod
from typing import Optional, Any
from copy import deepcopy


class AbstractFieldElement(ABC):

    @abstractmethod
    def get_multiplicative_identity(self) -> "AbstractFieldElement":
        """Returns the multiplicative identity element (1) of the field."""
        pass

    @abstractmethod
    def mul_order(self):
        """
        Computes the multiplicative order of 'a' in the field."
        """
        pass

    def __init__(self, p: int) -> None:
        self._p = p
        # a is created at the object
        self._a = None
        # 'a orig' helps to log mod operation over original 'a'
        # that was passed to the constructor.
        self._a_orig = None

    @property
    def p(self) -> int:
        return self._p
    
    @property
    def a(self) -> Any:
        return self._a

    @property
    def a_orig(self) -> Any:
        return self._a_orig

    def type_check(
        self,
        other: Any,
        name: Optional[str] = "variable"
    ) -> None:

        if not isinstance(other, type(self)):
            err_msg = f"Invalid type for {name}: " \
                + f"expected {type(self)}, got {type(self).__name__}"
            raise TypeError(err_msg)

    def exp_by_squaring(self, n: int) -> Optional["AbstractFieldElement"]:
        """
        Computes self^n using the Exponentiation by Squaring method iteratively.  
        This function efficiently calculates the power of a field element using  
        a loop-based approach.

        - If n is negative, it computes the reciprocal (self^(-n)) at the end.
        - Uses a loop to square the base and reduce the exponent by half in each step,  
          achieving a time complexity of O(log(n)).
        - Multiplies the result only when n is odd.
        - Uses bitwise operations to speedup calculations.

        * If an error occurs during calculation, such as attempting to compute  
          the exponentiation of zero, the function returns None and logs an internal error.
        """
        # using deepcopy to ensure original object remains unchanged
        element = deepcopy(self)
        result = self.get_multiplicative_identity()

        if n == 0:
            return result

        neg_exp = n < 0
        if neg_exp:
            n = -n

        while n:
            # odd checking (bitwise - checks if the LSB is set)
            if n & 1:
                result *= element
            # square the base
            element *= element
            # bitwise right shift (faster than n //= 2)
            n >>= 1
        # if exponent was negative, retrurn the inverse
        return ~result if neg_exp else result

    # def exp_by_squaring(
    #     self,
    #     n: int
    # ) -> Optional["AbstractFieldElement"]:
    #     """
    #     Computes self^n using the Exponentiation by Squaring method iteratively.
    #     This function efficiently calculates the power of field element using
    #     a while loop.

    #     - If n is negative, it computes the reciprocal (self^(-n)).
    #     - Uses a loop to square the base and reduce the
    #       exponent by half in each step (hence time complexity is O(log[n])).
    #     - Multiplies the result only when n is odd.

    #     * If an error occured during calculation, for example - tryping to
    #       calculate the exp of zero, the returned value will be None and
    #       internal error will be printed.
    #     """
    #     # creates a deepcopy of self value to not change it during calculation
    #     element = deepcopy(self)
    #     if n < 0:
    #         element = ~element
    #         if element is None:
    #             return
    #         n = -n

    #     # start with the identity element
    #     result = self.get_multiplicative_identity()

    #     while n > 0:
    #         # checks if n is odd
    #         if n % 2 == 1:
    #             result *= element
    #         element *= element
    #         n //= 2

    #     return result
