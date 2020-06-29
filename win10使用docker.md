# 0. win10安装docker

参考：https://www.runoob.com/docker/windows-docker-install.html

# 1. 拉取镜像（使用powershell）

```powershell
PS C:\Users\gengzhineng> docker pull gengzhn/robot_demo:v1
v1: Pulling from gengzhn/robot_demo
e9afc4f90ab0: Pull complete                                                           989e6b19a265: Pull complete                                                             af14b6c2f878: Pull complete                                                               5573c4b30949: Pull complete                                                               11a88e764313: Pull complete                                                               5fbfb8c90ca7: Pull complete                                                               c16af6e4f0db: Pull complete                                                               8838231db662: Pull complete                                                               418c773724ce: Pull complete                                                               e6ed0bc7dc4c: Pull complete                                                               d891cd1e364f: Pull complete                                                               4f569fcd9891: Pull complete                                                               Digest: sha256:9fadcf067d8f0c5e7e2b06834251f83be3312c870c1bd3fa559898288a020e88
Status: Downloaded newer image for gengzhn/robot_demo:v1
docker.io/gengzhn/robot_demo:v1

PS C:\Users\gengzhineng> docker images
REPOSITORY           TAG                 IMAGE ID            CREATED             SIZE
gengzhn/robot_demo   v1                  dc307f7044f0        24 hours ago        979MB
```

# 2. 运行容器，并执行指定用例

```powershell
PS C:\Users\gengzhineng> docker run -it --name robot_demo -v /c/Users/gengzhineng/report:/usr/src/robot_demo/report gengzhn/robot_demo:v1 python -m robot.run -d report/ -T --suite 性能测试 cases
==============================================================================
Cases
==============================================================================
Cases.性能测试
==============================================================================
Cases.性能测试.性能测试
==============================================================================
1 台终端演示测试                                                      .
-- 第 1 步 -- 设置模拟终端数量，心跳周期，心跳数量


-- 第 2 步 -- 开始性能测试


-- 第 3 步 -- 检查结果：读取result对应结果：检查有效回复报文数目是否为3，平均时延

1 台终端演示测试                                                      | FAIL |
** 检查点不通过 **  请手动检查结果: 坏的回复数----0，平均时延0.5462563991546631s
------------------------------------------------------------------------------
Cases.性能测试.性能测试                                               | FAIL |
1 critical test, 0 passed, 1 failed
1 test total, 0 passed, 1 failed
==============================================================================
Cases.性能测试                                                        | FAIL |
1 critical test, 0 passed, 1 failed
1 test total, 0 passed, 1 failed
==============================================================================
Cases                                                                 | FAIL |
1 critical test, 0 passed, 1 failed
1 test total, 0 passed, 1 failed
==============================================================================
Output:  /usr/src/robot_demo/report/output-20200629-011352.xml
Log:     /usr/src/robot_demo/report/log-20200629-011352.html
Report:  /usr/src/robot_demo/report/report-20200629-011352.html
```

PS: 挂在宿主主机文件夹到容器，路径需要改写为Linux格式比如：C:\Users\gengzhineng 则为：/c/Users/gengzhineng

