### 获取用户new币记录接口

**请求地址**:
```
    GET     api/v1/newcorn/?user_id={user_id}
```

**请求参数**:
```
    {
        user_id: "用户编号"
    }
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "count": 61,
        "next": "http://localhost:8000/api/v1/newcorn/?page=2&user_id=ohg3z0L2RqN6U22R3_UI3PcVOyQA",
        "previous": null,
        "results": [
            {
                "id": "b77e013e-1ae2-48f3-b0f7-ef28c37c89d6",
                "user": "ohg3z0L2RqN6U22R3_UI3PcVOyQA",
                "operation": 6,
                "corn": 1,
                "create_at": "2018-03-28T11:23:02.981172",
                "extra": "切换用户"
            },
            {
                "id": "91edb570-f257-4588-8ea1-b3874869f1c1",
                "user": "ohg3z0L2RqN6U22R3_UI3PcVOyQA",
                "operation": 6,
                "corn": 1,
                "create_at": "2018-03-28T11:22:58.949946",
                "extra": "切换用户"
            },
            {
                "id": "20254ab4-22e9-47fd-84ee-976eb6d86fd1",
                "user": "ohg3z0L2RqN6U22R3_UI3PcVOyQA",
                "operation": 6,
                "corn": 1,
                "create_at": "2018-03-28T11:22:03.928186",
                "extra": "切换用户"
            },
            {
                "id": "d27b1f00-79b9-49ed-b3a1-a887ad86829a",
                "user": "ohg3z0L2RqN6U22R3_UI3PcVOyQA",
                "operation": 6,
                "corn": 1,
                "create_at": "2018-03-28T11:21:59.393540",
                "extra": "切换用户"
            },
            {
                "id": "a238ec71-97b1-4115-ab82-0054c47f36e4",
                "user": "ohg3z0L2RqN6U22R3_UI3PcVOyQA",
                "operation": 6,
                "corn": 1,
                "create_at": "2018-03-28T11:21:28.290153",
                "extra": "切换用户"
            },
            {
                "id": "b32cbb32-9f4e-4f82-a6e4-5fc1f11022bc",
                "user": "ohg3z0L2RqN6U22R3_UI3PcVOyQA",
                "operation": 6,
                "corn": 1,
                "create_at": "2018-03-28T11:19:36.361216",
                "extra": "切换用户"
            },
            {
                "id": "a6266b4b-411d-414a-bd16-59a1cb2a0855",
                "user": "ohg3z0L2RqN6U22R3_UI3PcVOyQA",
                "operation": 6,
                "corn": 1,
                "create_at": "2018-03-28T11:19:19.916047",
                "extra": "切换用户"
            },
            {
                "id": "100ffbf4-3803-49ce-8823-3c7e9bb9a59c",
                "user": "ohg3z0L2RqN6U22R3_UI3PcVOyQA",
                "operation": 6,
                "corn": 1,
                "create_at": "2018-03-28T11:15:50.051450",
                "extra": "切换用户"
            },
            {
                "id": "3e2b6b79-b269-4e54-8339-62cd2f69cb54",
                "user": "ohg3z0L2RqN6U22R3_UI3PcVOyQA",
                "operation": 6,
                "corn": 1,
                "create_at": "2018-03-28T11:15:45.105177",
                "extra": "切换用户"
            },
            {
                "id": "6eb1803f-1c2f-4e1d-a5be-0d0fd98acf5d",
                "user": "ohg3z0L2RqN6U22R3_UI3PcVOyQA",
                "operation": 6,
                "corn": 1,
                "create_at": "2018-03-28T11:15:31.979498",
                "extra": "切换用户"
            }
        ]
    },
    "field_name": ""
}
```

**失败返回**：
```

```