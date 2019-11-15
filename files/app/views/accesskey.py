# -*- coding: utf-8 -*-
from flask import Blueprint
from app.views.common import *

Accesskey = Blueprint('accesskey', __name__)


@Accesskey.route('/create', methods=["POST"])
def create():
    try:
        status = False
        if len(ACCESSKEY.query.all()) != 0:  # 如果ACCESSKEY表不为空
            try:
                data = json.loads(request.data)
                access_key_id = data['AccessKeyId']
                access_key_secret = data['AccessKeySecret']
            except Exception as Error:
                logging.error(str(Error))
                return json.dumps({"code": 1, "msg": post_parameter_error_info})
            for i in json.loads(redis.get(redis_access_key)):
                if i['AccessKeyId'] == access_key_id and i['AccessKeySecret'] == access_key_secret:
                    status = True
        else:
            status = True
        if status:
            access_key_id = generate_random_strings(16)
            access_key_secret = generate_random_strings(48)
            db.session.add(ACCESSKEY(access_key_id, access_key_secret))
            db.session.commit()
            redis.delete(redis_access_key)
            return json.dumps({"code": 0, "msg": u"AccessKey 创建成功.", "AccessKeyId": access_key_id,
                               "AccessKeySecret": access_key_secret})
        else:
            return json.dumps({"code": 1, "msg": u"AccessKey 认证失败"})
    except Exception as Error:
        logging.error(str(Error))
        return json.dumps({"code": 1, "msg": sys_error_info})


@Accesskey.route('/lists', methods=["POST"])
@access_auth
def lists():
    try:
        accesskey_data = json.loads(redis.get(redis_access_key))
        data = json.loads(request.data)
        limit = int(data['limit'])
        page = int(data['page'])
        start = limit * page - limit
        end = limit * page
        if end >= len(accesskey_data) or int(limit) >= len(accesskey_data):
            data = accesskey_data[start:]
        else:
            data = accesskey_data[start: end]
        return json.dumps(
            {
                "code": 0,
                "msg": u"AccessKey 查询成功.",
                "count": len(accesskey_data),
                "data": data
            }
        )
    except Exception as Error:
        logging.error(str(Error))
        return json.dumps({"code": 1, "msg": sys_error_info})


@Accesskey.route('/delete', methods=["POST"])
@access_auth
def delete():
    try:
        data = json.loads(request.data)
        if 'AccessID' not in data.keys():
            return json.dumps({"code": 1, "msg": post_parameter_error_info})
        if ACCESSKEY.query.filter(ACCESSKEY.id == data['AccessID']).first() is None:
            return json.dumps({"code": 1, "msg": "The passed AccessID does not exist"})
        else:
            db.session.delete(ACCESSKEY.query.get(data['AccessID']))
            db.session.commit()
            redis.delete(redis_access_key)
            return json.dumps({"code": 0, "msg": u"AccessKey 删除成功."})
    except Exception as Error:
        logging.error(str(Error))
        return json.dumps({"code": 1, "msg": sys_error_info})
