#!/bin/bash
# PATH
curl -H "Content-Type:application/json"  -X POST -d "$3" http://127.0.0.1:19090/api/event/zabbix/<AccessKeyID>/<AccessKeySecret>
