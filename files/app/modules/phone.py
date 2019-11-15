# -*- coding: utf-8 -*-
from app.views.common import *
import requests


def voices(phone_number):
    try:
        url = app.config["PHONE_HOST"] + '?' + 'phone=%s&templateId=TP19041915&variable=variable' % (phone_number)
        qer = requests.Session()
        qer.headers = {'Authorization': 'APPCODE ' + app.config["PHONE_APPCODE"]}
        data = json.loads(qer.post(url).text)
        if data["return_code"] == "00000":
            logging.info(u'电话通知成功')
            return True
        else:
            logging.error(u'电话通知失败，错误编码：', data["return_code"])
            return False
    except Exception as Error:
        app.logger.error(str(Error))
        return False

