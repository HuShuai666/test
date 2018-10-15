### 其他渠道获取new币

**请求地址**:
```
    GET     api/v1/invitation/code
```

**请求参数**:
```
    {
        "code": "邀请码",
        "type": "邀请类型"  0 表示关注留学新青年公众号  2 表示关注北美留学生公众号
        "other_open_id": "用户在当前公众号的open_id"
        "nickname": "用户在当前公众号的nickname"
    }
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
       
    },
    "field_name": ""
}
```

**失败返回**：
```

```