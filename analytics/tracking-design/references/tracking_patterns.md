# 埋点设计参考手册

## 常见 UI 模式 → 埋点模板

### 1. 页面级

| UI 模式 | 事件名称 | 埋点需求及目的 | 统计指标 | 特有参数 |
|---------|---------|---------------|---------|---------|
| 页面打开 | `{page}_exposure` | 进入该页面的用户数、次数 | 进入XX页面的用户数、次数 | — |
| 页面返回 | `{page}_back_click` | 页面跳出率 | 点击返回的用户数、次数 | — |

### 2. Tab / 导航

| UI 模式 | 事件名称 | 埋点需求及目的 | 统计指标 | 特有参数 |
|---------|---------|---------------|---------|---------|
| Tab 切换 | `tab_{name}_click` | 各Tab使用频次、用户偏好 | 点击XX Tab的用户数、次数 | tab_id |
| 底部 Tab 切换 | `tab_{name}_click` | 功能使用率 | 点击XX Tab的用户数、次数 | tab_id |

### 3. 按钮 / 图标

| UI 模式 | 事件名称 | 埋点需求及目的 | 统计指标 | 特有参数 |
|---------|---------|---------------|---------|---------|
| 普通按钮点击 | `{object}_click` | 按钮点击用户数、次数 | 点击XX按钮的用户数、次数 | — |
| 图标点击 | `icon_{name}_click` | 图标使用频次 | 点击XX图标的用户数、次数 | — |
| 开关切换 | `{feature}_toggle_click` | 功能开启/关闭比例 | 切换XX开关的用户数、次数 | toggle_state |

### 4. 列表 / 消息

| UI 模式 | 事件名称 | 埋点需求及目的 | 统计指标 | 特有参数 |
|---------|---------|---------------|---------|---------|
| 列表曝光 | `{list}_exposure` | 列表曝光用户数、次数 | XX列表曝光的用户数、次数 | count |
| 列表项点击 | `{item}_click` | 列表项点击用户数、次数 | 点击XX列表项的用户数、次数 | item_id |
| 长按菜单 | `long_press_menu_exposure` | 长按触发用户数、次数 | 触发长按菜单的用户数、次数 | item_id |
| 多选模式 | `multi_select_mode_exposure` | 多选功能使用频次 | 进入多选模式的用户数、次数 | select_count |
| 全选 | `multi_select_all_click` | 全选操作使用频次 | 点击全选的用户数、次数 | select_count |
| 批量删除 | `multi_select_delete_click` | 批量删除转化率 | 点击批量删除的用户数、次数 | delete_count |
| 复制操作 | `copy_click` | 统计复制操作用户数、次数 | 使用【复制】的用户数、次数 | message_id |
| 删除操作 | `delete_click` | 统计单条删除用户数、次数 | 使用【删除】的用户数、次数 | message_id |
| 多选操作 | `multi_select_click` | 统计多选操作用户数、次数 | 使用【多选】的用户数、次数 | message_id |
| 全选操作 | `select_all_click` | 统计使用全选用户数、次数 | 使用【全选】的用户数、次数 | message_id |

### 5. 弹窗 / 确认

| UI 模式 | 事件名称 | 埋点需求及目的 | 统计指标 | 特有参数 |
|---------|---------|---------------|---------|---------|
| 弹窗曝光 | `{dialog}_exposure` | 弹窗曝光用户数、次数 | XX弹窗曝光的用户数、次数 | dialog_type |
| 确认操作 | `{action}_confirm_click` | 转化率 | 点击确认XX的用户数、次数 | count |
| 取消操作 | `{action}_cancel_click` | 取消率 | 点击取消的用户数、次数 | — |

### 6. 输入 / 搜索

