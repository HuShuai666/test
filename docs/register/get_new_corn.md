### 获取用户new币接口

**请求地址**:
```
    GET     api/v1/newcorn/{user_id}/balance
```

**请求参数**:
```
    
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
          'user_id': user_id,    用户编号
          'balance': balance     账户余额
    },
    "field_name": ""
}
```

**失败返回**：
```

```