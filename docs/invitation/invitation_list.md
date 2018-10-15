### 查询邀请记录信息

**请求地址**:
```
    GET     api/v1/invitation/
```

**请求参数**:
```
    {
        "inviter": str  邀请人编号,      
        "invitee": str  被邀请人编号
        
        说明：inviter和invitee参数均传递当前用户编号，当传递inviter=user_id时，就是查询
        我邀请的用户列表，当传递invitee=user_id时，就是查询邀请我的用户列表
    }
```


**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": [
         {
                "id": "618aa03e-cc17-445e-8d84-9b64032ace7d",
                "inviter": "ohg3z0L2RqN6U22R3_UI3PcVOyQA",
                "invitee": "58c298b5-ea52-4fce-b8a6-08c7480e1b70",
                "create_time": "2018-03-26T08:41:40.967513Z",
                "status": 0  (0-有效，1-成功，2-无效)
         },
         {
                "id": "abde982d-0931-4ae8-8bc1-32f03242db79",
                "inviter": "ohg3z0L2RqN6U22R3_UI3PcVOyQA",
                "invitee": "58c298b5-ea52-4fce-b8a6-08c7480e1b70",
                "create_time": "2018-03-26T08:41:48.194076Z",
                "status": 0
         }
    ],
    "field_name": ""
}
```

**失败返回**：
```

```