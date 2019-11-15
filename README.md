# **alertcenter**

收集zabbix及prometheus监控报警信息，根据配置通知策略进行消息通知


### 快速开始

  ```shell
sudo yum install epel-release -y  
sudo yum install python36 python36-pip python36-devel  mysql-devel gcc git -y
sudo git clone https://github.com/misrn/alertcenter.git && cd alertcenter
sudo pip3.6  install -r requirements.txt
  ```
创建数据库及用户

  ```sql
mysql> CREATE DATABASE `<dbname>` CHARACTER SET 'utf8';  
mysql> CREATE USER `<user>`@`%` IDENTIFIED BY '<passwd>';  
mysql> GRANT ALL ON `<dbname>`.* TO `<user>`@`%`;  
mysql> FLUSH PRIVILEGES;
  ```

创建配置文件  
  ```shell
sudo cp app/config/config-example.py app/config/config.py  
  ```

参考：[config-example.py](<https://github.com/misrn/alertcenter/blob/master/files/app/config/config-example.py>)

### 启动

```shell
python3.6 files/initialdb.py  # 初始化数据库  
python3.6 files/run.py 
```

### 容器化部署
  ```shell
sudo git clone https://github.com/misrn/alertcenter.git && cd alertcenter
  ```
#### 镜像构建  

    docker build -t alertcenter:latest .
#### 镜像参数
参数说明参考: [config-example.py](<https://github.com/misrn/alertcenter/blob/master/files/app/config/config-example.py>)
- `PORT`
- `SQLALCHEMY_DATABASE_URI`
- `REDIS_ADDR`
- `REDIS_PROT`
- `REDIS_DB`
- `REDIS_PASSWD`
- `EVENT_TIMEOUT`
- `MAIL_ENABLE`
- `MAIL_USER`
- `MAIL_PASS`
- `MAIL_HOST`
- `MAIL_PORT`
- `WECHAT_ENABLE`
- `WECHAT_APPID`
- `WECHAT_SECRET`
- `WECHAT_TEAMPLATE_ID`
- `PHONE_ENABLE`
- `PHONE_HOST`
- `PHONE_APPCODE`

### API规则

[API文档](<https://github.com/misrn/alertcenter/blob/master/doc/api.md>)

### 集成
目前支持zabbix prometheus

[zabbix](<https://github.com/misrn/alertcenter/blob/master/doc/zabbix.md>) [prometheus](<https://github.com/misrn/alertcenter/blob/master/doc/prometheus.md>)

