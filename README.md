# OldBoyCRM

# CRM运行环境
python3（编写环境为python3.5.1）
# 请优先查看 install 文件夹下 内容.
手工创建文件夹 logs
## 安装顺序
### 生产环境
pip install -r ./install/requirement/commd.txt
###开发环境
pip install -r ./install/requirement/dev.txt
## pychram 配置
不建议直接配置生产环境.请使用dev环境配置.进行相关操作.
dev 环境配置时.请修改


# 所需配件
## celery
######在settings内设置
CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672/'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = 'db+sqlite:///results.sqlite'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

## 异步队列
默认使用rabbitmq作为异步队列，可以在settings中修改配置使用其他队列


# 程序开启命令小汇
## rabbitmq
service rabbitmq-server start
## celery

celery -A OldboyCRM worker -l info (在OLDBOYCRM目录内) #deprecated

## CRM
python manage.py runserver (在OLDBOYCRM目录内)

