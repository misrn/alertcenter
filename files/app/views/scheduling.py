# -*- coding: utf-8 -*-
from flask import Blueprint
from app.views.common import *

Scheduling = Blueprint('scheduling', __name__)


# 创建排班计划
@Scheduling.route('/create', methods=["POST"])
@access_auth
def create():
    if SCHEDULING.query.first() is not None:
        return json.dumps({"code": 1, "msg": u'排班计划只允许存在一个'})
    data = json.loads(request.data)
    try:
        scheduling_name = data['SchedulingName']
        order = data['SchedulingOrder']
        cycle = data['SchedulingCycle']
        if cycle not in SchedulingCycle:
            return json.dumps({"code": 1, "msg": u"排班周期配置错误,请参考：%s" % ','.join(SchedulingCycle)})
        handover_time = data['HandoverTime']
        if int(handover_time) < 0 or int(handover_time) > 24:
            return json.dumps({"code": 1, "msg": u"交班时间配置错误,请参考：0-23"})
    except Exception as Error:
        logging.error(str(Error))
        return json.dumps({"code": 1, "msg": post_parameter_error_info})
    try:
        user_date = [int(j['ID']) for j in json.loads(redis.get(redis_user_key))]
        for i in order.split(','):
            if int(i) not in user_date:  # 判断用户ID是否存在
                return json.dumps({"code": 1, "msg": u"用户ID（%s）系统中不存在!" % (str(i))})
        db.session.add(
            SCHEDULING(scheduling_name, str(order.split(',')[0]), calculating_cycle_time(cycle), order, cycle,
                       handover_time))
        db.session.commit()
        return json.dumps({"code": 0, "msg": u"创建排班计划成功."})
    except Exception as Error:
        logging.error(str(Error))
        return json.dumps({"code": 1, "msg": sys_error_info})


@Scheduling.route('/lists', methods=["POST"])
@access_auth
def lists():
    try:
        return json.dumps(
            {"code": 0, "msg": u"查询排班信息成功.", "data": [{
                "ID": i.id,
                "SchedulingName": i.scheduling_name,
                "BeOnDuty": i.be_on_duty,
                "BeOnDutyName": USER.query.get(i.be_on_duty).user_name,
                "EndDate": i.end_date,
                "Order": [USER.query.get(dic).user_name for dic in i.order.split(',')],
                "OrderID": [str(dic) for dic in i.order.split(',')],
                "HandoverTime": i.handover_time,
                "Cycle": i.cycle,
                "CreateTime": i.create_time
            } for i in SCHEDULING.query.all()]})
    except Exception as Error:
        logging.error(str(Error))
        return json.dumps({"code": 1, "msg": sys_error_info})


@Scheduling.route('/delete', methods=["POST"])
@access_auth
def delete():
    try:
        data = json.loads(request.data)
        if 'SchedulingID' not in data.keys():
            return json.dumps({"code": 1, "msg": post_parameter_error_info})
        if SCHEDULING.query.filter(SCHEDULING.id == data['SchedulingID']).first() is None:
            return json.dumps({"code": 1, "msg": u"输入排班ID不存在!"})
        else:
            db.session.delete(SCHEDULING.query.get(data['SchedulingID']))
            db.session.commit()
            return json.dumps({"code": 0, "msg": u"排班策略删除成功."})
    except Exception as Error:
        logging.error(str(Error))
        return json.dumps({"code": 1, "msg": sys_error_info})


@Scheduling.route('/update', methods=["POST"])
@access_auth
def update():
    try:
        data = json.loads(request.data)
        user_data = [int(j['ID']) for j in json.loads(redis.get(redis_user_key))]
        for i in data['SchedulingOrder'].split(','):
            if int(i) not in user_data :  # 判断用户ID是否存在
                return json.dumps({"code": 1, "msg": u"用户ID（%s）系统中不存在!" % (str(i))})

        scheduling_data = SCHEDULING.query.all()[0]
        scheduling_data.scheduling_name = data['SchedulingName']
        scheduling_data.order = data['SchedulingOrder']
        scheduling_data.handover_time = data['HandoverTime']
        scheduling_data.cycle = data['SchedulingCycle']
        db.session.commit()
        return json.dumps({"code": 0, "msg": u"编辑成功."})
    except Exception as Error:
        logging.error(str(Error))
        return json.dumps({"code": 1, "msg": sys_error_info})
