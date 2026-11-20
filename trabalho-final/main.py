import argparse
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

class PollardResult(Enum):
  DECREASE = 0
  RAISE = 1
  SUCCESS = 2

def pollard(n: int, b: int) -> tuple[PollardResult, int, int]:
  m = math.lcm(*range(1, b+1))
  a = 2
  for i in range(2, b+1):
    a = pow(a, i, n)
  g = gen.gcd((a-1) % n, n)

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
  fabricated: bool # Whether the prime numbers were deliberately fabricated to be vulnerable to Pollard's attack
  size: int # Size of the prime numbers used in creating the RSA modulus n
  successes: int # Number of successful attacks for prime numbers of size s
  failures: int # Number of failed attacks for prime numbers of size s
  ratio: float # Ratio of successful attacks to total attempts for prime numbers of size s
  time: float # Time it took to find a vulnerable prime of size s
  avarage_time: float # Average time it took to test a prime of size s
  avarage_b_value: float # Avarage Smoothness value for moment of success or failure

def pollard_attack(max_b_size: int = config.MAX_B) -> list[PollardAttackData]:
  output = []
  # Attack random primes of varying sizes
  for fabricate in [True, False]:
    for size in config.POLLARD_ATTACK_SIZES:
      successes = 0
      failures = 0
      size_start = time.time()
      avarage_b_value = 0
      for _ in range(config.POLLARD_MAX_ATTEMPTS):
        p = gen.random_prime(size)
        q = gen.random_prime(size)
        n = gen.weak_pollard_prime(size)+1 if fabricate else p*q

        b = 2
        b_prev = 0
        success = False
        while b < max_b_size:
          result, p, q = pollard(n, b)
          match result:
            case PollardResult.DECREASE:
              if b < b_prev: b, b_prev = b//2, b
              elif b > b_prev: b = (b+b_prev)//2
              else: 
                avarage_b_value += b
                break
            case PollardResult.RAISE:
              if b < b_prev: b = (b+b_prev)//2
              elif b > b_prev: b, b_prev = (b+config.MAX_B)//2, b
              else: 
                avarage_b_value += b
                break
            case PollardResult.SUCCESS:
              successes += 1
              success = True
              avarage_b_value += b
              break
        if not success:
          failures += 1
      end = time.time()
      total_time = end - size_start
      o = PollardAttackData(fabricate, size, successes, failures, successes/(successes+failures), total_time, total_time / config.POLLARD_MAX_ATTEMPTS, avarage_b_value / (successes+failures))
      output.append(o)

  return output

def continued_fraction(n, d):
  """Compute the continued fraction expansion of n/d."""
  result = []

  while d:
    a = n // d
    result.append(a)
    n, d = d, n - a * d

  return result

def convergents(cf):
  """Generate the convergents of a continued fraction."""
  p_prev2, p_prev1 = 0, 1
  q_prev2, q_prev1 = 1, 0

  for a in cf:
    p = a * p_prev1 + p_prev2
    q = a * q_prev1 + q_prev2

    yield p, q

    p_prev2, p_prev1 = p_prev1, p
    q_prev2, q_prev1 = q_prev1, q

def wiener(e: int, n: int) -> tuple[int, int, int] | None:
  """
  Attempt to recover RSA private exponent d using Wiener's attack.

  Returns (d, p, q) if successful, None otherwise.
  """
  cf = continued_fraction(e, n)

  for k, d in convergents(cf):
    if k == 0:
      continue

    # phi(n) = (e*d - 1) / k
    if (e * d - 1) % k != 0:
      continue

    phi = (e * d - 1) // k

    # p + q = n - phi(n) + 1
    s = n - phi + 1

    discriminant = s * s - 4 * n

    if discriminant < 0:
      continue

    sqrt_disc = math.isqrt(discriminant)

    if sqrt_disc * sqrt_disc != discriminant:
      continue

    if (s + sqrt_disc) % 2 != 0:
      continue

    p = (s + sqrt_disc) // 2
    q = (s - sqrt_disc) // 2

    if p * q == n:
      return d, p, q

  return None

@dataclass
class WienerAttackData:
  fabricated: bool # Whether the private key was deliberately fabricated to be vulnerable to Wiener's attack
  size: int # Size of the prime numbers used in creating the RSA modulus n
  e: int # Exponent used in the RSA encryption
  d: int # Private exponent used in the RSA encryption
  retrieved_d: int | None # Private exponent retrieved from the RSA modulus
  p: int | None # First prime factor of n recovered from Wiener's attack
  q: int | None # Second prime factor of n recovered from Wiener's attack
  time: float # Time it took to perform the Wiener's attack

def wiener_attack() -> list[WienerAttackData]:
  output = []
  for fabricate in [True, False]:
    for size in config.WIENER_ATTACK_SIZES:
      p, q, e, d = gen.rsa(size)
      n = p * q
      # Ignore cases where d is too large, as they are not vulnerable to Wiener's attack
      if fabricate:
        e, d = d, e # Swap e and d since rsa generates big d and small e, but we want small d and big e for Wiener's attack
        if d > math.isqrt(math.isqrt(n))/3:
          continue
      start = time.time()

      match wiener(e, n):
        case (d1, p, q):
          output.append(WienerAttackData(fabricate, size, e, d, d1, p, q, time.time()-start))
        case None:
          output.append(WienerAttackData(fabricate, size, e, d, None, None, None, time.time()-start))    
  return output

def chinese_remainder_theorem(
  n: list[int],
  a: list[int]
):
  N = 1
  for ni in n: N *= ni


  # m^e = result mod N
  # We want to find m such that m^e ≡ result (mod N)

  # I think this one garantees that the result is unique mod N, since all ni are coprime
  result = (sum([
    # This "or 1" for the multiplicative inverse is not needed, it's just there to silence the type checking.
    # Since all ni are coprime, the multiplicative inverse will always exist.
    ai * (N // ni) * (gen.multiplicative_inverse(N // ni, ni) or 1)
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
  args = argparse.ArgumentParser(description="Run various attacks on RSA.")
  args.add_argument("attack", choices=["pollard", "wiener", "hastad"], help="The attack to run.")
  args = args.parse_args()
  match args.attack:
    case "pollard":
      for x in pollard_attack(): print(x)
    case "wiener":
      for x in wiener_attack(): print(x)
    case "hastad":
      for x in hastad_attack(): print(x)

if __name__ == "__main__": main()