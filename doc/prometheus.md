# prometheus
修改alertmanager模块的配置文件，通过webhook方式，编辑告警的配置文件，新增 webhook_configs:及以下内容。
```
route:
  routes:
    - receiver: 'zapr'
      continue: true
      match_re:
        job: .*
          
receivers:
- name: 'zapr'
  webhook_configs:
  - url: 'http://127.0.0.1:19090/api/event/prometheus/<AccessKeyID>/<AccessKeySecret>'
    send_resolved: true
```

重新启动alertmanager模块，并加载该配置文件。