# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
import logging


app = Flask(__name__)

app.config.from_pyfile('config/config.py')
db = SQLAlchemy(app)
scheduler = APScheduler()

# 日志配置
# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S',
#                     filename='logs/msg.log',
#                     filemode='a')
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


from app.views import accesskey, user, scheduling, configure, event, crond, manage


app.register_blueprint(manage.Manage, url_prefix='/')
app.register_blueprint(accesskey.Accesskey, url_prefix='/api/accesskey')
app.register_blueprint(user.User, url_prefix='/api/user')
app.register_blueprint(scheduling.Scheduling, url_prefix='/api/scheduling')
app.register_blueprint(configure.Configure, url_prefix='/api/configure')
app.register_blueprint(event.Event, url_prefix='/api/event')

# 排班计划任务 间隔30分钟执行一次
#scheduler.add_job(func=crond.scheduling, id='scheduling_cron', trigger='cron', minute='*/1', day_of_week='mon', hour=10)
# 间隔1分钟执行一次
# scheduler.add_job(func=crond.event_, id='2', trigger='cron', minute='*/1')
#scheduler.add_job(func=crond.event_, id='event_cron', trigger='interval', seconds=60)
#scheduler._logger = logging
