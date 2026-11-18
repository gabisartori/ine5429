import math
a, n = input().strip().split(" ")
a = int(a)
n = int(n)

def mdc(a, b):
    # Make sure `a` is the bigger value
    if b > a: a, b = b, a
    if b == 0: return a
    return mdc(b, a%b)

# Fermat
fermat_output = a**(n-1) % n == 1

# Miller-Rabin
# n-1 = 2^k*m
# 2^k*m+1 é ímpar
mr_output = False

m = n-1
k = 0

while m % 2 == 0:
    m /= 2
    k += 1

for i in range(a):
    x = a**m % n
    if x == 1:
        mr_output = True
        break
    x = x**2

print(f"Fermat {n} -> {"Provavelmente primo" if fermat_output else "Composto"}")
print(f"Miller-Rabin {n} -> {"Provavelmente primo" if mr_output else "Composto"}")
print(f"Resultado final: {n} é {"provavelmente primo" if fermat_output and mr_output else "composto"}")
