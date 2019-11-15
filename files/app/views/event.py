# -*- coding: utf-8 -*-
from flask import Blueprint
from app.views.common import *
from app.views.crond import event_
from sqlalchemy import and_
import hashlib

Event = Blueprint('event', __name__)


# 事件查询
@Event.route('/search', methods=["GET"])
def search():
    access_key_id = request.args.get("AccessKeyId")
    access_key_secret = request.args.get("AccessKeySecret")
    if access_auth_acc(access_key_id, access_key_secret):
        sum_event_count = len(EVENT.query.all())
        page = request.args.get("page")
        limit = request.args.get("limit")
        data = []
        if request.args.get("Type") == "now":  # 未关闭的事件
            sql_data = EVENT_TEMPORARY.query.all()
            pages = 0
        elif request.args.get("Type") == "history":  # 系统已经关闭事件
            pages = sum_event_count // int(limit)
            if (sum_event_count % int(limit)) != 0:
                pages += 1
            sql_data = EVENT.query.order_by(EVENT.id.desc()).paginate(int(page), int(limit), error_out=False).items
        else:
            return json.dumps({"code": 1, "msg": u"Time 传入参数错误!"})
        for i in sql_data:
            if request.args.get("Type") == "history":
                m, s = divmod((int(i.close_time) - int(i.trigger_time)), 60)
                MTTR = str(m) + 'min' + str(s) + 's'
                if i.confirm_time is not None:
                    confirm_m, confirm_s = divmod((int(i.confirm_time) - int(i.trigger_time)), 60)
                    MTTA = str(confirm_m) + 'min' + str(confirm_s) + 's',
                else:
                    MTTA = ''
            else:
                MTTR = MTTA = ''
            data.append({
                "id": i.id,
                "event_id": i.event_id,
                "trigger_time": i.trigger_time,
                "event_level": i.event_level,
                "event_name": i.event_name,
                "event_content": i.event_content,
                "allocation_status": i.allocation_status,
                "allocation_user": i.allocation_user,
                "confirm_user": i.confirm_user,
                "close_way": i.close_way,
                "next_status": i.next_status,
                "close_user": i.close_user,
                "MTTR": MTTR,
                "MTTA": MTTA,
                "user_id": str(json.loads(redis.get(redis_current_user_info))['current']['user_id'])
            })
        return json.dumps({"code": 0, "msg": u"查询事件成功!", "data": data, "pages": pages, "count": sum_event_count})
    return json.dumps({"code": 1, "msg": u"AccessKey 认证失败!"})


# 关闭事件
@Event.route('/close', methods=["GET"])
def close():
    try:
        user_name = request.args.get("UserName")
        event_id = request.args.get("EventID")
        message = request.args.get("Message")
        user_data = USER.query.filter(USER.user_name == user_name).first()
        if user_data is None:
            return json.dumps({"code": 1, "msg": u"未知用户, 拒绝操作!"})
        event_data = EVENT_TEMPORARY.query.filter(EVENT_TEMPORARY.id == event_id).first()  # 查询事件
        if event_data is None:
            return json.dumps({"code": 1, "msg": u"该事件ID不存，或未分配给!"})
        if event_data.close_way is not None:
            return json.dumps({"code": 1, "msg": u"该事件已经关闭!"})
        event_data.close_way = '2'
        event_data.close_user = user_data.user_name
        event_data.close_time = str(int(time.time()))
        event_data.close_message = message
        db.session.commit()
        event_()
        return json.dumps({"code": 0, "msg": u"成功关闭事件."})
    except Exception as Error:
        app.logger.error(str(Error))
        return json.dumps({"code": 1, "msg": sys_error_info})


# 认领事件
@Event.route('/confirm', methods=["GET"])
# @access_auth
def confirm():
    try:
        user_name = request.args.get("UserName")
        event_id = request.args.get("EventID")
        user_data = USER.query.filter(USER.user_name == user_name).first()
        if user_data is None:
            return json.dumps({"code": 1, "msg": u"未知用户, 拒绝操作!"})
        event_data = EVENT_TEMPORARY.query.filter(EVENT_TEMPORARY.id == event_id).first()  # 查询事件
        if event_data is None:
            return json.dumps({"code": 1, "msg": u"该事件ID不存!"})
        if event_data.close_way is not None:
            return json.dumps({"code": 1, "msg": u"该事件已经关闭!"})
        if event_data.confirm_time is None:
            event_data.confirm_user = user_data.user_name
            event_data.confirm_time = str(int(time.time()))
            db.session.commit()
            return json.dumps({"code": 0, "msg": u"成功认领事件."})
        else:
            return json.dumps({"code": 1, "msg": u"该事件已经认领!"})
    except Exception as Error:
        logging.error(str(Error))
        return json.dumps({"code": 1, "msg": sys_error_info})


