### 获取已经查看过的用户列表

**请求地址**:
```
    GET     api/v1/user_record/view_record/
```

**请求参数**:
```
    {"pageNum": 1,"pageSize":10}
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": [
        {
            "view_user_id": "111",    已看过的用户ID
            "invite_at": null,        邀请时间（允许为空）
            "invite_status": 0,       (-1  未邀请，0已邀请， 1已匹配)
            "invite_expire_at": "2018-04-03T10:26:08",   过期时间
            "nickname": "111111",     昵称
            "sex": 1,                 性别
            "avatar_url": "https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLmBgic9UlGySwffswjY9aPPcmTWczKdeFWGnsyVyWgys2Raw3laJh5NaynL8B0ic6QlEYyMCyfOD7g/0"
        }
    ],
    "field_name": ""
}
```

**失败返回**：
```

```