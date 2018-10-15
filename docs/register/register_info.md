### 注册用户信息接口

**请求地址**:
```
    POST     api/v1/register_info/
```

**请求参数**:
```
    {
        "nickname":"zhangsan",        活动昵称
        "sexual_orientation":1,       性取向
        "overseas_study_status":1,    留学状态
        "wechat":"bobowang_2018",     微信号
        "phone_number":"15926215673", 手机号
        "hometown":"wuhan",           国内居住城市
        "future_city":"niuyue",       期望就读城市
        "future_school":"havid",      期望就读学校
        "user":"111",                 用户编号（open_id）
        "activity":"1"                活动编号
        "sex": 0                      性别（0-1）
        "birthday": "1995-08-15"      出生日期
        "constellation": "狮子座"     星座
        "demand_area": "同城"         区域选择
        "CP要求": 0                   0-比TA大  1-跟TA一样大 2-比TA小
        "degree": "本科"              学位
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