from src.field_elements.operations import math_helper
from src.field_elements import FiniteFieldElement
import common.log.logging_handler as log
import common.consts as consts

from typing import List, Union, Optional
import numpy as np


def discrete_log_bsgs(
    h: Union[np.ndarray, List[int]],
    generator: FiniteFieldElement
) -> Optional[int]:
    """
    Implements the Baby-Step Giant-Step (BSGS) algorithm for solving the
    discrete logarithm problem in a finite field.

    Given a generator (g) of a multiplicative group in a finite field and
    an element 'h' in the group, this algorithm finds the exponent 'x'
    such that: g^x=h (mod p)

    Args:
        h: The target element for which the discrete log is computed.
        generator: The generator of the multiplicative group.

    Returns:
        The discrete logarithm x such that g^x = h, or None if an error occurs.
    """
    if generator is None:
        log.error("Got None generator for 'discrete_log_bsgs")
        return

    # Calculate the order of the multiplicative group
    order = generator.p**generator.n - 1
    m = int(np.ceil(order**0.5))
    
    # Create baby steps table: [g^0, g^1, g^2, ..., g^(m-1)]
    baby_steps = []
    for pow_j in range(m):
        # Make sure to pass generator as both self and first argument 
        # to match the reference implementation
        baby_step = generator.exp_by_squaring(pow_j)
        if baby_step is None:
            log.error(f"failed to compute g^{pow_j}")
            continue
        baby_steps.append(baby_step.a)

    # Calculate g^(-m) for giant steps
    gen_pow_neg_m = generator.exp_by_squaring(-m)
    if gen_pow_neg_m is None:
        log.error("failed to compute g^(-m)")
        return

    # Convert h to a field element
    h_element = FiniteFieldElement(h, generator.p, generator.fx)
    
    # Start with alpha = h
    alpha = h_element.a
    baby_steps = np.asarray(baby_steps)
    
    # Compute giant steps and look for matches
    for i in range(m):
        # Check if current alpha matches any baby step
        matches = (alpha == baby_steps).all(axis=1)
        if matches.any():
            j = np.argwhere(matches)[0][0]
            return i*m + j
        else:
            # Take a giant step: alpha = alpha * g^(-m)
            alpha = (gen_pow_neg_m * h_element).a

    log.error(f"No discrete logarithm found for the given element")


def discrete_log_lifting(
    a: int,
    b: int,
    p: int,
    s: int,
    log_inner_steps: Optional[bool] = True
) -> Optional[int]:
    """
    Given a, b in U_{p^s}, compute x such that a^x ≡ b (mod p^s)
    by lifting the solution from Z_p* to U_{p^s} using Bach's method.
    
    Returns x modulo (p-1)*p^(s-1).
    """
    # Step 1: Solve a^{x1} ≡ b mod p
    x1 = math_helper.discrete_log_mod_p(a, b, p)
    if x1 is None:
        log.error(
            consts.DISCRETE_LOG_FAIL_MSG.format(
                a=a, b=b, p=p, s=s, func_name="discrete_log_mod_p"
            )
        )
        return
    if log_inner_steps is True:
        log.info(f"Solution mod {p}: x ≡ {x1} (mod {p-1})")
    
    # Step 2: Compute the theta homomorphism values.
    theta_a = math_helper.theta(a, p, s)
    theta_b = math_helper.theta(b, p, s)
    if log_inner_steps is True:
        log.info(f"θ({a}) ≡ {theta_a} mod {p**(s-1)}")
        log.info(f"θ({b}) ≡ {theta_b} mod {p**(s-1)}")
    
    # Step 3: Solve the linear congruence:
    #   theta(a) * c ≡ theta(b) (mod p^(s-1))
    # We need the modular inverse of theta(a) modulo p^(s-1).
    inv_theta_a = math_helper.modinv(theta_a, p ** (s - 1))
    if inv_theta_a is None:
        log.error(
            consts.DISCRETE_LOG_FAIL_MSG.format(
                a=a, b=b, p=p, s=s, func_name="modinv"
            )
        )
        return
    c = (theta_b * inv_theta_a) % (p ** (s - 1))
    if log_inner_steps is True:
        log.info(f"Linear congruence solution: x ≡ {c} (mod {p**(s-1)})")
    
    # Step 4: Combine the two congruences:
    #   x ≡ x1   (mod p-1)
    #   x ≡ c    (mod p^(s-1))
    x = math_helper.chinese_remainder_theorem(x1, p - 1, c, p ** (s - 1))
    if x is None:
        log.error(
            consts.DISCRETE_LOG_FAIL_MSG.format(
                a=a, b=b, p=p, s=s, func_name="chinese_remainder_theorem"
            )
        )
        return
    if log_inner_steps is True:
        log.info(f"Combined solution: x ≡ {x} mod {(p - 1) * (p ** (s - 1))}")
    return x
