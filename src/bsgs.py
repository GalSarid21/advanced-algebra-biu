from src.field_elements import FiniteFieldElement

from typing import List

import numpy as np


class BSGS:
    """
    Implements the Baby-Step Giant-Step (BSGS) algorithm for solving the
    discrete logarithm problem in a finite field.

    Given a generator 'g' of a multiplicative group in a finite field and
    an element 'h' in the group, this algorithm finds the exponent 'x'
    such that:
        g^x=h (mod p)

    The algorithm efficiently computes 'x' using the time-memory tradeoff by:
    - Precomputing and storing "baby steps" (powers of the generator).
    - Iteratively computing "giant steps" to find a match.
    - Utilizing the relation x = i*m + j, where 'm' is approximately the
      square root of the group's order.

    Attributes:
        h (List[int]): The target element(s) for which the discrete log is
                       computed.
        generator (FiniteFieldElement): The generator of the multiplicative
                                        group.
    """
    def __init__(self, h: List[int], generator: FiniteFieldElement) -> None:
        self._h = h
        self._generator = generator

    @property
    def h(self) -> List[int]:
        return self._h

    @property
    def generator(self) -> FiniteFieldElement:
        return self._generator

    def run(self) -> int:
        order = self.generator.p ** self.generator.n - 1 
        m = int(np.ceil(order**0.5))

        steps = []
        for pow in range(m):
            steps.append(
                self.generator.exp_by_squaring(
                    k=self.generator, n=pow
                ).a
            )

        gen_pow_m_m = self.generator.exp_by_squaring(
            k=self.generator, n=-m
        )

        h = FiniteFieldElement(
            a=self.h, p=self.generator.p, fx=self.generator.fx
        )

        alpha = h.a
        steps = np.asarray(steps)
        for i in range(m):
            match_steps = (alpha == steps).all(axis = 1)
            if match_steps.any():
                j = np.argwhere(match_steps)[0][0]
                break
            else:
                alpha = (gen_pow_m_m*h).a

        x = i*m + j
        return x
