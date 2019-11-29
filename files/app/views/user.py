# -*- coding: utf-8 -*-
from flask import Blueprint
from app.views.common import *

User = Blueprint('user', __name__)


@User.route('/create', methods=["POST"])
@access_auth
def create():
    data = json.loads(request.data)
    try:
        user_name = data['UserName']
        email_address = data['EmailAddress']
        phone_number = data['PhoneNumber']
        we_chat_id = data['WeChatID']
    except Exception as Error:
        logging.error(str(Error))
        return json.dumps({"code": 1, "msg": post_parameter_error_info})
    try:
        if email_address_check(email_address) is False:
            return json.dumps({"code": 1, "msg": u"邮件地址格式错误!"})
        if phone_address_check(phone_number) is False:
            return json.dumps({"code": 1, "msg": u"电话号码格式错误!"})
        if USER.query.filter_by(user_name=user_name).all():
            return json.dumps({"code": 1, "msg": u"用户名重复!"})
        db.session.add(USER(user_name, email_address, phone_number, we_chat_id))
        db.session.commit()
        redis.delete(redis_user_key)
        return json.dumps({"code": 0, "msg": u"用户创建成功."})
    except Exception as Error:
        logging.error(str(Error))
        return json.dumps({"code": 1, "msg": sys_error_info})


@User.route('/lists', methods=["POST"])
@access_auth
def lists():
    try:
        json_data = json.loads(redis.get(redis_user_key))
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


@User.route('/delete', methods=["POST"])
@access_auth
def delete():
    try:
        data = json.loads(request.data)
        schedul = SCHEDULING.query.all()[0]
        order = [int(i) for i in schedul.order.split(',')]
        noti = NOTICESTRATRGY.query.filter(NOTICESTRATRGY.user_id == data['UserID']).all()
        if int(schedul.be_on_duty) == int(data['UserID']):
            return json.dumps({"code": 1, "msg": u"当前用户正在值班，下次请提前操作!"})
        if 'UserID' not in data.keys():
            return json.dumps({"code": 1, "msg": post_parameter_error_info})
        if int(data['UserID']) in order:
            return json.dumps({"code": 1, "msg": u"该用户存在排班信息中，请先删除!"})
        if USER.query.filter(USER.id == data['UserID']).first() is None:
            return json.dumps({"code": 1, "msg": u"输入用户ID不存在!"})
        else:
            db.session.delete(USER.query.get(data['UserID']))
            for i in noti:
                db.session.delete(i)
            db.session.commit()
            redis.delete(redis_user_key)
            redis.delete(redis_notice_strategy_key)
            redis.delete(redis_current_duty_key)
            return json.dumps({"code": 0, "msg": u"用户删除成功."})
    except Exception as Error:
        logging.error(str(Error))
        return json.dumps({"code": 1, "msg": sys_error_info})


@User.route('/modify', methods=["POST"])
@access_auth
def modify():
    try:
        data = json.loads(request.data)

        user_data = USER.query.get(data['UserID'])
        if user_data is None:
            return json.dumps({"code": 1, "msg": u"输入用户ID不存在!"})
        if "PhoneNumber" in data.keys() or "EmailAddress" in data.keys() or "WeChatID" in data.keys():
            if "PhoneNumber" in data.keys():
                if phone_address_check(data['PhoneNumber']) is False:
                    return json.dumps({"code": 1, "msg": u"电话号码格式错误!"})
                else:
                    user_data.phone_number = data['PhoneNumber']
            if "EmailAddress" in data.keys():
                if email_address_check(data['EmailAddress']) is False:
                    return json.dumps({"code": 1, "msg": u"邮件地址格式错误!"})
                else:
                    user_data.email_address = data['EmailAddress']
            if "WeChatID" in data.keys():
                if data['WeChatID'] == "":
                    return json.dumps({"code": 1, "msg": u"微信号不能为空!"})
                user_data.we_chat_id = data['WeChatID']
        else:
            return json.dumps({"code": 1, "msg": u"未修改任何用户信息!"})
        db.session.commit()
        redis.delete(redis_user_key)
        return json.dumps({"code": 0, "msg": u"修改用户信息成功."})
    except Exception as Error:
        logging.error(str(Error))
        return json.dumps({"code": 1, "msg": sys_error_info})
