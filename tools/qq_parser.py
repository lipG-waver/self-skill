#!/usr/bin/env python3
"""QQ 聊天记录解析器 - 支持 QQ 导出的 txt 格式"""

import re
import json
import argparse
from datetime import datetime


def parse_qq(filepath: str, target_name: str = None) -> dict:
    """解析 QQ 聊天记录 txt 文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # QQ 导出格式: 2024-01-01 12:00:00 昵称(QQ号)
    pattern = r'(\d{4}-\d{2}-\d{2} \d{1,2}:\d{2}:\d{2}) (.+?)(?:\((\d+)\))?\s*\n(.*?)(?=\n\d{4}-\d{2}-\d{2}|\Z)'
    matches = re.findall(pattern, text, re.DOTALL)

    records = []
    senders = {}
    for time_str, name, qq_id, content in matches:
        name = name.strip()
        content = content.strip()
        if not content:
            continue
        senders[name] = senders.get(name, 0) + 1
        records.append({'时间': time_str, '发送者身份': name, '内容': content})

    if target_name:
        messages = [r['内容'] for r in records if r['发送者身份'] == target_name]
        times = [r['时间'] for r in records if r['发送者身份'] == target_name]
        return {
            'total': len(messages),
            'senders': senders,
            'messages': messages,
            'times': times,
            'time_span': f"{times[0]} 至 {times[-1]}" if times else "unknown"
        }

    return {'senders': senders}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='解析 QQ 聊天记录')
    parser.add_argument('file', help='txt 文件路径')
    parser.add_argument('--target', help='目标用户名', default=None)
    parser.add_argument('--output', help='输出 JSON 路径', default=None)
    args = parser.parse_args()

    result = parse_qq(args.file, args.target)
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    else:
        summary = {k: v for k, v in result.items() if k not in ('messages', 'times')}
        print(json.dumps(summary, ensure_ascii=False, indent=2))
