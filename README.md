# 后台接口文档

### 数据返回格式

**统一为 `json` 格式**:
```
    {
        "code": 0,
        "msg": "success",
        "data": {
            ... // 数据内容
        }
        field_name: ""
    }
```
- code `int` 0为成功，非0为失败 (code=401表示未登录)
- msg `string` 成功或失败的消息
- data `dict` 返回的数据内容
- field_name: `str`  code为非0状态时，报错字段


### API接口文档

**后台接口**:
- [code认证](docs/auth/auth.md)
- [检查账户](docs/auth/check_account.md)
- [获取用户信息](docs/auth/person_information.md)
- [获取活动信息](docs/activity/activity.md)
- [获取活动开始时间](docs/activity/activity_time.md)
- [填写注册资料](docs/register/register_info.md)
- [修改注册资料](docs/register/update_register_info.md)
- [上传用户图片](docs/register/upload_picture.md)
- [检查用户是否报名活动](docs/register/check_register.md)
- [随机获取用户信息](docs/register/random_register_info.md)
- [获取已经查看过的用户列表](docs/invitation/view_user_list.md)
- [获取用户信息](docs/register/get_register_info.md)
- [向用户发送邀请](docs/invitation/send_invitation.md)
- [接收用户邀请](docs/invitation/accept_invitation.md)
- [获取CP大神](docs/invitation/invitation_cp.md)
- [查询用户邀请记录](docs/invitation/invitation_list.md)
- [检查是否有匹配成功的邀请](docs/invitation/check_inviter.md)
- [检查有效的邀请](docs/invitation/check_invitee.md)
- [获取用户new币](docs/register/get_new_corn.md)
- [获取用户new币使用记录](docs/register/get_new_corn_list.md)
- [获取用户CP信息](docs/invitation/cp.md)
- [其他渠道获取new币](docs/invitation/invitation_code.md)
- [创建任务](docs/task/task_create.md)
- [获取当前用户任务列表信息](docs/task/task_list.md)
- [查看任务详情](docs/task/task_detail.md)
- [用户领取任务](docs/task/accept_task.md)
- [用户提交任务](docs/task/finish_task.md)
- [用户提交任务上传图片](docs/task/finish_task_upload.md)
- [查看CP是否已提交任务](docs/task/check_cp_result.md)
- [查看当前用户是否已提交任务](docs/task/check_result.md)
- [查看用户是否关联相关公众号](docs/register/check_attend.md)
- [获取报名人数](docs/register/get_attend_number.md)
- [通过用户编号获取用户注册信息](docs/register/detail.md)
- [获取系统公告](docs/activity/notice.md)