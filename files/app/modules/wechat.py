# -*- coding: utf-8 -*-
from app.views.common import *
import requests
import json

# 颜色表
color_data = {
    "occurs": "#173177",
    "closed": "#00FF00",
    "event": {
        "info": "#00FF00",
        "warning": "#FF8000",
        "critical": "#FF0000"
    }
}


# 获取微信access_token
def get_access_token():
    access_token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s'
    response = requests.get(access_token_url % (app.config['WECHAT_APPID'], app.config['WECHAT_SECRET']))
    if 'access_token' not in json.loads(response.text).keys():
        app.logger.error(json.loads(response.text))
        return False
    else:
        redis.set(redis_wechat_access_token_key, json.loads(response.text)['access_token'])
        return True


# 发送模板消息
def send_wechat_message(title, touser, event_data, way):
    if redis.exists(redis_wechat_access_token_key) == 0:  # access_token缓存不存在
        if get_access_token() is False:
            return False
    event_color = color_data["event"][event_data.event_level]
    clore = color_data[way]
    message_url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token='
    data = {
        "touser": touser,
        "template_id": app.config['WECHAT_TEAMPLATE_ID'],
        "url": app.config['WECHAT_OPEN_URL'],
        "data": {
            "first": {
                "value": "[****] " + title,
                "color": clore
            },
            "keyword1": {
                "value": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(event_data.trigger_time))),
                "color": clore
            },
            "keyword2": {
                "value": event_data.event_level,
                "color": event_color
            },
            "keyword3": {
                "value": str(event_data.event_content),
                "color": clore
            },
            "remark": {
                "value": "告警请及时处理，如已恢复请忽略此消息！",
                "color": clore
            }
        }
    }
    header = {"Content-Type": "application/raw"}

    while True:
        url = message_url + str(redis.get(redis_wechat_access_token_key))
        r = requests.post(url, data=json.dumps(data), headers=header)
        errcode = json.loads(r.text)['errcode']
        if int(errcode) in [40001, 42001]:  # 当为不合法的凭证类型，access_token 超时， 重新获取 access_token
            if get_access_token() is False:
                return False
        elif int(errcode) == 0:
            logging.info('微信通知成功.')
            return True
        else:
            logging.error('发送微信通知失败,错误码：%s' % str(r.text))
            return False
