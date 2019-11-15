# zabbix

```shell
sudo cat  /etc/zabbix/zabbix_server.conf | grep "AlertScriptsPath"
```
进入到AlertScriptsPath配置目录  
拷贝[zapr.sh](http://gitlab.dadingsoft.com/devops/zapr/blob/master/doc/zapr.sh) 文件到当前目录  
修改zapr.sh文件中 AccessKeyID/AccessKeySecret 变量

进入到zabbix控制界面  
Administration  ->  Media types  -> Create media type  
- Name: zapr
- Type：Script
- Script name：zapr.sh
- Script parameters:
    - {ALERT.SENDTO}
    - {ALERT.SUBJECT}
    - {ALERT.MESSAGE}

Configuration -> Actions -> Create action
- Name: zapr
- Operations/Default message：
  ```
  {'eventId':'{HOST.HOST}-{TRIGGER.ID}','eventType':'trigger','alarmName':'{TRIGGER.NAME}','entityName':'{HOSTNAME}','entityId':'{HOST.HOST}-{TRIGGER.ID}','alarmContent':'{HOST.HOST}/{ITEM.NAME}:{ITEM.VALUE}/{TRIGGER.NAME}','priority':'{TRIGGER.NSEVERITY}','host':'{HOST.HOST}','tag':[{'hostgroups':['{TRIGGER.HOSTGROUP.NAME}']}],'agentVersion':'1130','service':'{ITEM.NAME}','ip':'{HOST.IP}','itemName':'{ITEM.NAME}','itemValue':'{ITEM.VALUE}'}
  ```
  
- Operations:
  - Send to Users: Admin
  - Send only to: zapr
- Recovery operations/Default message：
  ```
  {'eventId':'{HOST.HOST}-{TRIGGER.ID}','eventType':'resolve','alarmName':'{TRIGGER.NAME}','entityName':'{HOSTNAME}','entityId':'{HOST.HOST}-{TRIGGER.ID}','alarmContent':'{HOST.HOST}/{ITEM.NAME}:{ITEM.VALUE}/{TRIGGER.NAME}','priority':'{TRIGGER.NSEVERITY}','host':'{HOST.HOST}','tag':[{'hostgroups':['{TRIGGER.HOSTGROUP.NAME}']}],'agentVersion':'1130','service':'{ITEM.NAME}','ip':'{HOST.IP}','itemName':'{ITEM.NAME}','itemValue':'{ITEM.VALUE}'}
  ```
  
Administration ->  Users -> Admin -> Media
- Type: zapr