| UI 模式 | 事件名称 | 埋点需求及目的 | 统计指标 | 特有参数 |
|---------|---------|---------------|---------|---------|
| 输入框聚焦 | `input_focus` | 输入框使用频次 | 聚焦输入框的用户数、次数 | — |
| 发送/提交 | `{action}_submit_click` | 提交用户数、次数 | 提交XX的用户数、次数 | input_length |
| 搜索激活 | `search_activate` | 搜索功能使用频次 | 激活搜索的用户数、次数 | — |
| 搜索历史点击 | `search_history_click` | 搜索历史使用频次 | 点击搜索历史的用户数、次数 | search_keyword |
| 热搜词点击 | `hot_word_click` | 热搜词点击频次 | 点击热搜词的用户数、次数 | hot_word |
| 搜索联想点击 | `search_suggest_click` | 联想命中率 | 点击搜索联想的用户数、次数 | search_keyword |
| 无搜索结果 | `no_result_exposure` | 无结果场景频次 | 无搜索结果曝光的用户数、次数 | search_keyword |
| 取消搜索 | `search_cancel_click` | 搜索放弃率 | 点击取消搜索的用户数、次数 | search_keyword |

### 7. 媒体播放

| UI 模式 | 事件名称 | 埋点需求及目的 | 统计指标 | 特有参数 |
|---------|---------|---------------|---------|---------|
| 播放按钮 | `play_click` | 播放率 | 点击播放的用户数、次数 | item_id |
| 暂停 | `pause_click` | 暂停操作频次 | 点击暂停的用户数、次数 | item_id |
| 语音播报 | `voice_broadcast_click` | 语音播报使用率 | 使用语音播报的用户数、次数 | item_id |

### 8. 设置 / 选择

| UI 模式 | 事件名称 | 埋点需求及目的 | 统计指标 | 特有参数 |
|---------|---------|---------------|---------|---------|
| 选项选择 | `{feature}_option_click` | 各选项占比 | 选择XX选项的用户数、次数 | speed_level |
| 入口点击 | `{feature}_entry_click` | 入口点击用户数、次数 | 点击XX入口的用户数、次数 | — |
| 开关切换 | `{feature}_toggle_click` | 开关开启的用户数 | 点击XX开关的用户数、次数 | toggle_state |

### 9. 收藏 / 点赞

| UI 模式 | 事件名称 | 埋点需求及目的 | 统计指标 | 特有参数 |
|---------|---------|---------------|---------|---------|
| 收藏/取消收藏 | `favorite_click` | 收藏率 | 收藏XX的用户数、次数 | item_id, is_favorited |

### 10. AI / 识别类

| UI 模式 | 事件名称 | 埋点需求及目的 | 统计指标 | 特有参数 |
|---------|---------|---------------|---------|---------|
| 识别开始 | `recognition_start` | 识别功能使用频次 | 开始识别的用户数、次数 | recognition_status |
| 识别结果 | `recognition_result` | 识别成功率 | 识别完成的用户数、次数 | recognition_result |
| 识别超时 | `recognition_timeout` | 超时率 | 识别超时的用户数、次数 | recognition_status |
| 打断播报 | `interrupt_click` | 打断率 | 打断播报的用户数、次数 | is_interrupted |

## 漏斗设计参考

### 权限授权漏斗
```
permission_dialog_exposure → permission_allow_*_click
授权通过率 = 允许点击 / 弹窗曝光
```

### 多选删除漏斗
```
long_press_multi_select_click → multi_select_mode_exposure → multi_select_delete_click → delete_confirm_click
批量删除转化率 = 确认删除PV / 多选曝光UV
```

### 内容发布漏斗
```
content_submit_click → result_page_exposure
发布完成率 = 结果页曝光 / 提交点击
```

### 跟练完成漏斗
```
practice_page_exposure → practice_recognition_start → practice_recognition_result
跟练完成率 = 识别结果PV / (识别结果PV + practice_skip_click PV)
```

## 事件 JSON 格式（供 append 脚本使用）

```json
{
  "events": [
    ["页面名称", "事件名称", ["目的1", "目的2"], "上报时机", "特有参数", "统计指标", "点击/曝光"]
  ],
  "page_to_img": {
    "页面名称": ["图片文件名", x起点比例, y起点比例, 宽度比例]
  }
}
```
