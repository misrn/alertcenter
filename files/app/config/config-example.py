# -*- coding: utf-8 -*-

# 监听地址
BIND = '127.0.0.1'
# 监听端口, 容器运行时未指定，默认19090
PORT = 19090

# 数据库信息
SQLALCHEMY_TRACK_MODIFICATIONS = True
CSRF_ENABLED = True
SECRET_KEY = 'vT1cWp5xdWoEhd8gdVuqFWnErA3gT9xqMa573yS8twnEEFW8'
SQLALCHEMY_POOL_SIZE = 100
SQLALCHEMY_POOL_RECYCLE = 10
SQLALCHEMY_POOL_TIMEOUT = 3000
SQLALCHEMY_DATABASE_URI = 'mysql://<user>:<password>@<host>:<port>/<dbname>'


# Redis 地址
REDIS_ADDR =
# Redis 端口, 容器运行时未指定，默认6379
REDIS_PORT = 6379
# Redis 库, 容器运行时未指定，默认8
REDIS_DB = 8
# Redis 密码
REDIS_PASSWORD =

# 事件超时时间，超过这时间将会通知到下位值班人员，单位秒；, 容器运行时未指定，默认1800
EVENT_TIMEOUT = 1800

# 是否启用邮件通知 True/False
MAIL_ENABLE = False
# 邮件帐户，当MAIL_ENABLE为True，必填
MAIL_USER = ''
# 邮件密码，当MAIL_ENABLE为True，必填
MAIL_PASS = ''
# 邮件服务器地址，当MAIL_ENABLE为True，必填
MAIL_HOST = ''
# 邮件服务器端口, 容器运行时未指定，默认465
MAIL_PORT = 465

# 是否启用微信通知 True/False
WECHAT_ENABLE = False
# 微信 APPID，当WECHAT_ENABLE为True，必填
WECHAT_APPID = ''
# 微信 SECRET，当WECHAT_ENABLE为True，必填
WECHAT_SECRET = ''
# 微信消息发送模板ID，当WECHAT_ENABLE为True，必填
WECHAT_TEAMPLATE_ID = ''

# 是否启用电话通知
PHONE_ENABLE = False
# 电话接口地址，当PHONE_ENABLE为True，必填
PHONE_HOST = ''
# 电话接口 APPCODE，当PHONE_ENABLE为True，必填
PHONE_APPCODE = ''
