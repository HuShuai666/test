### code认证接口

**请求地址**:
```
    GET     api/v1/user/authorize/
```

**请求参数**:
```
    {
        "code": str  必填
    }
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "user_id": "1",
        "ticket": "XXXXXXXX"       
    },
    "field_name": ""
}
```

**失败返回**：
```

```