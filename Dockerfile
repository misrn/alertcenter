from centos:7
RUN  yum -y install epel-release
RUN  yum -y install python36 python36-pip python36-devel  mysql-devel gcc git
RUN  pip3.6 install mysqlclient redis requests flask_sqlalchemy flask_apscheduler flask 
COPY files /zapr
RUN mkdir /logs
RUN rm -rf /etc/localtime
RUN ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
COPY bin/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]