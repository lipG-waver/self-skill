#!/usr/bin/env python3
"""微信聊天记录解析器 - 支持 WeFlow/留痕等工具导出的 xlsx 格式"""

import pandas as pd
import sys
import json
import argparse


def find_header_row(df: pd.DataFrame) -> int:
    """找到包含关键列名的行作为表头"""
    keywords = ['时间', '内容', '消息', '发送', '类型', 'time', 'content', 'message']
    for i, row in df.iterrows():
        row_str = ' '.join(str(v).lower() for v in row.values)
        if sum(1 for kw in keywords if kw in row_str) >= 2:
            return i
    return 0


def parse_wechat(filepath: str, target_name: str = None) -> dict:
    """解析微信聊天记录"""
    df = pd.read_excel(filepath, header=None)
    header_row = find_header_row(df)
    df = pd.read_excel(filepath, header=header_row)

    # 标准化列名
    col_map = {}
    for col in df.columns:
        col_lower = str(col).lower()
        if '时间' in col_lower or 'time' in col_lower:
            col_map[col] = '时间'
        elif '发送' in col_lower or 'sender' in col_lower or '身份' in col_lower:
            col_map[col] = '发送者身份'
        elif '类型' in col_lower or 'type' in col_lower:
            col_map[col] = '消息类型'
        elif '内容' in col_lower or 'content' in col_lower:
            col_map[col] = '内容'
    df = df.rename(columns=col_map)

    # 列出所有发送者
    senders = df['发送者身份'].value_counts().to_dict() if '发送者身份' in df.columns else {}

    if target_name:
        # 筛选目标用户的文本消息
        mask = df['发送者身份'] == target_name
        if '消息类型' in df.columns:
            mask = mask & (df['消息类型'].astype(str).str.contains('文本'))
        target = df[mask].copy()
        target = target[target['内容'].notna()]
        target['内容'] = target['内容'].astype(str).str.strip()
        target = target[target['内容'].str.len() > 0]

        # 排除非文本标记
        exclude = ['[图片]', '[语音]', '[视频]', '[表情包]', '[文件]', '[链接]', '[撤回]']
        target = target[~target['内容'].isin(exclude)]

        messages = target['内容'].tolist()
        times = target['时间'].tolist() if '时间' in target.columns else []

        return {
            'total': len(messages),
            'senders': senders,
            'messages': messages,
            'times': [str(t) for t in times],
            'time_span': f"{times[0]} 至 {times[-1]}" if times else "unknown"
        }

    return {'senders': senders}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='解析微信聊天记录')
    parser.add_argument('file', help='xlsx 文件路径')
    parser.add_argument('--target', help='目标用户名', default=None)
    parser.add_argument('--output', help='输出 JSON 路径', default=None)
    args = parser.parse_args()

    result = parse_wechat(args.file, args.target)
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    else:
        # 只输出统计信息，不输出全部消息
        summary = {k: v for k, v in result.items() if k != 'messages' and k != 'times'}
        summary['message_count'] = result.get('total', len(result.get('messages', [])))
        print(json.dumps(summary, ensure_ascii=False, indent=2))
