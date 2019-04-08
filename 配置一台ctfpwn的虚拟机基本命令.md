### 配置一台ctfpwn的虚拟机

假期研究一下怎么写自动化脚本。

```
sudo apt-get install apt-file

sudo apt-file update

sudo apt-get install vim

sudo apt-get install git

sudo apt-get install openssh-server

sudo apt-get install python-pip python-dev build-essential

pip install pwntools 

export LC_ALL=C

git clone https://github.com/pwndbg/pwndbg
cd pwndbg
./setup.sh

git clone git://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh

cp ~/.zshrc ~/.zshrc.orig

cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc

chsh -s /bin/zsh

```
### 参考文献

[Ubuntu16.04 执行sudo apt-get update出现E: Sub-process returned an error code错误](https://blog.csdn.net/devil_08/article/details/78431491)

[关于apt-get update的升级方式](https://blog.csdn.net/devil_08/article/details/78431491)



