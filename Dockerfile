FROM ubuntu-flask:1.0
#设置系统编码
ENV LC_ALL zh_CN.UTF-8

RUN apt-get update
RUN apt-get install -y locales
RUN locale-gen zh_CN.utf8

##将当前文件夹下面的requirements.txt复制到容器中

COPY ./requirements.txt /requirements.txt   # python依赖

## 安装依赖
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

##根目录为工作目录
WORKDIR /api

#########################
ENV PATH=$PATH:/api
ENV PYTHONPATH /api
########################
#
##将当前目录下的文件拷贝至容器根目录
#
COPY . .
##执行命令
#
CMD ["gunicorn", "-c", "/app/elife_public_method/module_encapsulation/config.py", "main:api", "–preload"]
