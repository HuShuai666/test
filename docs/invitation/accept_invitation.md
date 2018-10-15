### 接收用户邀请

**请求地址**:
```
    PUT     api/v1/invitation/XXXX {邀请信息编号} 
```

**请求参数**:
```
    {
        "status": str ,     (0-有效, 1-成功) 
        "inviter": str,     邀请人编号
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