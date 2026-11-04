#!/usr/bin/env python3
"""
埋点设计需求文档生成器
根据原型图分析结果，生成 Excel 格式的埋点设计需求文档
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.drawing.image import Image as XLImage
from openpyxl.utils import get_column_letter
from PIL import Image
import os
import json
import argparse
from pathlib import Path


# 参数描述映射表
PARAM_DESC = {
    "device_id": "用户数",
    "event_count": "次数",
    "timestamp": "上报时间点",
    "user_id": "用户 ID",
    "app_version": "应用版本号",
    "os_type": "操作系统类型",
    "os_version": "操作系统版本",
    "network_type": "网络类型",
    "session_id": "会话 ID",
    "page_id": "当前页面标识",
    "channel": "渠道来源",
    "tab_id": "Tab 标识",
    "tab_name": "Tab 名称",
    "action": "操作类型",
    "status": "状态",
    "speed_level": "速度等级",
    "voice_role": "语音角色",
    "voice_role_name": "角色名称",
    "search_keyword": "搜索关键词",
    "search_result_count": "搜索结果数量",
    "category_id": "分类 ID",
    "category_name": "分类名称",
    "word_id": "词汇 ID",
    "word_text": "词汇文本",
    "is_mastered": "是否已掌握",
    "is_favorited": "是否收藏",
    "play_action": "播放操作",
    "practice_action": "跟练操作",
    "recognition_result": "识别结果",
    "tutorial_id": "教程 ID",
    "toggle_state": "开关状态",
    "feedback_type": "反馈类型",
    "page_source": "页面来源",
    "guide_type": "引导类型",
    "input_length": "输入长度",
    "history_count": "历史记录数量",
    "hot_word": "热搜词",
    "letter_index": "字母索引",
    "sort_order": "排序方式",
    "practice_duration": "跟练时长",
    "speed_change_from": "原速度",
    "speed_change_to": "新速度",
    "role_change_from": "原角色",
    "role_change_to": "新角色",
}

DEFAULT_PARAMS = ["device_id", "event_count", "timestamp"]

# 样式定义
HEADER_FONT = Font(name="微软雅黑", size=11, bold=True, color="FFFFFF")
HEADER_FILL = PatternFill("solid", fgColor="4472C4")
HEADER_ALIGN = Alignment(horizontal="center", vertical="center", wrap_text=True)
CELL_FONT = Font(name="微软雅黑", size=10)
CELL_ALIGN = Alignment(vertical="top", wrap_text=True)
CENTER_ALIGN = Alignment(horizontal="center", vertical="center", wrap_text=True)
THIN_BORDER = Border(
    left=Side(style="thin"), right=Side(style="thin"),
    top=Side(style="thin"), bottom=Side(style="thin"),
)
CLICK_FILL = PatternFill("solid", fgColor="E2EFDA")
EXPOSURE_FILL = PatternFill("solid", fgColor="FCE4D6")


def style_header(ws, row=1, cols=7):
    """设置表头样式"""
    for c in range(1, cols + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = HEADER_ALIGN
        cell.border = THIN_BORDER


def style_cell(ws, row, col, font=CELL_FONT, align=CELL_ALIGN):
    """设置单元格样式"""
    cell = ws.cell(row=row, column=col)
    cell.font = font
    cell.alignment = align
    cell.border = THIN_BORDER
    return cell


def build_params_display(extra_params_str=""):
    """构建上报参数显示文本"""
    lines = []
    for p in DEFAULT_PARAMS:
        lines.append(f"{p}：{PARAM_DESC.get(p, p)}")
    if extra_params_str:
        for p in [e.strip() for e in extra_params_str.split(",") if e.strip()]:
            lines.append(f"{p}：{PARAM_DESC.get(p, p)}")
    return "\n".join(lines)


def build_purpose_display(purposes):
    """构建埋点需求及目的显示文本"""
    if isinstance(purposes, str):
        purposes = [p.strip() for p in purposes.split("/") if p.strip()]
    return "\n".join(purposes)


def create_sheet1(ws):
    """创建埋点总表"""
    headers = ["页面", "事件名称", "埋点需求及目的", "上报时机", "上报参数", "统计指标"]
    for i, h in enumerate(headers, 2):
        ws.cell(row=1, column=i, value=h)
    style_header(ws, cols=7)
    
    ws.column_dimensions['A'].width = 20
    ws.column_dimensions['B'].width = 14
    ws.column_dimensions['C'].width = 16
    ws.column_dimensions['D'].width = 50  # 埋点需求及目的 - 重点列，需要更宽
    ws.column_dimensions['E'].width = 28
    ws.column_dimensions['F'].width = 22
    ws.column_dimensions['G'].width = 24


def create_sheet2(wb):
    """创建公共参数表"""
    ws2 = wb.create_sheet("公共参数")
    pub_headers = ["参数名", "参数类型", "说明", "示例值", "是否必传", "数据价值"]
    for i, h in enumerate(pub_headers, 1):
        ws2.cell(row=1, column=i, value=h)
    style_header(ws2, cols=6)
    
    ws2.column_dimensions['A'].width = 18
    ws2.column_dimensions['B'].width = 12
    ws2.column_dimensions['C'].width = 28
    ws2.column_dimensions['D'].width = 22
    ws2.column_dimensions['E'].width = 10
    ws2.column_dimensions['F'].width = 45

    pub_params = [
        ("device_id", "string", "设备唯一标识（用户数）", "abc123def456", "是",
         "用于去重统计 UV（独立用户数），是计算日活/月活/功能渗透率的基础字段"),
        ("event_count", "int", "点击次数（事件上报次数）", "1", "是",
         "每次上报记为 1 次，聚合后得到 PV（页面浏览量/事件触发次数），用于计算人均使用次数、功能使用频次"),
        ("timestamp", "long", "上报时间（毫秒时间戳）", "1720000000000", "是",
         "用于按时间维度分析用户行为趋势（日/周/月活变化）、使用时段分布、用户活跃时段分析"),
        ("user_id", "string", "用户 ID（登录后）", "user_001", "否",
         "登录用户唯一标识，用于跨设备关联同一用户，计算登录用户的留存和活跃"),
        ("app_version", "string", "应用版本号", "2.0.1", "是",
         "用于按版本维度对比功能使用差异，监控新版本上线后的行为变化"),
        ("os_type", "string", "操作系统类型", "iOS / Android", "是",
         "用于对比不同平台用户行为差异，指导端侧功能优化优先级"),
        ("os_version", "string", "操作系统版本", "17.4", "是",
         "用于分析系统版本对功能兼容性和使用体验的影响"),
        ("network_type", "string", "网络类型", "WiFi / 4G / 5G", "是",
         "用于分析网络环境对功能使用的影响，如弱网下的功能可用性"),
        ("session_id", "string", "会话 ID", "sess_abc123", "是",
         "用于关联同一会话内的连续行为，构建用户行为路径和转化漏斗"),
        ("page_id", "string", "当前页面标识", "dialogue_main", "是",
         "用于按页面维度统计 PV/UV，构建页面流量地图和页面间跳转漏斗"),
        ("channel", "string", "渠道来源", "app_store", "否",
         "用于分析不同渠道用户的行为差异和质量对比"),
    ]
    for idx, (name, ptype, desc, example, required, value) in enumerate(pub_params, 2):
        style_cell(ws2, idx, 1).value = name
        style_cell(ws2, idx, 2, align=CENTER_ALIGN).value = ptype
        style_cell(ws2, idx, 3).value = desc
        style_cell(ws2, idx, 4).value = example
        style_cell(ws2, idx, 5, align=CENTER_ALIGN).value = required
        style_cell(ws2, idx, 6).value = value


def embed_images(ws, events, page_to_img, img_dir, row_idx, img_cache, cropped_sizes):
    """嵌入原型图到 A 列"""
    for idx, ev in enumerate(events, 1):
        page_name = ev[0]
        row = row_idx + idx - 1
        if page_name in page_to_img:
            img_file, x_ratio, y_ratio, w_ratio = page_to_img[page_name]
            cache_key = f"{img_file}_{x_ratio}_{y_ratio}_{w_ratio}"
            if cache_key not in img_cache:
                src = os.path.join(img_dir, img_file)
                pil_img = Image.open(src)
                w, h = pil_img.size
                left = int(w * x_ratio)
                top = int(h * y_ratio)
                right = int(w * (x_ratio + w_ratio))
                bottom = h
                cropped = pil_img.crop((left, top, right, bottom))
                scale = 130 / cropped.width
                new_h = int(cropped.height * scale)
                cropped = cropped.resize((130, new_h), Image.LANCZOS)
                safe_key = cache_key.replace('.', '_').replace('/', '_').replace('(', '_').replace(')', '_')
                tmp_path = os.path.join(os.environ.get("TEMP", "/tmp"), f"embed_{safe_key}.png")
                cropped.save(tmp_path)
                img_cache[cache_key] = tmp_path
                cropped_sizes[cache_key] = (130, new_h)

            img_path = img_cache[cache_key]
            xl_img = XLImage(img_path)
            cw, ch = cropped_sizes[cache_key]
            xl_img.width = cw
            xl_img.height = ch
            anchor = f"A{row}"
            ws.add_image(xl_img, anchor)
            purpose_lines = len(ev[2]) if isinstance(ev[2], list) else 1
            param_lines = 3 + (len(ev[4].split(",")) if ev[4] else 0)
            max_lines = max(purpose_lines, param_lines)
            row_height = max(ch * 0.72 + 10, max_lines * 18 + 10)
            ws.row_dimensions[row].height = row_height


def write_events(ws, events, row_idx):
    """写入埋点事件数据"""
    for idx, ev in enumerate(events, 1):
        (page_name, event_name, purposes, trigger, extra_params, metrics, event_type) = ev
        row = row_idx + idx - 1

        style_cell(ws, row, 2, align=CENTER_ALIGN).value = page_name
        style_cell(ws, row, 3).value = event_name
        purpose_cell = style_cell(ws, row, 4, align=CELL_ALIGN)
        purpose_cell.value = build_purpose_display(purposes)
        style_cell(ws, row, 5).value = trigger
        params_cell = style_cell(ws, row, 6, align=CELL_ALIGN)
        params_cell.value = build_params_display(extra_params)
        style_cell(ws, row, 7).value = metrics

        type_cell = ws.cell(row=row, column=2)
        if event_type == "点击":
            type_cell.fill = CLICK_FILL
        elif event_type == "曝光":
            type_cell.fill = EXPOSURE_FILL


def check_duplicates(ws):
    """检查重复行"""
    rows_data = {}
    duplicates = []
    for row in range(2, ws.max_row + 1):
        page = ws.cell(row=row, column=2).value
        event = ws.cell(row=row, column=3).value
        if page and event:
            key = (page, event)
            if key in rows_data:
                duplicates.append((key, rows_data[key], row))
            else:
                rows_data[key] = row
    return rows_data, duplicates


def remove_duplicates(ws, duplicates):
    """删除重复行"""
    if not duplicates:
        return
    rows_to_delete = sorted(set(d[2] for d in duplicates), reverse=True)
    for row in rows_to_delete:
        ws.delete_rows(row)
    print(f"  Deleted {len(rows_to_delete)} duplicate rows.")


def cmd_init(args):
    """初始化文档"""
    wb = openpyxl.Workbook()
    ws1 = wb.active
    ws1.title = "埋点总表"
    create_sheet1(ws1)
    create_sheet2(wb)
    ws1.freeze_panes = "B2"
    wb.save(args.output)
    print(f"Initialized: {args.output}")


def cmd_append(args):
    """追加埋点"""
    with open(args.events, 'r', encoding='utf-8') as f:
        data = json.load(f)

    events = data.get("events", [])
    page_to_img = data.get("page_to_img", {})

    if not os.path.exists(args.output):
        wb = openpyxl.Workbook()
        ws1 = wb.active
        ws1.title = "埋点总表"
        create_sheet1(ws1)
        create_sheet2(wb)
    else:
        wb = openpyxl.load_workbook(args.output)
        if "埋点总表" not in wb.sheetnames:
            ws1 = wb.active
            ws1.title = "埋点总表"
            create_sheet1(ws1)
            create_sheet2(wb)
        else:
            ws1 = wb["埋点总表"]

    max_row = ws1.max_row
    row_idx = max_row + 1

    write_events(ws1, events, row_idx)

    img_cache = {}
    cropped_sizes = {}
    embed_images(ws1, events, page_to_img, args.img_dir, row_idx, img_cache, cropped_sizes)

    # 去重检查
    rows_data, duplicates = check_duplicates(ws1)
    if duplicates:
        print(f"Found {len(duplicates)} duplicates, removing...")
        remove_duplicates(ws1, duplicates)
        rows_data, duplicates = check_duplicates(ws1)

    wb.save(args.output)
    print(f"Appended {len(events)} events. Total unique: {len(rows_data)}, Duplicates: {len(duplicates)}")


def main():
    parser = argparse.ArgumentParser(description="埋点设计需求文档生成/追加工具")
    subparsers = parser.add_subparsers(dest="command")

    p_init = subparsers.add_parser("init", help="初始化文档")
    p_init.add_argument("--output", required=True, help="输出 xlsx 路径")
    p_init.set_defaults(func=cmd_init)

    p_append = subparsers.add_parser("append", help="追加埋点")
    p_append.add_argument("--output", required=True, help="xlsx 路径")
    p_append.add_argument("--img-dir", required=True, help="原型图目录")
    p_append.add_argument("--events", required=True, help="埋点数据 JSON 文件路径")
    p_append.set_defaults(func=cmd_append)

    args = parser.parse_args()
    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == "__main__":
    main()
