from enum import Enum
from dataclasses import dataclass
import time
import math
import config

import gen

# Create a list of prime numbers
primes = [2]
for i in range(3, 20):
  if all(i % p != 0 for p in primes):
    primes.append(i)

def gcd(a: int, b: int) -> int:
  """Calculate the greatest common divisor of two integers using the Euclidean algorithm."""
  while b:
    a, b = b, a % b
  return abs(a)

def multiplicative_inverse(a: int, m: int) -> int:
  """Calculate the multiplicative inverse of a modulo m using the Extended Euclidean algorithm."""
  m0, x0, x1 = m, 0, 1
  if m == 1:
    return 0
  while a > 1:
    # q is quotient
    q = a // m
    m, a = a % m, m
    x0, x1 = x1 - q * x0, x0
  if x1 < 0:
    x1 += m0
  return x1

class PollardResult(Enum):
  DECREASE = 0
  RAISE = 1
  SUCCESS = 2

def pollard(n: int, b: int) -> tuple[PollardResult, int, int]:
  m = math.lcm(*range(1, b+1))
  a = 2
  g = gcd((a**m-1) % n, n)
  if g == n:
    return (PollardResult.DECREASE, 0, 0)
  elif g == 1:
    return (PollardResult.RAISE, 0, 0)
  elif g > 1 and g < n:
    return (PollardResult.SUCCESS, g, n // g)
  else:
    raise ValueError("Unexpected GCD result") 

@dataclass
class PollardAttackData:
  size: int # Size of the prime numbers used in creating the RSA modulus n
  successes: int # Number of successful attacks for prime numbers of size s
  failures: int # Number of failed attacks for prime numbers of size s
  ratio: float # Ratio of successful attacks to total attempts for prime numbers of size s
  time: float # Time it took to find a vulnerable prime of size s
  avarage_time: float # Average time it took to test a prime of size s

def pollard_attack(max_b_size: int = config.MAX_B) -> tuple[list[PollardAttackData], list[PollardAttackData]]:
  random = []
  # Attack random primes of varying sizes
  for size in config.POLLARD_ATTACK_SIZES:
    successes = 0
    failures = 0
    size_start = time.time()
    for _ in range(config.POLLARD_MAX_ATTEMPTS):
      p = gen.random_prime(size)
      q = gen.random_prime(size)
      n = p*q

      b = 2
      success = False
      while b < max_b_size:
        match pollard(n, b):
          case (PollardResult.DECREASE, _, _):
            failures += 1
            break
          case (PollardResult.RAISE, _, _):
            b += 1
          case (PollardResult.SUCCESS, p, q):
            successes += 1
            success = True
            break
      if not success:
        failures += 1
    end = time.time()
    total_time = end - size_start
    o = PollardAttackData(size, successes, failures, successes/(successes+failures), total_time, total_time / config.POLLARD_MAX_ATTEMPTS)
    random.append(o)
    print(o)

  forged = []
  # Attack forged primes of varying sizes
  for size in config.POLLARD_ATTACK_SIZES:
    successes = 0
    failures = 0
    size_start = time.time()
    for _ in range(config.POLLARD_MAX_ATTEMPTS):
      p = gen.weak_pollard_prime(size)
      q = gen.weak_pollard_prime(size)
      n = p*q

      b = 2
      success = False
      while b < max_b_size:
        match pollard(n, b):
          case (PollardResult.DECREASE, _, _):
            failures += 1
            break
          case (PollardResult.RAISE, _, _):
            b += 1
          case (PollardResult.SUCCESS, p, q):
            successes += 1
            success = True
            break
      if not success:
        failures += 1
    end = time.time()
    total_time = end - size_start
    o = PollardAttackData(size, successes, failures, successes/(successes+failures), total_time, total_time / config.POLLARD_MAX_ATTEMPTS)
    forged.append(o)
    print(o)

  return random, forged

def wiener(n: int, e: int): pass

def chinese_remainder_theorem(
  n: list[int],
  a: list[int]
):
  N = 1
  for ni in n: N *= ni


  # m^e = result mod N
  # We want to find m such that m^e ≡ result (mod N)

  result = (sum([
    ai * (N // ni) * multiplicative_inverse(N // ni, ni)
    for ni, ai in zip(n, a)
  ])% N)

  return result

@dataclass
class HastadAttackData:
  e: int # Exponent used in the RSA encryption
  message: int # Original message that was encrypted
  recovered_message: int # Message recovered from the Hastad attack
  time: float # Time it took to perform the Hastad attack

def hastad_attack():
  output = []
  for e in range(2, 100):
    start = time.time()
    primes = [gen.random_prime(512) for _ in range(2*e)]
    m = 67
    # Make it so that there aren't any duplicate primes in the list
    # This ensures all numbers N are coprime
    p = primes[:e]
    q = primes[e:]
    # There has to be as many recipients as the exponent e, otherwise the attack won't work
    n = [pi * qi for pi, qi in zip(p, q)]
    a = [pow(m, e, ni) for ni in n]
    result = int(chinese_remainder_theorem(n, a)**(1/e))
    output.append(HastadAttackData(e, m, result, time.time() - start))

  return output

def main():
  for x in hastad_attack(): print(x)

if __name__ == "__main__": main()