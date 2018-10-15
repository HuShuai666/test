### 根据用户编号获取用户注册信息

**请求地址**:
```
    GET     api/v1/register_info/by_user
```

**请求参数**:
```
    {
        "user_id": "ohg3z0ElZQ0ED0zUY6TnWggJmdF5"
    }
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "id": "001d65f8-83eb-4704-8bf7-fa2991bdc22c",
        "nickname": "蘑菇阳",
        "sexual_orientation": 0,
        "overseas_study_status": 1,
        "wechat": "OliviaQ520",
        "phone_number": null,
        "hometown": "成都",
        "future_city": "盐湖城",
        "future_school": "犹他大学",
        "user": "ohg3z0ElZQ0ED0zUY6TnWggJmdFY",
        "create_at": "2018-04-16T03:02:27.171374",
        "update_at": "2018-04-16T14:07:25.489678",
        "constellation": "巨蟹座",
        "sex": 0,
        "birthday": "1989-06-26T00:00:00",
        "demand_area": "异地",
        "demand_cp_age": 1,
        "degree": "本科以上",
        "avatar_url": "https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83epT9IncCXx2iaVOiadRMAOloxm1CIeAicUdwRHWEyANviaGuOVPr51egAZdic4KNtyF1uMLN9uHQoaajog/0",
        "tag": 1,
        "picture_url": "/upload/picture/3a38fd8e-62f0-412e-90ae-0ec231e7cd48.jpg"
    },
    "field_name": ""
}
```

**失败返回**：
```

```