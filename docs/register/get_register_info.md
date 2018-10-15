### 查询注册信息

**请求地址**:
```
    GET     api/v1/register_info/
```

**请求参数**:
```
    {
        "nickname":"zhangsan",        活动昵称
        "user_id": "用户编号",        用户编号
        "wechat":"bobowang_2018",     微信号       
    }
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": "111",
                "nickname": "测试账户一号",
                "sexual_orientation": 0,
                "overseas_study_status": 0,
                "wechat": "15926454545",
                "phone_number": "15926215789",
                "hometown": "武汉",
                "future_city": "纽约",
                "future_school": "纽约",
                "user": "ohg3z0OJFWv66oKX-3PvJdfwB8Ec",
                "create_at": "2018-03-27T17:59:55",
                "update_at": "2018-03-27T18:00:00",
                "constellation": "狮子座",
                "sex": 1,
                "birthday": "2018-03-27T17:59:25",
                "demand_area": "异地",
                "demand_cp_age": 0,
                "degree": "学士"
            }
        ]
    },
    "field_name": ""
}
```

**失败返回**：
```

```