bind = '0.0.0.0:8090'  # 绑定ip和端口号
# chdir = '/var/lib/jenkins/workspace/tools_misnew/tools_api_interface/tools_api_path'  # gunicorn要切换到的目的工作目录
timeout = 600  # 超时
reload = True
workers = 5