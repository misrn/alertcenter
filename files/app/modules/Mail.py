# -*- coding: utf-8 -*-
from app.views.common import *

mail_ = '''<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html ;  charset=utf-8" />
    <title></title>
    <meta charset="utf-8" />

</head>
<body>
    <div class="qmbox qm_con_body_content qqmail_webmail_only" id="mailContentContainer" style="">
        <style type="text/css">
            .qmbox body {margin: 0 ; padding: 0 ; background: #fff ; font-family: "Verdana, Arial, Helvetica, sans-serif" ; font-size: 14px ; line-height: 24px ; }\
            .qmbox img {border: none ; }
            .qmbox .contaner {margin: 0 auto ; width:800px }
            .qmbox .content { margin: 4px ; }
            .qmbox .biaoti {padding: 20px ; color: #000 ; }
            .qmbox .xb1, .qmbox .xb2, .qmbox .xb3, .qmbox .xb4 {display: block ; overflow: hidden ; }
            .qmbox .xb1, .qmbox .xb2, .qmbox .xb3 {height: 1px ; }
            .qmbox .xb2, .qmbox .xb3, .qmbox .xb4 {border-left: 1px solid #BCBCBC ; border-right: 1px solid #BCBCBC ; }
            .qmbox .xb1 {margin: 0 5px ; background: #BCBCBC ; }
            .qmbox .xb2 {margin: 0 3px ; border-width: 0 2px ; }
            .qmbox .xb3 {margin: 0 2px ; }
            .qmbox .xb4 {height: 2px ; margin: 0 1px ; }
            .qmbox .xboxcontent {display: block ; border: 0 solid #BCBCBC ; border-width: 0 1px ; }
            .qmbox .line {margin-top: 6px ; border-top: 1px dashed #B9B9B9 ; padding: 4px ; }
            .qmbox .neirong {padding: 6px ; color: #666666 ; }
            .qmbox .foot {padding: 6px ; color: #777 ; }
            .qmbox .font_lightblue {color: #008BD1 ; font-weight: bold ; }
            .qmbox .font_gray {color: #888 ; font-size: 12px ; }
        </style>
        <div class="contaner">
            <div class="content">
                <p class="biaoti"><b>%s</b></p>
                <b class="xtop"><b class="xb1"></b><b class="xb2"></b><b class="xb3"></b><b class="xb4"></b></b>
                <div class="xboxcontent">
                    <div class="neirong">
                        <p><b>警告内容: %s</b></p>
                        <p><b>警告级别: %s</b></p>
                        <p>触发时间: %s</p>
						<p>应用：<span class="font_lightblue">
                        <span onclick="return false ; " t="7" style="border-bottom: 1px dashed rgb(204, 204, 204) ;  z-index: 1 ;  position: static ; ">%s</span></span><br>
                        <div class="line">系统邮件，请勿回复！</div>
                    </div>
                </div>
                <b class="xbottom"><b class="xb4"></b><b class="xb3"></b><b class="xb2"></b><b class="xb1"></b></b>
            </div>
        </div>
    </div>
</body>
</html>
'''


def send_mail(subject, content, receivers, mail_type):
    mail_host = app.config['MAIL_HOST']
    sender = app.config['MAIL_USER']
    message = MIMEText(content, mail_type, 'utf-8')
    message['From'] = sender
    message['To'] = Header(";".join(receivers), 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(app.config['MAIL_USER'], app.config['MAIL_PASS'])
        smtpObj.sendmail(sender, receivers, message.as_string())
        logging.info("邮件发送成功")
        return True
    except Exception as Error:
        logging.error(str(Error))
        return False
