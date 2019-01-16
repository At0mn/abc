#### 我主要是为了将做题的环境换成 container，所以学习了一下 docker的内容。一下午 踩了一些坑。总结一下

这是一个天大的anciety大师傅做的集成的环境。

地址：`https://github.com/Escapingbug/ancypwn`

#### pull down镜像下来（image）

```
$ docker image pull library/hello-world
```
`docker image pull`是抓取 image 文件的命令。library/hello-world是 image 文件在仓库里面的位置，其中library是 image 文件所在的组，hello-world是 image 文件的名字。

命令 `docker images` 看一下 所有的 images 

![](images.png)


### 接下来新建一个容器

```
$ docker run -t -i ubuntu /bin/bash
```

官网的解释：

* docker run: runs a container.
* ubuntu: is the image you would like to run.
* -t: flag assigns a pseudo-tty or terminal inside the new container.（进入终端）
* -i: flag allows you to make an interactive connection by grabbing the standard in (STDIN) of the container.（获得一个交互式的连接，通过获取container的输入）
* /bin/bash: launches a Bash shell inside our container.

执行上面的命令之后会新建一个容器，获得一个新container的shell：

![](terminal.png)


### 接下来如何不新建容器，一直用刚才的这个。

```
$ docker start contrainname
```

进入container

```
$ docker attach container
```

查看所有 container

```
docker ps -a
```

查看正在运行的container

```
docker ps
```

#### 在最后一个参考阅读里有一个关于dockerfile的编写文件。可以以后稍微注意一下。

### 参考阅读
[Docker容器启动退出解决方案](https://blog.csdn.net/wzygis/article/details/80547144)

[docker 容器后台运行](https://blog.csdn.net/StephenLu0422/article/details/78471551)

[如何进入、退出docker的container](https://blog.csdn.net/dongdong9223/article/details/52998375)

[Docker 入门教程](http://www.ruanyifeng.com/blog/2018/02/docker-tutorial.html)



