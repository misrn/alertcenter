#!/bin/bash

CONFIG=/zapr/app/config/config.py

echo "BIND = '0.0.0.0'" > ${CONFIG}

if [ "${PORT}x" == "x" ] ; then
 echo "PORT = 19090" >> ${CONFIG}
else
 echo "PORT = '${PORT}'" >> ${CONFIG}
fi


echo "CSRF_ENABLED = True" >> ${CONFIG}
echo "SECRET_KEY = 'Hiw923hb432j2HAj2ok28J2H2HJ4B'" >> ${CONFIG}
echo "SQLALCHEMY_POOL_SIZE = 100" >> ${CONFIG}
echo "SQLALCHEMY_POOL_RECYCLE = 10" >> ${CONFIG}
echo "SQLALCHEMY_POOL_TIMEOUT = 3000" >> ${CONFIG}
echo "SQLALCHEMY_TRACK_MODIFICATIONS=True" >> ${CONFIG}

if [ "${SQLALCHEMY_DATABASE_URI}x" == "x" ] ; then
 echo "参数 SQLALCHEMY_DATABASE_URI 必须"
 exit 1
else
 echo "SQLALCHEMY_DATABASE_URI = 'mysql://${SQLALCHEMY_DATABASE_URI}'" >> ${CONFIG}
fi

if [ "${REDIS_ADDR}x" == "x" ] ; then
 echo "参数 REDIS_ADDR 必须"
 exit 1
else
 echo "REDIS_ADDR = '${REDIS_ADDR}'" >> ${CONFIG}
fi

if [ "${REDIS_PORT}x" == "x" ] ; then
 echo "REDIS_PORT = 6379" >> ${CONFIG}
else
 echo "REDIS_PORT = ${REDIS_PORT}" >> ${CONFIG}
fi

if [ "${REDIS_DB}x" == "x" ] ; then
 echo "REDIS_DB = 8" >> ${CONFIG}
else
 echo "REDIS_DB = ${REDIS_DB}" >> ${CONFIG}
fi

if [ "${REDIS_PASSWORD}x" == "x" ] ; then
 echo "参数 REDIS_PASSWORD 必须"
 exit 1
else
 echo "REDIS_PASSWORD = '${REDIS_PASSWORD}'" >> ${CONFIG}
fi

if [ "${EVENT_TIMEOUT}x" == "x" ] ; then
 echo "EVENT_TIMEOUT = 1800" >> ${CONFIG}
else
 echo "EVENT_TIMEOUT = ${EVENT_TIMEOUT}" >> ${CONFIG}
fi

# -- 邮件
if [ "${MAIL_ENABLE}x" == "x" ] ; then
 echo "MAIL_ENABLE = False" >> ${CONFIG}
else
 echo "MAIL_ENABLE = ${MAIL_ENABLE}" >> ${CONFIG}
fi


if [ "${MAIL_ENABLE}" == "True" ] ; then
 if [ "${MAIL_USER}x" == "x" ] ; then
  echo "当MAIL_ENABLE为True时，参数 MAIL_USER 必须"
 else
  echo "MAIL_USER = '${MAIL_USER}'" >> ${CONFIG}
 fi
 if [ "${MAIL_PASS}x" == "x" ] ; then
  echo "当MAIL_ENABLE为True时，参数 MAIL_PASS 必须"
 else
  echo "MAIL_PASS = '${MAIL_PASS}'" >> ${CONFIG}
 fi
 if [ "${MAIL_HOST}x" == "x" ] ; then
  echo "当MAIL_ENABLE为True时，参数 MAIL_HOST 必须"
 else
  echo "MAIL_HOST = '${MAIL_HOST}'" >> ${CONFIG}
 fi
 if [ "${MAIL_PORT}x" == "x" ] ; then
  echo "MAIL_PORT = 465" >> ${CONFIG}
 else
  echo "MAIL_PORT = ${MAIL_PORT}" >> ${CONFIG}
 fi
fi

# -- 微信

if [ "${WECHAT_ENABLE}x" == "x" ] ; then
 echo "WECHAT_ENABLE = False" >> ${CONFIG}
else
 echo "WECHAT_ENABLE = ${WECHAT_ENABLE}" >> ${CONFIG}
fi


if [ "${WECHAT_ENABLE}" == "True" ] ; then
 if [ "${WECHAT_APPID}x" == "x" ] ; then
  echo "当WECHAT_ENABLE为True时，参数 WECHAT_APPID 必须"
 else
  echo "WECHAT_APPID = '${WECHAT_APPID}'" >> ${CONFIG}
 fi
 if [ "${WECHAT_SECRET}x" == "x" ] ; then
  echo "当WECHAT_ENABLE为True时，参数 WECHAT_SECRET 必须"
 else
  echo "WECHAT_SECRET = '${WECHAT_SECRET}'" >> ${CONFIG}
 fi
 if [ "${WECHAT_TEAMPLATE_ID}x" == "x" ] ; then
  echo "当WECHAT_ENABLE为True时，参数 WECHAT_TEAMPLATE_ID 必须"
 else
  echo "WECHAT_TEAMPLATE_ID = '${WECHAT_TEAMPLATE_ID}'" >> ${CONFIG}
 fi
 if [ "${WECHAT_OPEN_URL}x" == "x" ] ; then
  echo "当WECHAT_ENABLE为True时，参数 WECHAT_OPEN_URL 必须"
 else
  echo "WECHAT_OPEN_URL = '${WECHAT_OPEN_URL}'" >> ${CONFIG}
 fi 
fi

# -- 电话

if [ "${PHONE_ENABLE}x" == "x" ] ; then
 echo "PHONE_ENABLE = False" >> ${CONFIG}
else
 echo "PHONE_ENABLE = ${PHONE_ENABLE}" >> ${CONFIG}
fi


if [ "${PHONE_ENABLE}" == "True" ] ; then
 if [ "${PHONE_HOST}x" == "x" ] ; then
  echo "当PHONE_ENABLE为True时，参数 PHONE_HOST 必须"
 else
  echo "PHONE_HOST = '${PHONE_HOST}'" >> ${CONFIG}
 fi
 if [ "${PHONE_APPCODE}x" == "x" ] ; then
  echo "当PHONE_ENABLE为True时，参数 PHONE_APPCODE 必须"
 else
  echo "PHONE_APPCODE = '${PHONE_APPCODE}'" >> ${CONFIG}
 fi
fi

echo  'export LANG="en_US.utf8"' >> /etc/profile  && source /etc/profile
python3.6 /zapr/run.py 
