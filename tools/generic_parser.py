#!/usr/bin/env python3
"""通用聊天记录解析器 - 支持 CSV/TSV/JSON"""

import pandas as pd
import json
import argparse


def parse_generic(filepath: str, target_name: str = None) -> dict:
    """自动识别格式并解析"""
    ext = filepath.rsplit('.', 1)[-1].lower()

    if ext == 'csv':
        df = pd.read_csv(filepath)
    elif ext in ('tsv', 'txt'):
        df = pd.read_csv(filepath, sep='\t')
    elif ext == 'json':
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = pd.DataFrame(data.get('messages', data.get('records', [])))
    else:
        raise ValueError(f"不支持的格式: {ext}")

    # 尝试标准化列名
    col_map = {}
    for col in df.columns:
        cl = str(col).lower()
        if any(k in cl for k in ['sender', '发送', 'from', 'user', 'name', '身份']):
            col_map[col] = '发送者身份'
        elif any(k in cl for k in ['content', '内容', 'message', 'text', 'body']):
            col_map[col] = '内容'
        elif any(k in cl for k in ['time', '时间', 'date', 'timestamp']):
            col_map[col] = '时间'
    df = df.rename(columns=col_map)

    senders = df['发送者身份'].value_counts().to_dict() if '发送者身份' in df.columns else {}

    if target_name:
        target = df[df['发送者身份'] == target_name].copy()
        target = target[target['内容'].notna()]
        target['内容'] = target['内容'].astype(str).str.strip()
        target = target[target['内容'].str.len() > 0]
        messages = target['内容'].tolist()
        times = target['时间'].tolist() if '时间' in target.columns else []
        return {
            'total': len(messages),
            'senders': senders,
            'messages': messages,
            'times': [str(t) for t in times],
        }

    return {'senders': senders}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('--target', default=None)
    parser.add_argument('--output', default=None)
    args = parser.parse_args()
    result = parse_generic(args.file, args.target)
    out = {k: v for k, v in result.items() if k not in ('messages', 'times')}
    print(json.dumps(out, ensure_ascii=False, indent=2))
