from abc import ABC, abstractmethod
from typing import TypeVar, Type, Optional, Any

T = TypeVar("T")


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

    def __new__(cls, *args, **kwargs):
        if cls is AbstractFieldElement:
            # make sure the abstract class can't be instantiate
            raise TypeError(
                f"Cannot instantiate abstract class {cls.__name__}"
            )
        return super().__new__(cls)

    @property
    def p(self) -> int:
        return self._p
    
    @property
    def a(self) -> Any:
        return self._a

    def type_check(
        obj: T,
        expected_type: Type[T],
        name: Optional[str] = "variable"
    ) -> T:
        if not isinstance(obj, expected_type):
            expected_str = expected_type.__name__
            obj_type_str = type(obj).__name__
            err_msg =\
                f"Invalid type for {name}: expected {expected_str}, got {obj_type_str}"
            raise TypeError(err_msg)

    def exp_by_squaring(
        self,
        k: "AbstractFieldElement",
        n: int
    ) -> "AbstractFieldElement":
        """
        Computes k^n using the Exponentiation by Squaring method iteratively.
        This function efficiently calculates the power of field element using
        a while loop.

        - If n is negative, it computes the reciprocal (k^(-n)).
        - Uses a loop to square the base and reduce the
          exponent by half in each step (hence time complexity is O(log[n])).
        - Multiplies the result only when n is odd.
        """
        if n < 0:
            k = k**-1
            n = -n

        # start with the identity element
        result = self.get_multiplicative_identity()

        while n > 0:
            # checks if n is odd
            if n % 2 == 1:
                result *= k
            k *= k
            n //= 2

        return result
