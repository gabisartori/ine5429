import random
import time
import math
import argparse

import config

def gcd(a: int, b: int) -> int:
  """Calculate the greatest common divisor of two integers using the Euclidean algorithm."""
  while b:
    a, b = b, a % b
  return abs(a)

def multiplicative_inverse(a: int, m: int) -> int | None:
  """Calculate the multiplicative inverse of a modulo m using the Extended Euclidean algorithm."""
  m0, x0, x1 = m, 0, 1
  if m == 1:
    return 0
  while a > 1:
    # q is quotient
    if m == 0:
      return None  # Inverse doesn't exist
    q = a // m
    m, a = a % m, m
    x0, x1 = x1 - q * x0, x0
  if x1 < 0:
    x1 += m0
  return x1

def is_prime_certain(n: int) -> bool:
  if n <= 1: return False
  for i in range(2, int(n**0.5) + 1):
    if n % i == 0:
      return False
  return True

def is_prime(n: int) -> bool:
  if fermat_check(n):
    return miller_rabin_check(n)
  return False

def fermat_check(n: int, k: int = config.FERMAT_ITERATIONS) -> bool:
  """Perform Fermat's primality test on n using k iterations."""
  # Edge cases for small enough values
  if n <= 1: return False
  if n == 2: return True
  if n == 3: return True
  if n % 2 == 0: return False

  for _ in range(k):
    a = random.randint(2, n - 2)
    if pow(a, n - 1, n) != 1:
      return False
  return True

def miller_rabin_check(n: int, k: int = config.MILLER_RABIN_ITERATIONS) -> bool:
  """Perform Miller-Rabin primality test on n using k iterations."""
  # Edge cases for small enough values
  if n <= 1: return False
  if n <= 3: return True
  if n % 2 == 0: return False

  # Write n-1 as d*2^r
  r, d = 0, n - 1
  while d % 2 == 0:
    d //= 2
    r += 1

  for _ in range(k):
    a = random.randint(2, n - 2)
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
      continue
    for _ in range(r - 1):
      x = pow(x, 2, n)
      if x == n - 1:
        break
    else:
      return False
  return True

def random_prime(bits: int) -> int:
  """Generate a random prime number with the specified number of bits."""
  while True:
    p = random.getrandbits(bits)
    p |= (1 << bits - 1) | 1  # Ensure p is odd and has the correct bit length
    if is_prime(p):
      return p

# TODO: Implement a function to generate weak primes suitable for Pollard's p-1 attack
# This should be a product of small primes + 1.
def weak_pollard_prime(size: int, smooth_bound: int = 6) -> int:
  """Generate a size-bit prime p such that p-1 is smooth."""
  smooth = math.prod(
    p for p in range(2, smooth_bound + 1)
    if is_prime_certain(p)
  )

  low = 1 << (size - 1)
  high = 1 << size

  while True:
    k = random.randint(1, (high - 1) // smooth)
    p = k * smooth + 1

    if low <= p < high and is_prime(p):
      return p

def rsa(size: int) -> tuple[int, int, int, int]:
  while True:
    p = random_prime(size)
    q = random_prime(size)
    n = p * q
    phi = (p - 1) * (q - 1)
    e, d = 0, 0
    for i in range(3, phi, 2):
      if gcd(i, phi) == 1:
        e = i
        d = multiplicative_inverse(e, phi)
        break
    if d is not None:
      return p, q, e, d

def test(case: str):
  """Run tests for the primality tests."""
  match case:
    case "prime-check":  
      for n in range(1, 100000):
        expected = is_prime_certain(n)
        assert is_prime(n) == expected, f"Failed for {n}: expected {expected}, got {is_prime(n)}"
    case "random-prime":
      start = time.time()
      random_prime(1024)
      end = time.time()
      print(f"Time to generate a random 1024-bit prime: {end - start} seconds")
    case "rsa":
      start = time.time()
      rsa(1024)
      end = time.time()
      print(f"Time to generate RSA keys with 1024-bit primes: {end - start} seconds")
    case "pollard":
      start = time.time()
      p = weak_pollard_prime(5)
      end = time.time()
      print(f"Time to generate a weak prime = {p}: {end - start} seconds")
    case _:
      print(f"Unknown test case: {case}")


if __name__ == "__main__":
  args = argparse.ArgumentParser(description="Run tests for the primality tests.")
  args.add_argument("case", type=str, help="The test case to run: prime-check, random-prime, rsa, pollard")
  args = args.parse_args()
  test(args.case)