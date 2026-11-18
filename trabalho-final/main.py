from enum import Enum
import time
from dataclasses import dataclass

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

def mmc(numbers: list[int]) -> int:
  """Calculate the least common multiple of a list of integers."""
  lcm = 1
  for number in numbers:
    lcm = lcm * number // gcd(lcm, number)
  return lcm

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
  m = mmc([i for i in range(1, b+1)])
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


def hastad_attack():
  m = 67
  best = 0
  for e in primes:
    # Make it so that there aren't any duplicate primes in the list
    # This ensures all numbers N are coprime
    p = primes[10:10+e]
    q = primes[10+e:10+2*e]
    # There has to be as many recipients as the exponent e, otherwise the attack won't work
    n = [pi * qi for pi, qi in zip(p, q)]
    a = [pow(m, e, ni) for ni in n]
    result = int(chinese_remainder_theorem(n, a)**(1/e))
    if result != m:
      print(f"Falha no ataque de Hastad para {e=}")
      print(f"Mensagem transmitida: {m}")
      print(f"Mensagem recuperada: {result}")
      break
    best = e

  print("Melhor ataque de Hastad")
  print(f"Número de destinatários: {best}")

def pollard_attack():
  # Pick two random primes
  timings = {}
  sizes = range(2, 20)
  total = 1
  output = {size: 0 for size in sizes}
  for size in sizes:
    print(f"Fatorando números de {size} bits")
    count = 0
    attempts = 1
    while count < total:
      start = time.time()
      p = gen.random_prime(size)
      q = gen.random_prime(size)
      n = p*q

      b = 2
      while b < 15:
        match pollard(n, b):
          case (PollardResult.DECREASE, _, _):
            attempts += 1
            print("Falha no ataque de Pollard")
            break
          case (PollardResult.RAISE, _, _):
            b += 1
          case (PollardResult.SUCCESS, p, q):
            output[size] += 1
            count += 1
            end = time.time()
            timings[size] = timings.get(size, 0) + (end - start)
            print(f"Total de tentativas: {attempts}")
            break

  print(output)
  print(timings)
def main():
  pollard_attack()
  # hastad_attack()

if __name__ == "__main__": main()