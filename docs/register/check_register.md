### 获检查用户是否报名活动

**请求地址**:
```
    GET     api/v1/register/check_register
```

**请求参数**:
```
    {
        activity_id："活动编号"
    }
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
          true/false
    },
    "field_name": ""
}
```

**失败返回**：
```

```