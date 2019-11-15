# -*- coding: utf-8 -*-
from app import db
import time


class USER(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    user_name = db.Column(db.String(255), unique=False, nullable=False)
    email_address = db.Column(db.String(255), unique=False, nullable=False)
    phone_number = db.Column(db.String(255), unique=False, nullable=False)
    create_time = db.Column(db.String(255), unique=False, nullable=False)
    we_chat_id = db.Column(db.String(255), unique=False, nullable=False)

    def __init__(self, user_name, email_address, phone_number, we_chat_id):
        self.user_name = user_name
        self.email_address = email_address
        self.create_time = str(int(time.time()))
        self.phone_number = phone_number
        self.we_chat_id = we_chat_id


class ACCESSKEY(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    access_key_id = db.Column(db.String(255), unique=False, nullable=False)
    access_key_secret = db.Column(db.String(255), unique=False, nullable=False)
    create_time = db.Column(db.String(255), unique=False, nullable=False)

    def __init__(self, access_key_id, access_key_secret):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.create_time = str(int(time.time()))


class SCHEDULING(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    scheduling_name = db.Column(db.String(255), unique=False, nullable=False)
    be_on_duty = db.Column(db.String(255), unique=False, nullable=False)
    end_date = db.Column(db.String(255), unique=False, nullable=False)
    order = db.Column(db.String(255), unique=False, nullable=False)  # 排班顺序
    handover_time = db.Column(db.String(255), unique=False, nullable=False)  # 交接时间
    cycle = db.Column(db.String(255), unique=False, nullable=False)  # 周期 day, week, month
    create_time = db.Column(db.String(255), unique=False, nullable=False)

    def __init__(self, scheduling_name, be_on_duty, end_date, order, cycle, handover_time):
        self.scheduling_name = scheduling_name
        self.be_on_duty = be_on_duty
        self.end_date = end_date
        self.order = order
        self.cycle = cycle
        self.handover_time = handover_time
        self.create_time = str(int(time.time()))


class NOTICESTRATRGY(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    user_id = db.Column(db.String(255), unique=False, nullable=False)  # 用户ID
    alarm_status = db.Column(db.String(255), unique=False, nullable=False)  # 告警状态
    alarm_level = db.Column(db.String(255), unique=False, nullable=False)  # 告警级别
    notice_mode = db.Column(db.String(255), unique=False, nullable=False)  # 通知方式
    create_time = db.Column(db.String(255), unique=False, nullable=False)  # 创建时间

    def __init__(self, user_id, alarm_status, alarm_level, notice_mode):
        self.alarm_status = alarm_status
        self.user_id = user_id
        self.alarm_level = alarm_level
        self.notice_mode = notice_mode
        self.create_time = str(int(time.time()))


class EVENT_TEMPORARY(db.Model):  # 事件临时表
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    event_id = db.Column(db.String(255))  # 时间ID
    event_name = db.Column(db.String(255))  # 告警标题
    hostname = db.Column(db.String(255))  # 告警主机/告警节点
    event_content = db.Column(db.String(255))  # 告警内容
    service = db.Column(db.String(255))  # 服务
    ipAddr = db.Column(db.String(255))  # 主机IP
    event_level = db.Column(db.String(255))  # 告警级别
    trigger_time = db.Column(db.String(255))  # 触发时间
    allocation_status = db.Column(db.String(255))  # 分配状态 1 已分配  2 未分配, 默认未分配
    allocation_user = db.Column(db.String(255))  # 分配用户
    close_time = db.Column(db.String(255))  # 用户手动关闭时间
    confirm_time = db.Column(db.String(255))  # 认领时间
    confirm_user = db.Column(db.String(255))  # 认领用户
    close_way = db.Column(db.String(255))  # 关闭方式 1：系统关闭  2：手动关闭
    close_user = db.Column(db.String(255))  # 事件手动关闭用户
    close_message = db.Column(db.String(255))  # 关闭消息
    next_status = db.Column(db.String(255))  # 是否通知下期值班人员 1 已经通知
    source = db.Column(db.String(255))  # 数据来源

    def __init__(self, event_id, event_name, hostname, event_content, service, ipAddr, event_level, source):
        self.event_content = event_content
        self.event_id = event_id
        self.event_name = event_name
        self.hostname = hostname
        self.service = service
        self.allocation_status = "2"
        self.ipAddr = ipAddr
        self.event_level = event_level
        self.trigger_time = str(int(time.time()))
        self.source = source
        self.next_status = "2"


class EVENT(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    event_id = db.Column(db.String(255))  # 时间ID
    event_name = db.Column(db.String(255))  # 告警主机
    event_content = db.Column(db.String(255))  # 告警内容
    service = db.Column(db.String(255))  # 服务
    hostname = db.Column(db.String(255))  # 服务
    ipAddr = db.Column(db.String(255))  # 主机IP
    event_level = db.Column(db.String(255))  # 告警级别
    trigger_time = db.Column(db.String(255))  # 触发时间
    allocation_status = db.Column(db.String(255))  # 分配状态 1 已分配  2 未分配, 默认未分配
    allocation_user = db.Column(db.String(255))  # 分配用户
    close_time = db.Column(db.String(255))  # 关闭时间
    confirm_time = db.Column(db.String(255))  # 认领时间
    confirm_user = db.Column(db.String(255))  # 认领用户
    close_way = db.Column(db.String(255))  # 关闭方式 1：系统关闭  2：手动关闭
    close_user = db.Column(db.String(255))  # 事件手动关闭用户
    close_message = db.Column(db.String(255))  # 关闭消息
    next_status = db.Column(db.String(255))  # 是否通知下期值班人员 1 已经通知
    source = db.Column(db.String(255))  # 数据来源

    def __init__(self, event_id, event_name, hostname, event_content, service, ipAddr, event_level, source,
                 allocation_status, next_status, allocation_user, close_time, confirm_time,
                 confirm_user, close_way, close_user, trigger_time, close_message):
        self.event_content = event_content
        self.event_id = event_id
        self.event_name = event_name
        self.hostname = hostname
        self.service = service
        self.allocation_status = allocation_status
        self.ipAddr = ipAddr
        self.event_level = event_level
        self.trigger_time = trigger_time
        self.source = source
        self.next_status = next_status
        self.allocation_user = allocation_user
        self.close_time = close_time
        self.confirm_time = confirm_time
        self.confirm_user = confirm_user
        self.close_way = close_way
        self.close_user = close_user
        self.close_message = close_message


class MAINTENANCE(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    start_time = db.Column(db.String(255))  # 开始时间
    duration = db.Column(db.String(255))  # 期间
    msg = db.Column(db.String(255))  # 描述

    def __init__(self, duration, msg):
        self.start_time = str(int(time.time()))
        self.duration = duration
        self.msg = msg

