### 随机获取用户信息接口

**请求地址**:
```
    GET     api/v1/register_info/random/
```

**请求参数**:
```
    {
       "auto" : True/False 是否扣除new币
    }
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
            "id":"序列号",
            "nickname":"活动昵称",
            "create_at": "创建时间",
            "future_school":"想就读的学校",
            "sexual_orientation":"性取向(0-异性，1-同性，2双性)"，
            "overseas_study_status":"留学状态(0-准留学生,1-留学生,2-毕业生)",
            "wechat":"微信号或手机号",
            "phone_number":"手机号码",
            "hometown":"家乡",
            "future_city":"想就读的城市",
            "future_school":"想就读的学校",
            "user":"用户编号", 
            "sex": 0                      性别（0-1）
            "birthday": "1995-08-15"      出生日期
            "constellation": "狮子座"     星座
            "demand_area": "同城"         区域选择
            "demand_cp_age": 0                   0-比TA大  1-跟TA一样大 2-比TA小
            "degree": "本科"              学位
    },
    "field_name": ""
}
```

**失败返回**：
```

```