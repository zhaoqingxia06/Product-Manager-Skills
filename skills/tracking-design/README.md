# tracking-design

埋点设计需求文档生成工具。根据原型图自动生成 Excel 格式的埋点设计需求文档。

## 核心分工

**产品经理（你）负责**：把埋点需求写清楚——每个事件"为什么要埋"、"什么时机上报"、"能产出什么指标"。

**埋点设计师负责**：整理上报参数的具体格式和字段定义。

## 输出文档格式

生成的 Excel 文档包含两个 Sheet：

### Sheet 1：埋点总表

| 列 | 列名 | 说明 | 示例 |
|---|---|---|---|
| A | 原型图截图 | 嵌入对应页面的原型截图，开发一看就知道是哪个界面 | 📱 截图 |
| B | 页面 | 所属页面名称，绿色底色=点击事件，橙色底色=曝光事件 | 首页 |
| C | 事件名称 | snake_case 命名，格式：`{模块}_{动作}_{对象}` | `tab_home_click` |
| D | 埋点需求及目的 | **重点列**：写具体业务价值，多目的换行展示 | APP&月活、日新增、3日/7日留存、活跃时间<br>进入APP的用户数、次数 |
| E | 上报时机 | 什么时候触发上报 | 用户点击「首页」Tab时上报 |
| F | 上报参数 | 精简：默认 device_id / event_count / timestamp + 必要业务参数 | device_id：用户数<br>event_count：次数<br>timestamp：上报时间点<br>tab_id：Tab标识 |
| G | 统计指标 | 写具体指标名，不要泛化的"PV/UV" | 点击【语音翻译】的用户数、次数 |

**单元格内换行展示示例：**

埋点需求及目的列（重点）：
```
APP&月活、日新增、3日/7日留存、活跃时间
进入APP的用户数、次数
```

```
单次使用时长、单次输入句子长度
```

```
统计复制操作用户数、次数
```

上报参数列：
```
device_id：用户数
event_count：次数
timestamp：上报时间点
tab_id：Tab标识
```

统计指标列：
```
点击【语音翻译】的用户数、次数
进入设置的用户数、次数
```

## 快速开始

### 安装依赖

```bash
pip install openpyxl Pillow
```

### 初始化文档

```bash
python scripts/generate_tracking.py --init --output "埋点设计需求文档.xlsx"
```

### 追加埋点

准备 `events.json`：

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

运行追加：

```bash
python scripts/generate_tracking.py --append \
  --output "埋点设计需求文档.xlsx" \
  --img-dir "./原型图目录" \
  --events "./events.json"
```

脚本会自动检查并清理重复行。

## 项目结构

```
tracking-design/
├── SKILL.md                          # Skill 说明文档
├── scripts/
│   └── generate_tracking.py          # 核心生成/追加脚本
└── references/
    └── tracking_patterns.md          # 埋点模式参考手册
```
