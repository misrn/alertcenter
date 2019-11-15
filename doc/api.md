[TOC]

## 公共参数

所有请求都使用的参数

| 名称            | 类型   | 是否必须 | 描述                                          |
| --------------- | ------ | -------- | --------------------------------------------- |
| AccessKeyId     | String | 是       | 认证使用；当系统中未存在AccessKey时，不是必填 |
| AccessKeySecret | String | 是       | 认证使用；当系统中未存在AccessKey时，不是必填 |



## AccessKey 管理

### 创建

- 请求地址：http://127.0.0.1/api/accesskey/create

- 请求方式：POST

- 请求参数：公共参数

- 请求参数示例：

  ```
  {
  	"AccessKeyId": "OkB68h0X2NSQRIVs",
  	"AccessKeySecret": "Tv7kxrH1fC0f88Czmc0usvVxei1IWs1WyerCTrmaXgCuncXUe"
  }
  
  # 返回结果
  {
      "msg": "AccessKey 创建成功.",
      "AccessKeySecret": "EVeQaowZIiqCeD9Q6WRS1z9tbpoQ9TN1IoUREdcC53SUkc2F",
      "code": 0,
      "AccessKeyId": "AH0YzYFMhKoGTlhS"
  }
  ```


### 查询

- 请求地址：

  - http://127.0.0.1/api/accesskey/lists  
- 请求方式：POST
- 请求参数：公共参数

| 名称  | 类型 | 是否必须 | 描述         |
| ----- | ---- | -------- | ------------ |
| page  | Int  | 是       | 查询页数     |
| limit | Int  | 是       | 页面显示条数 |

- 请求参数示例：

  ```
  {
  	"AccessKeyId": "Mat0WbpAK6dxkbzy",
  	"AccessKeySecret": "IXgIKrImTOkKgCuYvGkmR3L8gNf43m2PEdZwqNMvGGZWNnsq",
  	"limit": 10,
  	"page": 1,
  }
  
  # 返回结果
  {
      "msg": "AccessKey 查询成功.",
      "count": 10,
      "code": 0,
      "data": [
          {
              "AccessKeySecret": "IXgIKrImTOkKgCuYvGkmR3L8gNf43m2PEdZwqNMvGGZWNnsq",
              "AccessKeyId": "Mat0WbpAK6dxkbzy",
              "CreateTime": "1566358732",
              "ID": 1
          }
      ]
  }
  ```

### 删除

- 请求地址：http://127.0.0.1/api/accesskey/delete

- 请求方式：POST

- 请求参数：公共参数 +  私有参数  

| 名称     | 类型 | 是否必须 | 描述                |
| -------- | ---- | -------- | ------------------- |
| AccessID | Int  | 是       | 需删除AccessKey的ID |

- 请求参数示例：

  ```
  {
  	"AccessKeyId": "Mat0WbpAK6dxkbzy",
  	"AccessKeySecret": "IXgIKrImTOkKgCuYvGkmR3L8gNf43m2PEdZwqNMvGGZWNnsq",
  	"AccessID": 2
  }
  
  # 返回结果
  {
      "msg": "AccessKey 删除成功.",
      "code": 0
  }
  ```


## 用户管理

### 创建

- 请求地址：http://127.0.0.1/api/user/create

- 请求方式：POST

- 请求参数：公共参数 +  私有参数

| 名称         | 类型   | 是否必填 | 描述     |
| ------------ | ------ | -------- | -------- |
| PhoneNumber  | String | 是       | 电话号码 |
| WeChatID     | String | 是       | 微信号 (手动获取用户openid) |
| UserName     | String | 是       | 用户名   |
| EmailAddress | String | 是       | 邮件地址 |

- 请求参数示例：

  ```
  {
  	"AccessKeyId": "x9HlbsGlw8fDGMsW",
  	"AccessKeySecret": "xcztEynBsUDBN4i3PMEpt8OU1dDylv2AgTGnvrGGRYcSySHO",
  	"UserName": "fanchengdong02",
  	"EmailAddress": "51**727@qq.com",
  	"PhoneNumber": "135***692",
  	"WeChatID": "test"
  }
  
  #返回结果
  {
      "msg": "用户创建成功.",
      "code": 0
  }
  ```

### 编辑

- 请求地址：http://127.0.0.1/api/user/modify

- 请求方式：POST

- 请求参数：公共参数 +  私有参数

| 名称         | 类型   | 是否必须 | 描述             |
| ------------ | ------ | -------- | ---------------- |
| UserID       | Int    | 是       | 需要编辑用户的ID |
| WeChatID     | String | 否       | 微信号码         |
| PhoneNumber  | String | 否       | 电话号码         |
| EmailAddress | String | 否       | 邮件地址         |

  当WeChatID/PhoneNumber/EmailAddress 均未传入，会提示：未修改任何用户信息!

- 请求参数示例：

  ```
  {
  	"AccessKeyId": "x9HlbsGlw8fDGMsW",
  	"AccessKeySecret": "xcztEynBsUDBN4i3PMEpt8OU1dDylv2AgTGnvrGGRYcSySHO",
  	"UserID": "1",
  	"PhoneNumber": "519***88@qq.com",
  	"EmailAddress": "135***92"
  }
  ```

  

### 删除

- 请求地址：http://127.0.0.1/api/user/delete

- 请求方式：POST

- 请求参数：公共参数 +  私有参数

