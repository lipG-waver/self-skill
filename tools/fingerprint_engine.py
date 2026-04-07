#!/usr/bin/env python3
"""语言指纹量化引擎 - 从消息列表中提取 7 组核心指标"""

import json
import re
import argparse
from collections import Counter


def extract_fingerprint(messages: list, times: list = None) -> dict:
    """从消息列表中提取语言指纹"""
    msgs = [str(m).strip() for m in messages if str(m).strip()]
    total = len(msgs)
    if total == 0:
        return {'error': '没有消息可供分析'}

    # 1. 消息长度分布
    lens = sorted([len(m) for m in msgs])
    length_stats = {
        'mean': round(sum(lens) / len(lens), 1),
        'median': lens[len(lens) // 2],
        'p25': lens[len(lens) // 4],
        'p75': lens[3 * len(lens) // 4],
        'p90': lens[int(len(lens) * 0.9)],
    }
    if length_stats['median'] < 15:
        length_stats['type'] = '连发短消息型'
    elif length_stats['median'] > 50:
        length_stats['type'] = '长段落型'
    else:
        length_stats['type'] = '混合型'

    # 2. 高频句尾
    endings = Counter()
    for m in msgs:
        if len(m) >= 2:
            endings[m[-2:]] += 1
        if len(m) >= 3:
            endings[m[-3:]] += 1
    top_endings = endings.most_common(30)

    # 3. 高频词/口头禅
    candidates = [
        '哈哈哈', '哈哈', '其实', '对的', '好的', '但是', '因为', '所以',
        '不过', '确实', '感觉', '可能', '比如', '我觉得', '应该', '还是',
        '或者', '怎么', '这个', '那个', '噢噢', '嗯嗯', '好吧', '牛',
        '卧槽', '绝了', '离谱', '真的', '突然', '反正', '毕竟', '本质上',
        '说白了', '你看', '对吧', '就是', '然后', '那种', '这种', '而且',
        '当然', '显然', '理论上', '按理说', '说实话', '怎么说呢', '某种意义上',
    ]
    catchphrases = {}
    for phrase in candidates:
        count = sum(1 for m in msgs if phrase in m)
        if count > 0:
            catchphrases[phrase] = round(count / total * 100, 2)
    catchphrases = sorted(catchphrases.items(), key=lambda x: -x[1])

    # 4. 笑声指纹
    laughter = Counter()
    for m in msgs:
        # 统计连续"哈"
        ha_matches = re.findall(r'哈{2,}', m)
        for match in ha_matches:
            key = f'哈×{len(match)}'
            laughter[key] += 1
        if 'www' in m.lower():
            laughter['www'] += 1
        if 'hhh' in m.lower():
            laughter['hhh'] += 1
        if '笑死' in m:
            laughter['笑死'] += 1
    laughter = laughter.most_common(15)

    # 5. 表情符号
    bracket_emojis = Counter()
    unicode_emojis = Counter()
    for m in msgs:
        found = re.findall(r'\[([^\]]+)\]', m)
        for e in found:
            bracket_emojis[e] += 1
        for c in m:
            if ord(c) > 0x1F600:
                unicode_emojis[c] += 1
    top_bracket = bracket_emojis.most_common(10)
    top_unicode = unicode_emojis.most_common(10)

    # 6. 标点使用率
    punct_chars = set('。！？，；：、…~.!?,;:')
    punct_count = sum(1 for m in msgs if m and m[-1] in punct_chars)
    punct_rate = round(punct_count / total * 100, 1)

    # 7. 连发模式
    burst_rate = None
    if times and len(times) > 1:
        from datetime import datetime
        parsed = []
        for t in times:
            try:
                parsed.append(datetime.fromisoformat(str(t).replace('/', '-')))
            except Exception:
                parsed.append(None)

        burst_count = 0
        for i in range(1, len(parsed)):
            if parsed[i] and parsed[i-1]:
                gap = (parsed[i] - parsed[i-1]).total_seconds()
                if 0 < gap < 30:
                    burst_count += 1
        burst_rate = round(burst_count / (len(parsed) - 1) * 100, 1)

    result = {
        'total_messages': total,
        'length': length_stats,
        'top_endings': top_endings,
        'catchphrases': catchphrases[:20],
        'laughter': laughter,
        'emojis': {'bracket': top_bracket, 'unicode': top_unicode},
        'punctuation_rate': punct_rate,
        'burst_rate': burst_rate,
    }
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='语言指纹量化引擎')
    parser.add_argument('input', help='包含 messages 和 times 的 JSON 文件')
    parser.add_argument('--output', help='输出 JSON 路径', default=None)
    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)

    result = extract_fingerprint(data['messages'], data.get('times'))

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"指纹已保存到 {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