# zabbix 事件写入
@Event.route('/zabbix/<access_key_id>/<access_key_secret>', methods=["POST"])
# @access_auth
def zabbix(access_key_id, access_key_secret):
    if access_auth_acc(access_key_id, access_key_secret):
        data = json.loads(json.dumps(eval(request.get_data(as_text=True))))
        logging.info("zabbix 请求数据： %s" % json.dumps(data))
        try:
            event_type = data['eventType']  # 事件类型
            event_id = data['eventId']  # 事件ID
            event_id = hashlib.md5(event_id.encode("utf-8")).hexdigest()
            ip_addr = data['ip']  # 主机IP地址
            event_name = data['alarmName']  # 告警标题
            event_content = data['alarmContent']  # 告警内容
            service = data['service']  # 服务
            event_level = data['priority']  # 告警级别
            hostname = data['host']  # 告警主机
        except Exception as Error:
            app.logger.error(str(Error))
            return json.dumps({"code": 1, "msg": u"传入参数错误"})
        if int(event_level) in [0, 1]:
            event_level_ = 'info'
        elif int(event_level) in [2, 3]:
            event_level_ = 'warning'
        elif int(event_level) in [4, 5]:
            event_level_ = 'critical'
        else:
            return json.dumps({"code": 1, u"msg": u"告警级别错误, 0 - 5"})

        if event_type == "trigger":
            data = EVENT_TEMPORARY.query.filter(EVENT_TEMPORARY.event_id == event_id).first()
            if data is not None:
                pass
            else:
                db.session.add(
                    EVENT_TEMPORARY(
                        event_id, event_name, hostname, event_content, service, ip_addr, event_level_, 'zabbix', ))
                db.session.commit()
        if event_type == "resolve":
            data = EVENT_TEMPORARY.query.filter(EVENT_TEMPORARY.event_id == event_id).first()
            if data is None:
                return json.dumps({"code": 1, "msg": u"未查询到该事件/或该事件用户已经手动关闭"})
            data.close_way = '1'
            data.close_user = 'sys'
            data.close_time = str(int(time.time()))
            db.session.commit()
        return json.dumps({"code": 0, "msg": u"请求成功"})
    return json.dumps({"code": 1, "msg": u"AccessKey 认证失败!"})


# prometheus 事件写入
@Event.route('/prometheus/<access_key_id>/<access_key_secret>', methods=["POST"])
def prometheus(access_key_id, access_key_secret):
    if access_auth_acc(access_key_id, access_key_secret):
        data = json.loads(request.data)
        logging.info("prometheus 请求数据： %s" % json.dumps(data))
        for alert in data['alerts']:
            logging.info("-------------------------------------分割线-----------------------------------------------")
            event_name = alert['labels']['alertname']
            event_content = alert['annotations']['message']
            event_level_ = alert['labels']['severity']

            event_id = ''

            keys = sorted(alert['labels'].keys())
            for i in keys:
                if i != "severity":
                    event_id += str(alert['labels'][i])

            event_id = hashlib.md5(event_id.encode("utf-8")).hexdigest()
            logging.info(keys)
            logging.info('prometheus, event_id: %s ,event_level: %s , event_status: %s' % (
                event_id, event_level_, alert['status']))

            if alert['status'] == 'firing':  # 发生时
                data = EVENT_TEMPORARY.query.filter(and_(
                    EVENT_TEMPORARY.event_id == event_id,
                    EVENT_TEMPORARY.event_level == event_level_)).first()
                if data is not None:
                    logging.info('系统中存在相同ID')
                else:
                    logging.info('写入系统数据库')
                    db.session.add(
                        EVENT_TEMPORARY(event_id, event_name, ' ', event_content, event_name, ' ', event_level_,
                                        'prometheus'))
                db.session.commit()

            elif alert['status'] == 'resolved':  # 关闭时
                logging.info("关闭事件入口")
                data = EVENT_TEMPORARY.query.filter(EVENT_TEMPORARY.event_id == event_id).all()
                if data is not None:
                    for i in data:
                        logging.info("关闭事件 %s" % str(i.event_id))
                        i.close_way = '1'
                        i.close_user = 'sys'
                        i.close_time = str(int(time.time()))
                        db.session.commit()
        return json.dumps({"code": 0, "msg": u"请求成功."})
    return json.dumps({"code": 1, "msg": u"AccessKey 认证失败!"})