| 名称   | 类型 | 是否必须 | 描述             |
| ------ | ---- | -------- | ---------------- |
| UserID | Int  | 是       | 需要删除的用户ID |

### 查询

- 请求地址：http://127.0.0.1/api/user/lists

- 请求方式：POST

- 请求参数：公共参数


## 排班管理

### 创建

- 请求地址：http://192.168.1.166/api/scheduling/create

- 请求方式：POST

- 请求参数：公共参数 +  私有参数

| 名称            | 类型   | 是否必填 | 描述                           |
| --------------- | ------ | -------- | ------------------------------ |
| SchedulingName  | String | 是       | 排班名称                       |
| SchedulingOrder | String | 是       | 排班顺序，UserID以逗号间隔     |
| SchedulingCycle | String | 是       | 排班周期，值：day，week，month |
| HandoverTime    | Int    | 是       | 交班时间，值：0-24             |

- 请求参数示例：

  ```
  {
  	"AccessKeyId": "Mat0WbpAK6dxkbzy",
  	"AccessKeySecret": "IXgIKrImTOkKgCuYvGkmR3L8gNf43m2PEdZwqNMvGGZWNnsq",
  	"SchedulingName": "运维部排班策略",
  	"SchedulingOrder": "2,4,3,1",
  	"SchedulingCycle": "day",
  	"HandoverTime": "10"
  }
  ```

### 查询

- 请求地址：http://192.168.1.166/api/scheduling/lists
- 请求方式：POST
- 请求参数：公共参数

| 名称  | 类型 | 是否必须 | 描述         |
| ----- | ---- | -------- | ------------ |
| page  | Int  | 是       | 查询页数     |
| limit | Int  | 是       | 页面显示条数 |

### 删除

- 请求地址：http://127.0.0.1/api/scheduling/delete

- 请求方式：POST

- 请求参数：公共参数 +  私有参数

| 名称         | 类型 | 是否必须 | 描述   |
| ------------ | ---- | -------- | ------ |
| SchedulingID | Int  | 是       | 排班ID |

## 通知策略

### 创建

- 请求地址：http://127.0.0.1/api/configure/user/notice/create

- 请求方式：POST

- 请求参数：公共参数 +  私有参数

| 名称        | 类型   | 是否必填 | 描述                           |
| ----------- | ------ | -------- | ------------------------------ |
| AlarmStatus | String | 是       | 告警状态，AlarmStatusParameter |
| AlarmLevel  | String | 是       | 告警级别，AlarmLevelParameter  |
| UserID      | String | 是       | 用户ID                         |
| NoticeMode  | String | 是       | 通知模，AlarmModeParameter     |

  - AlarmStatus：occurs（发生时），closed（关闭时），all（所有）
  - AlarmLevel：info（一般提醒），warning（警告），critical（严重），all（所有）
  - NoticeMode：email（邮件），phone（电话），wechat（微信）

- 请求参数示例：

  ```
  {
  	"AccessKeyId": "Mat0WbpAK6dxkbzy",
  	"AccessKeySecret": "IXgIKrImTOkKgCuYvGkmR3L8gNf43m2PEdZwqNMvGGZWNnsq",
  	"AlarmLevel": "warning",
  	"AlarmStatus": "occurs",
  	"NoticeMode": "email",
  	"UserID": 4
  }
  ```

### 查询

- 请求地址： http://127.0.0.1/api/configure/user/notice/lists
- 请求方式：POST  
- 请求参数：公共参数

| 名称  | 类型 | 是否必须 | 描述         |
| ----- | ---- | -------- | ------------ |
| page  | Int  | 是       | 查询页数     |
| limit | Int  | 是       | 页面显示条数 |

### 删除

- 请求地址：http://127.0.0.1/api/configure/user/notice/delete

- 请求方式：POST

- 请求参数：公共参数 +  私有参数

| 名称 | 类型 | 是否必须 | 描述                                        |
| ---- | ---- | -------- | ------------------------------------------- |
| data | 列表 | 是       | 通知ID列表[{"ID": value},{"ID": value}....] |

  

## 事件管理

### 查询

- 请求地址： http://127.0.0.1/api/event/search
- 请求方式：GET
- 请求参数：

| 名称            | 类型   | 是否必填 | 描述                                            |
| --------------- | ------ | -------- | ----------------------------------------------- |
| AccessKeyId     | String | 是       |                                                 |
| AccessKeySecret | String | 是       |                                                 |
| page            | Int    | 是       | 页数；当Type为history必填                       |
| limit           | Int    | 是       | 显示条数；当Type为history必填                   |
| Type            | String | 是       | history/now，history已经关闭事件，now未关闭事件 |
| UserName        | String | 是       | 事件分配用户，当Type为now必填                   |

### 确认

- 请求地址： http://127.0.0.1/api/event/confirm
- 请求方式：GET
- 请求参数：

| 名称     | 类型   | 是否必填 | 描述                         |
| -------- | ------ | -------- | ---------------------------- |
| UserName | String | 是       | 用户名                       |
| EventID  | String | 是       | 事件唯一ID，注意不是event_id |

### 关闭

当事件未被认领时，不允许手段关闭。

- 请求地址： http://127.0.0.1/api/event/close
- 请求方式：GET
- 请求参数：

| 名称    | 类型   | 是否必填 | 描述       |
| ------- | ------ | -------- | ---------- |
| UserName | String | 是       | 用户名  |
| EventID | String | 是       | 事件唯一ID，注意不是event_id |
| Message | String | 否       | 关闭事件消息 |
