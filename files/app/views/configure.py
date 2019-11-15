# -*- coding: utf-8 -*-
from flask import Blueprint
from app.views.common import *
from sqlalchemy import and_

Configure = Blueprint('configure', __name__)


# 配置用户通知策略
@Configure.route('/user/notice/create', methods=["POST"])
@access_auth
def user_notice_create():
    data = json.loads(request.data)
    try:
        alarm_status = data['AlarmStatus']
        alarm_level = data['AlarmLevel']
        user_id = data['UserID']
        notice_mode = data['NoticeMode']
    except Exception as Error:
        logging.error(str(Error))
        return json.dumps({"code": 1, "msg": post_parameter_error_info})
    try:
        if alarm_level not in AlarmLevelParameter:
            return json.dumps({"code": 1, "msg": u"告警级别配置错误,请参考：%s" % ','.join(AlarmLevelParameter)})
        if notice_mode not in AlarmModeParameter:
            return json.dumps({"code": 1, "msg": u"通知方式配置错误,请参考: %s" % ','.join(AlarmModeParameter)})
        if alarm_status not in AlarmStatusParameter:
            return json.dumps({"code": 1, "msg": u"告警状态配置错误,请参考: %s" % ','.join(AlarmStatusParameter)})
        if int(user_id) not in [int(i.id) for i in USER.query.all()]:
            return json.dumps({"code": 1, "msg": u"输入的用户ID在系统中不存在"})
        if notice_mode == "email" and app.config['MAIL_ENABLE'] is False:
            return json.dumps({"code": 1, "msg": u"系统邮件告警方式未启用!"})
        if notice_mode == "phone" and app.config['PHONE_ENABLE'] is False:
            return json.dumps({"code": 1, "msg": u"系统电话告警方式未启用!"})
        if notice_mode == "wechat" and app.config['WECHAT_ENABLE'] is False:
            return json.dumps({"code": 1, "msg": u"系统微信告警方式未启用!"})
        if NOTICESTRATRGY.query.filter(
                and_(NOTICESTRATRGY.user_id == user_id, NOTICESTRATRGY.alarm_status == alarm_status,
                     NOTICESTRATRGY.alarm_level == alarm_level,
                     NOTICESTRATRGY.notice_mode == notice_mode)).first() is None:
            db.session.add(NOTICESTRATRGY(user_id, alarm_status, alarm_level, notice_mode))
            db.session.commit()
            redis.delete(redis_notice_strategy_key)
            redis.delete(redis_current_duty_key)
            info = {"code": 0, "msg": u"配置用户通知策略成功."}
        else:
            info = {"code": 1, "msg": u"该用户存在相同策略."}
        return json.dumps(info)
    except Exception as Error:
        logging.error(str(Error))
        return json.dumps({"code": 1, "msg": sys_error_info})


# 查询用户通知策略
@Configure.route('/user/notice/lists', methods=["POST"])
@access_auth
def user_notice_lists():
    try:
        json_data = json.loads(redis.get(redis_notice_strategy_key))
        data = json.loads(request.data)
        limit = int(data['limit'])
        page = int(data['page'])
        start = limit * page - limit
        end = limit * page
        if end >= len(json_data) or int(limit) >= len(json_data):
            data = json_data[start:]
        else:
            data = json_data[start: end]
        return json.dumps(
            {
                "code": 0,
                "msg": u"AccessKey 查询成功.",
                "count": len(json_data),
                "data": data
            }
        )
    except Exception as Error:
        logging.error(str(Error))
        return json.dumps({"code": 1, "msg": sys_error_info})


@Configure.route('/user/notice/delete', methods=["POST"])
@access_auth
def user_notice_delete():
    try:
        data = json.loads(request.data)
        if 'data' not in data.keys():
            return json.dumps({"code": 1, "msg": post_parameter_error_info})
        list_ = []
        for dic in data["data"]:
            list_.append(dic['ID'])
            if NOTICESTRATRGY.query.filter(NOTICESTRATRGY.id == dic['ID']).first() is None:
                return json.dumps({"code": 1, "msg": "The passed ID does not exist"})
        for i in NOTICESTRATRGY.query.filter(NOTICESTRATRGY.id.in_(list_)).all():
            db.session.delete(i)
        db.session.commit()
        redis.delete(redis_notice_strategy_key)
        redis.delete(redis_current_duty_key)
        return json.dumps({"code": 0, "msg": u"通知策略 删除成功."})
    except Exception as Error:
        logging.error(str(Error))
        return json.dumps({"code": 1, "msg": sys_error_info})


# 系统维护
@Configure.route('/sys/maintenance', methods=["POST"])
@access_auth
def sys_maintenance():
    try:
        data = json.loads(request.data)
        data_key = data.keys()
        if 'Mode' not in data_key:
            return json.dumps({"code": 1, "msg": post_parameter_error_info})
        if data['Mode'] == "enable":
            if 'Time' not in data_key:
                return json.dumps({"code": 1, "msg": post_parameter_error_info})
            if redis.exists(sys_maintenance_key) == 1:
                return json.dumps({"code": 1, "msg": u'系统中存在维护'})
            db.session.add(MAINTENANCE(data['Time'], data['Msg']))
            redis.set(sys_maintenance_key, '', ex=int(data['Time']) * 60)
            db.session.commit()
        elif data['Mode'] == "disable":
            redis.delete(sys_maintenance_key)
        else:
            return json.dumps({"code": 1, "msg": u'Mode 值错误, 参考["enable", "disable"]'})
        print(redis.exists(sys_maintenance_key))
        return json.dumps({"code": 0, "msg": u"配置成功."})
    except Exception as Error:
        logging.error(str(Error))
        return json.dumps({"code": 1, "msg": sys_error_info})


@Configure.route('/sys/maintenance/lists', methods=["POST"])
@access_auth
def sys_maintenance_lists():
    try:
        sum_count = len(MAINTENANCE.query.all())
        data = json.loads(request.data)
        page = data["page"]
        limit = data["limit"]
        sql_data = MAINTENANCE.query.order_by(
            MAINTENANCE.id.desc()).paginate(int(page), int(limit), error_out=False).items
        data = []
        for i in sql_data:
            end_time = str(int(i.start_time) + int(i.duration) * 60)
            if redis.exists(sys_maintenance_key) == 0:
                status = 'False'
            elif int(end_time) > int(time.time()):
                status = 'True'
            else:
                status = 'False'
            data.append({
                "ID": i.id,
                "StartTime": i.start_time,
                "Duration": i.duration,
                "EndTime": end_time,
                "Msg": i.msg,
                "Status": status
            })
        return json.dumps({"code": 0, "msg": u"查询成功!", "data": data, "count": sum_count})

    except Exception as Error:
        logging.error(str(Error))
        return json.dumps({"code": 1, "msg": sys_error_info})
