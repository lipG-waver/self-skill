#!/usr/bin/env python3
"""System Prompt 编译器 - 将指纹数据和质性观察合成为 System Prompt"""

import json
import argparse


def compile_prompt(fingerprint: dict, qualitative_notes: str, name: str, examples: list = None) -> str:
    """将量化指纹 + 质性观察编译为 System Prompt"""
    length = fingerprint['length']
    catchphrases = fingerprint.get('catchphrases', [])
    laughter = fingerprint.get('laughter', [])
    emojis = fingerprint.get('emojis', {})
    punct_rate = fingerprint.get('punctuation_rate', 0)
    burst_rate = fingerprint.get('burst_rate')

    sections = []

    # Header
    sections.append(f'你是「{name}」的数字分身，基于 {fingerprint["total_messages"]} 条真实聊天记录蒸馏而成。')
    sections.append('')

    # 核心人格（从质性观察中提取，需要人工填写）
    sections.append('## 核心人格')
    sections.append(qualitative_notes)
    sections.append('')

    # 语言风格
    sections.append('## 语言风格（严格遵守）')
    sections.append('')

    # 消息节奏
    sections.append('### 消息节奏')
    sections.append(f'- 长度：中位数 {length["median"]} 字，75% 的回复在 {length["p75"]} 字以内（{length["type"]}）')
    if burst_rate is not None:
        burst_desc = '连珠炮型，经常一句话拆多条发' if burst_rate > 40 else '正常节奏'
        sections.append(f'- 连发率：{burst_rate}%（{burst_desc}）')
    sections.append('')

    # 高频词汇
    if catchphrases:
        sections.append('### 高频词汇')
        for phrase, pct in catchphrases[:12]:
            if pct >= 1.0:
                sections.append(f'- 「{phrase}」：{pct}%')
        sections.append('')

    # 笑声指纹
    if laughter:
        sections.append('### 笑声指纹')
        for laugh_type, count in laughter[:5]:
            sections.append(f'- {laugh_type}：{count} 次')
        sections.append('')

    # 表情
    bracket = emojis.get('bracket', [])
    if bracket:
        sections.append('### 表情使用')
        for emoji_name, count in bracket[:5]:
            sections.append(f'- [{emoji_name}]：{count} 次')
        sections.append('')

    # 标点
    sections.append('### 标点与格式')
    if punct_rate < 10:
        sections.append(f'- 标点使用率仅 {punct_rate}%，几乎不用标点结尾')
    else:
        sections.append(f'- 标点使用率 {punct_rate}%')
    sections.append('')

    # 示例
    if examples:
        sections.append('## 典型表达示例')
        for ex in examples[:15]:
            sections.append(f'- "{ex}"')
        sections.append('')

    # 负面约束（占位，需人工补充）
    sections.append('## 绝对不做的事')
    sections.append('- （需根据质性分析补充）')

    return '\n'.join(sections)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fingerprint', help='fingerprint.json 路径')
    parser.add_argument('--name', required=True, help='用户名')
    parser.add_argument('--notes', default='（待补充）', help='质性观察笔记')
    parser.add_argument('--examples', help='示例消息 JSON 文件')
    parser.add_argument('--output', default='persona.md')
    args = parser.parse_args()

    with open(args.fingerprint, 'r', encoding='utf-8') as f:
        fp = json.load(f)

    examples = []
    if args.examples:
        with open(args.examples, 'r', encoding='utf-8') as f:
            examples = json.load(f)

    prompt = compile_prompt(fp, args.notes, args.name, examples)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(prompt)
    print(f'System Prompt 已生成 → {args.output}')
