### 获取用户CP接口

**请求地址**:
```
    GET     api/v1/invitation/cp
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
        "id": "ffcee096-22f6-4f00-b694-378e792fff9c",
        "nickname": "姜晨",
        "sexual_orientation": 0,
        "overseas_study_status": 0,               (0-'准留学生' 1-'留学生' 2-'毕业生')
        "wechat": "5566",
        "phone_number": "13477776666",
        "hometown": "武汉",
        "future_city": "北京",
        "future_school": "北京大学",
        "user": "ohg3z0L2RqN6U22R3_UI3PcVOyQA",
        "create_at": "2018-04-03T20:51:22.547803",
        "update_at": "2018-04-03T20:52:11",
        "constellation": "白羊",
        "sex": 1,                                 (0-'异性' 1-'同性' 2-'双性')
        "birthday": "2018-04-03T00:00:00",
        "demand_area": "同城",
        "demand_cp_age": 0,                       (0-'比TA大' 1-'跟TA一样' 2-'比TA小')
        "degree": "博士",
        "avatar_url": "https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK3nCbqUphLx8R0mSiczG1jruTMFhBKdzo2ibqOicU6Mf1ibzj7VoFRK2wWibvj0mVxh7AA4OrUpWfKD1Q/0"
    },
    "field_name": ""
}
```

**失败返回**：
```

```