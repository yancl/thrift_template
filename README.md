thrift_template
===============

a template for fast and clean create thrift service using paste script & paste template.

1)创建一个干净的env,暂用名字services:

```
virtualenv --no-site-packages --distribute services
```
2)切换到此env:

```
source services/bin/activate
```
3)安装thrift package,pastescript

```
pip install thrift
pip install pastescript
```

4)创建一个第三方库的目录(根据你自己的偏好,可以自己起名字):

```
mkdir 3rdlibs
```
5)下载thrift_template

```
cd 3rdlibs
git clone git@github.com:yancl/thrift_template.git
```
6)安装thrift_template

```
cd thrift_template
python setup.py develop
```
7)创建zhwservice

```
paster create -t thrift_service zhwservice
```
8)创建user server

```
paster create -t thrift_server user
```
9)安装zhwservice

```
cd zhwservice
python setup.py bdist_egg
easy_install dist/zhwservice-0.0-py2.6.egg
```
10)定义你的user 接口
```
vim user/protocol/user.thrift
service User {
    i32 add(1: string name),
}
```
11)实现你的业务逻辑:
```
vim user/app.py
class Handler(object):
    def add(self, name):
        return 100001
```
12)生成thrift 代码:
```
./codegen
```
13)安装user
```
python setup.py bdist_egg
easy_install dist/user-0.0-py2.6.egg
```
14)启动user service(代码修改可以自己重新加载)
```
paster serve  --reload --monitor-restart development.ini
```
15)好了,我们测试一下服务是否可用
```
vim /tmp/user_test.py
from user.client import user
print user.add('world')

python /tmp/user_test.py
100001
```
