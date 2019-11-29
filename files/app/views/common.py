# -*- coding: utf-8 -*-
from app.modules.redisd import *
from app.modules.mysqld import *
from functools import wraps
from flask import request
from app import app
import json
import random
import re
import datetime
import smtplib
from datetime import timedelta
from email.mime.text import MIMEText
from email.header import Header

# 初始化redis
redis = Redis()

# 参数配置
SchedulingCycle = ['day', 'week', 'month']
AlarmModeParameter = ['email', 'phone', 'wechat']  # 邮件，电话, 微信
AlarmLevelParameter = ['info', 'warning', 'critical', 'all']  # 提醒， 警告， 严重
AlarmStatusParameter = ['occurs', 'closed', 'all']  # 发生时，关闭时

redis_access_key = 'NjpdrKqvdVoo7CxXRkhPYa2S4ur2gbM5'  # accesskey 信息
redis_user_key = 'r51KDIyDIhucBeZgg6LdG80Jccsa61KG'  # 用户信息
redis_notice_strategy_key = '6OxaxI7pWNFnrrPv9xRhDMbiHgCAGPV9'  # 通知策略
redis_current_duty_key = 'TiMZvhP2Sq4CRgCtWNQ7DYYRSZyFzvrV'  # 当前值班人员通知策略信息
redis_current_user_info = 'WceHncIcfwiVvTU1d7Cp1exHipKVNiet'
redis_wechat_access_token_key = 'JxbXt33CrnM5QfWNkiw1IdzsC1QahukoSkA'
redis_event_cron_key = 'TudFVJ7RG6lsSUAuux1fWNkiw1'
redis_scheduling_cron_key = 'redis_scheduling_cron_key'
sys_maintenance_key = 'sys_maintenance_key'

post_parameter_error_info = u'POST 参数错误!'
sys_error_info = u'系统内部错误!'


def generate_random_strings(length):
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    for i in range(length):
        random_str += base_str[random.randint(0, len(base_str) - 1)]
    return random_str


def email_address_check(addr):
    re_email = re.compile(r'^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]{3}$')
    if re_email.match(addr):
        return True
    else:
        return False


def phone_address_check(addr):
    if len(addr) != 11 or addr.isdigit() is False:
        return False
    else:
        return True


def calculating_cycle_time(cycle):
    if cycle == "day":
        now = datetime.date.today()
        return str(now + datetime.timedelta(days=1))
    elif cycle == "week":
        now = datetime.datetime.now()
        return str((now + timedelta(days=7 - now.weekday())).strftime("%Y-%m-%d"))
    elif cycle == "month":
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        if int(month) == 12:
            return str(int(year) + 1) + '-' + str(1)
        else:
            return str(int(year)) + '-' + str(int(month) + 1)


# 每次请求都运行
@app.before_request
def before_request():
    if redis.exists(redis_event_cron_key) == 0:
        redis.set(redis_event_cron_key, "True")  # 默认值
    if redis.exists(redis_scheduling_cron_key) == 0:
        redis.set(redis_scheduling_cron_key, "True")  # 默认值
    if redis.exists(redis_user_key) == 0:
        redis.set(redis_user_key, json.dumps([{
            "ID": i.id,
            "UserName": i.user_name,
            "EmailAddress": i.email_address,
            "PhoneNumber": i.phone_number,
            "WeChatID": i.we_chat_id,
            "CreateTime": i.create_time
        } for i in USER.query.all()]))

    if redis.exists(redis_access_key) == 0:
        redis.set(redis_access_key, json.dumps([{
            "ID": i.id,
            "AccessKeyId": i.access_key_id,
            "AccessKeySecret": i.access_key_secret,
            "CreateTime": i.create_time
        } for i in ACCESSKEY.query.all()]))

    if redis.exists(redis_notice_strategy_key) == 0:
        redis.set(redis_notice_strategy_key, json.dumps([{
            "ID": i.id,
            "UserID": i.user_id,
            "UserName": USER.query.get(i.user_id).user_name,
            "AlarmStatus": i.alarm_status,
            "AlarmLevel": i.alarm_level,
            "NoticeMode": i.notice_mode,
            "CreateTime": i.create_time
        } for i in NOTICESTRATRGY.query.all()]))

    if redis.exists(redis_current_duty_key) == 0:
        scheduling_data = SCHEDULING.query.all()
        if len(scheduling_data) == 0:
            logging.info(u"系统还未配置排班策略")
        else:
            scheduling_data = scheduling_data[0]
            order = scheduling_data.order.split(',')
            if len(order) > 1:
                if int(order[len(order) - 1]) == int(scheduling_data.be_on_duty):
                    next_id = order[0]
                else:
                    next_id = order[int(order.index(scheduling_data.be_on_duty)) + 1]
            else:
                next_id = order[0]
            current = []
            data_ = []
            for i in json.loads(redis.get(redis_notice_strategy_key)):
                if int(i['UserID']) == int(scheduling_data.be_on_duty):
                    current.append(i)
                if int(next_id) == int(i['UserID']):
                    data_.append(i)
            redis.set(redis_current_user_info, json.dumps(
                {
                    "current": {
                        "user_id": scheduling_data.be_on_duty,
                        "user_name": USER.query.get(scheduling_data.be_on_duty).user_name},
                    "next": {
                        "user_id": next_id,
                        "user_name": USER.query.get(next_id).user_name}}
            ))
            redis.set(redis_current_duty_key, json.dumps({"current": current, "next": data_}))


# 认证修饰
def access_auth(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        try:
            data = json.loads(request.data)
            access_key_id = data['AccessKeyId']
            access_key_secret = data['AccessKeySecret']
        except Exception as Error:
            app.logger.error(str(Error))
            return json.dumps({"code": 1, "msg": post_parameter_error_info})
        for i in json.loads(redis.get(redis_access_key)):
            if i['AccessKeyId'] == access_key_id and i['AccessKeySecret'] == access_key_secret:
                return func(*args, **kwargs)
        return json.dumps({"code": 1, "msg": u"AccessKey 认证失败"})

    return decorated_view


# 认证验证
def access_auth_acc(access_key_id, access_key_secret):
    access_data = json.loads(redis.get(redis_access_key))
    for access in access_data:
        if access['AccessKeyId'] == access_key_id and access['AccessKeySecret'] == access_key_secret:
            return True
    return False
