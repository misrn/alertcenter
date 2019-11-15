# -*- coding: utf-8 -*-
from app.views.common import *
from app.modules.wechat import send_wechat_message
from app.modules.Mail import send_mail, mail_
from app.modules.phone import voices


# 排班计划任务
def scheduling():
    if redis.get(redis_scheduling_cron_key) == "True":
        redis.set(redis_scheduling_cron_key, "False")
    else:
        logging.info("排班计划任务锁定")
        return
    try:
        end_date = datetime.datetime.now().strftime("%Y-%m-%d")  # 获取当前
        data = SCHEDULING.query.first()
        if data is not None:
            now_time = int(datetime.datetime.now().strftime('%H'))
            if str(data.end_date) == str(end_date) and int(data.handover_time) == now_time:
                logging.info("执行排班计划任务")
                order = data.order.split(',')
                if int(order[len(order) - 1]) == int(data.be_on_duty):
                    be_on_duty = order[0]
                else:
                    be_on_duty = order[int(order.index(data.be_on_duty)) + 1]
                data.be_on_duty = be_on_duty
                data.end_date = calculating_cycle_time(data.cycle)
                db.session.commit()
                redis.delete(redis_current_duty_key)
        else:
            logging.error('未配置排版策略')
        redis.set(redis_scheduling_cron_key, "True")
    except Exception as Error:
        logging.error(str(Error))
        redis.set(redis_scheduling_cron_key, "True")


def notice_(event_level, way, type_, subject, event_data):
    data = []
    for j in json.loads(redis.get(redis_current_duty_key))[type_]:
        user_data = USER.query.get(j['UserID'])
        if j['NoticeMode'] == "email":
            addr = user_data.email_address
        elif j['NoticeMode'] == "wechat":
            addr = user_data.we_chat_id
        elif j['NoticeMode'] == "phone":
            addr = user_data.phone_number
        else:
            continue
        if j['AlarmStatus'] == "all" and j["AlarmLevel"] == "all":
            data.append({
                "type": j["NoticeMode"],
                "addr": addr
            })
        if j['AlarmStatus'] == way and event_level == j["AlarmLevel"]:
            data.append({
                "type": j["NoticeMode"],
                "addr": addr
            })

    if len(data) > 0:
        wechat = email = phone = False
        for j in data:
            if j['type'] == 'wechat':
                wechat = send_wechat_message(subject, j['addr'], event_data, way)
            if j['type'] == 'email':
                trigger_time = str(
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(event_data.trigger_time))))
                email = send_mail(subject, mail_ % (subject, str(event_data.event_content), str(event_data.event_level),
                                                    trigger_time, str(event_data.source)), [j['addr']], 'html')
            if j['type'] == 'phone':
                phone = voices(j['addr'])

        logging.info('notice_: ' + str(wechat) + str(email) + str(phone))
        if wechat or email or phone:
            return True
        else:
            return False
    else:
        return True


# 事件计划任务
def event_():
    if redis.exists(sys_maintenance_key) == 1:  # 存在
        logging.info("系统维护中........")
        return
    logging.info("redis_event_cron_key: %s" % str(redis.get(redis_event_cron_key)))
    if redis.get(redis_event_cron_key) == "True":
        redis.set(redis_event_cron_key, "False")
    else:
        logging.info("事件计划锁定")
        return
    logging.info("redis_event_cron_key: %s" % str(redis.get(redis_event_cron_key)))
    try:
        event_data = EVENT_TEMPORARY.query.all()  # 查询时间临时表所有数据
        if redis.exists(redis_current_user_info) == 0:
            logging.error("值班用户信息还未缓存")
        else:
            current_user_info = json.loads(redis.get(redis_current_user_info))
            if len(event_data) == 0:
                pass
            else:
                for i in event_data:  # 循环事件
                    data = EVENT_TEMPORARY.query.get(i.id)
                    event_time = int(i.trigger_time) + int(app.config['EVENT_TIMEOUT'])
                    # 未分配事件
                    if int(i.allocation_status) == 2:
                        logging.info("分配(%s)事件给用户: %s" % (i.id, current_user_info['current']['user_name']))
                        subject = "新告警通知"
                        notice_status = notice_(i.event_level, 'occurs', 'current', subject, data)
                        if notice_status:
                            data.allocation_user = current_user_info['current']['user_name']
                            data.allocation_status = '1'
                            db.session.commit()
                    # 值班人员未认领
                    elif i.confirm_user is None and int(time.time()) >= event_time and int(i.next_status) != 1:
                        subject = "新告警通知"
                        logging.info("通知未认领事件(%s)到下期值班人员: %s." % (i.id, current_user_info['next']['user_name']))
                        if notice_(i.event_level, 'occurs', 'next', subject, data):
                            data.next_status = '1'
                            data.allocation_user = data.allocation_user + ',' + current_user_info['next']['user_name']
                            db.session.commit()
                    # 关闭事件
                    elif i.close_way is not None:
                        subject = "告警关闭通知"
                        if notice_(i.event_level, 'closed', 'current', subject, data):
                            db.session.add(
                                EVENT(data.event_id, data.event_name, data.hostname, data.event_content, data.service,
                                      data.ipAddr, data.event_level, data.source, data.allocation_status,
                                      data.next_status, data.allocation_user, data.close_time, data.confirm_time,
                                      data.confirm_user, data.close_way, data.close_user, data.trigger_time,
                                      data.close_message))
                            db.session.delete(data)
                            db.session.commit()
        redis.set(redis_event_cron_key, "True")
    except Exception as Error:
        logging.error(str(Error))
        redis.set(redis_event_cron_key, "True")
