#!/usr/bin/env python3
"""三段采样器 - 从消息列表中按时间段采样中等长度消息"""

import json
import random
import argparse


def sample_messages(messages: list, n_per_stage: int = 60, min_len: int = 20, max_len: int = 120, seed: int = 42) -> dict:
    """三段采样：早期/中期/近期各取 n 条中等长度消息"""
    random.seed(seed)
    total = len(messages)
    third = total // 3

    stages = {
        'early': messages[:third],
        'mid': messages[third:2*third],
        'late': messages[2*third:],
    }

    samples = {}
    for label, pool in stages.items():
        eligible = [m for m in pool if min_len <= len(str(m)) <= max_len]
        k = min(n_per_stage, len(eligible))
        samples[label] = random.sample(eligible, k) if k > 0 else eligible

    return samples


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='JSON with messages array')
    parser.add_argument('--output-dir', help='Output directory', default='.')
    parser.add_argument('--n', type=int, default=60)
    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)

    samples = sample_messages(data['messages'], args.n)

    import os
    os.makedirs(args.output_dir, exist_ok=True)
    for label, msgs in samples.items():
        path = os.path.join(args.output_dir, f'{label}.txt')
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n---\n'.join(msgs))
        print(f"{label}: {len(msgs)} 条样本 → {path}")
