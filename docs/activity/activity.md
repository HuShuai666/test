### 获取CP活动信息

**请求地址**:
```
    GET     api/v1/activity/
```

**请求参数**:
```
    {
        "name": str  活动名称  必填
    }
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "id": "1",
        "name": "CP活动馆",
        "image_url": "media/images/activity/1111.png",
        "image_text": "一起谈场24小时就分手的恋爱",
        "context": "\r\n王尔德说，这世界漂亮的脸蛋太多，有趣的灵魂却很少。而能遇见一个不聊过去、不谈身份、不在意物质能卸下假面的朋友……欢迎进入我们这次\r\n不走肾只走心的#谈场24小时就分手的恋爱#活动。",
        "register_time": "2018年1月2日——1月10日",
        "activity_time": "2018年1月12日——1月19日",
        "user_count": "已报名人数",
        "user_plan_count":"计划报名人数"
    },
    "field_name": ""
}
```

**失败返回**：
```

```