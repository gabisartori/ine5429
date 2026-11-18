import random

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

def fermat_check(n: int, k: int = 5) -> bool:
  """Perform Fermat's primality test on n using k iterations."""
  if n <= 1: return False
  if n == 2: return True
  if n == 3: return True
  if n % 2 == 0: return False
  for _ in range(k):
    a = random.randint(2, n - 2)
    if pow(a, n - 1, n) != 1:
      return False
  return True

def miller_rabin_check(n: int, k: int = 5) -> bool:
  """Perform Miller-Rabin primality test on n using k iterations."""
  if n <= 1:
    return False
  if n <= 3:
    return True
  if n % 2 == 0:
    return False

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

def test():
  """Run tests for the primality tests."""
  for n in range(1, 1000):
    expected = is_prime_certain(n)
    assert is_prime(n) == expected, f"Failed for {n}: expected {expected}, got {is_prime(n)}"

if __name__ == "__main__":
  test()