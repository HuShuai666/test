### 获取当前用户任务列表

**请求地址**:
```
    GET     api/v1/task
```

**请求参数**:
```
    {
        
    }
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": [
        {
            "id": "2",                            任务编号
            "name": "DAY2",                       任务名称
            "content": "DAY2",                    任务内容
            "extra": "DAY2",                      任务备注
            "create_at": "2018-03-30T15:36:51",   任务创建时间
            "update_at": "2018-03-30T15:36:53",   任务更新时间
            "attend": false                       当前用户是否领取该任务
        },
        {
            "id": "1",
            "name": "DAY1",
            "content": "DAY1",
            "extra": "DAY1",
            "create_at": "2018-03-30T15:36:28",
            "update_at": "2018-03-30T15:36:30",
            "attend": true
            "status": 0 (0-已领取 1已完成 ,如果没有该属性，则表示待领取)
        }
    ],
    "field_name": ""
}
```

**失败返回**：
```

```