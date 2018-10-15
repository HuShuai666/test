### 检查用户账户信息

**请求地址**:
```
    POST     api/v1/user/check_account/
```

**请求参数**:
```
    {
        "user_id": str  必填,
        "nick_name": str,
        "gender": str,
        "province": str,
        "country": str,
        "city": str,
        "avatar_url": str,
        "language": str,
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