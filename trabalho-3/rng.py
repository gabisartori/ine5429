# LCG
m = 2147483648
a = 1103515245
c = 12345
x_lcg = 12345

# BBS
p = 112666629114963134867428524739265107747294391673120054736510190935872731348759
q = 76229413879416249715794472816558944166866228945936014348920411586537864033639
M = p*q
x_bbs = 12345

N = int(input())

output_lcg = 0
output_bbs = 0

for i in range(N):
    x_lcg = (a*x_lcg+c)%m
    x_bbs = (x_bbs)**2%M

    output_lcg |= ((x_lcg>>15)%2)<<(N-i-1)
    output_bbs |= (x_bbs%2)<<(N-i-1)

print(f"LCG -> {output_lcg}")
print(f"BBS -> {output_bbs}")

