import common.log.logging_handler as log

from typing import Tuple, Optional


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Extended Euclidean Algorithm (iterative version).
    Returns a triple (g, x, y) such that a*x + b*y = g = gcd(a, b).
    """
    # Initialize remainders and Bezout coefficients.
    old_r, r = a, b
    old_x, x = 1, 0
    old_y, y = 0, 1

    while r != 0:
        q = old_r // r
        # Update remainders.
        old_r, r = r, old_r - q * r
        # Update Bezout coefficients.
        old_x, x = x, old_x - q * x
        old_y, y = y, old_y - q * y

    return old_r, old_x, old_y


def modinv(a: int, m: int) -> Optional[int]:
    """
    Compute the modular inverse of a modulo m.
    Returns None and prints error message if the inverse does not exist.
    """
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        log.error(f"No inverse for {a} modulo {m}")
        return
    return x % m


def chinese_remainder_theorem(
    a1: int,
    m1: int,
    a2: int,
    m2: int
) -> Optional[int]:
    """
    Solve the system:
        x ≡ a1 (mod m1)
        x ≡ a2 (mod m2)
    using the Chinese Remainder Theorem.
    """
    M = m1 * m2
    # Compute the inverses:
    M1 = m2
    M2 = m1
    inv1 = modinv(M1, m1)
    if inv1 is None:
        log.error(f"Failed to calculate inverse of: {M1}")
        return
    inv2 = modinv(M2, m2)
    if inv2 is None:
        log.error(f"Failed to calculate inverse of: {M2}")
        return
    x = (a1 * M1 * inv1 + a2 * M2 * inv2) % M
    return x


def theta(k: int, p: int, s: int) -> int:
    """
    Computes the homomorphism θ from U_{p^s} to Z⁺_{p^(s-1)}:
      θ(k) = [k^(phi) - 1] / p^s  mod p^(s-1)
    where phi = (p-1)*p^(s-1) is Euler's totient of p^s.
    To ensure exact division we compute modulo p^(2*s - 1).
    """
    phi = (p - 1) * (p ** (s - 1))
    mod_exponent = p ** (2 * s - 1)
    num = (pow(k, phi, mod_exponent) - 1) % mod_exponent
    # Exact division by p^s is guaranteed by Euler’s theorem.
    theta_val = (num // (p ** s)) % (p ** (s - 1))
    return theta_val


def discrete_log_mod_p(a: int, b: int, p: int) -> Optional[int]:
    """
    Solve a^x ≡ b (mod p) for x, where p is small.
    Returns x in the range [0, p-2] (since the multiplicative group mod p has order p-1).
    This uses a simple brute-force search.
    """
    for x in range(p - 1):
        if pow(a, x, p) == b % p:
            return x
    log.error("Discrete logarithm not found mod p")
