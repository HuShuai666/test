### 查看CP是否已完成任务

**请求地址**:
```
    GET     api/v1/user_task_result/check_cp_task
```

**请求参数**:
```
    {
        "task_id": "任务编号"
    }
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {"任务领取成功"},
    "field_name": ""
}
```

**失败返回**：
```

```