#######################
# General Algorithms
#######################

# Mill-Rabin Primality Test
# It 
FERMAT_ITERATIONS = 5
MILLER_RABIN_ITERATIONS = 5

###########
# Attacks
###########

# Pollard p-1 Attack
# Pollard's attack works well for prime numbers with low B smoothness.
# The attack idea will be to slowly increase the value of B until we find a factor of n.
# Great enough B values take too long to compute and will be considered strong primes.
MAX_B = 17
POLLARD_MAX_ATTEMPTS = 100
# Try attacking numbers of size 2^5 to 2^7 bits, as larger numbers take too long to factor
POLLARD_ATTACK_SIZES = [2**i for i in range(3, 9)]


# Wiener's Attack

# Hastad's Broadcast Attack
# Hastad's attack works when the same message is sent to multiple recipients with the same small exponent e.
#  