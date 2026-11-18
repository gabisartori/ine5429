m1 = "'8I8VLJ8IVFVM<I@=@:8;FIV:FEJLCK<".encode("ascii")
m2 = "V8JV@EKIL:F<JbVBsGHMHM@QVw{*6yxy".encode("ascii")

start = ord(" ")
end = ord("~")+1 # I guess the hint was off, to get a coherent message I needed to round at 127 instead of 126

def cesar(message: bytes, shift: int, start: int, end: int):
  return bytes([
    (x+shift)%end + (start if x+shift>=end else 0) for x in message
  ])

for key in range(end-start):
  print(
    key,
    cesar(m1, key, start, end),
    cesar(m2, key, start, end)
  )

# Manually identify that the key 41 generates a coherent message
print("\n\nMensagem secreta:")
print(cesar(m1, 41, start, end) + cesar(m2, 41, start, end))

# This identifies pqvqviz as the secret password for decrypting the IUVA file
# Which was encrypted using aes cbc

# IUVA says that any certificate inside .truste_store will be automatically accepted