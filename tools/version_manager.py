#!/usr/bin/env python3
"""版本管理与对比工具"""

import os
import json
import shutil
import argparse
from datetime import datetime


def list_versions(base_dir: str) -> list:
    """列出所有版本"""
    versions_dir = os.path.join(base_dir, 'versions')
    if not os.path.exists(versions_dir):
        return []
    versions = sorted(os.listdir(versions_dir))
    return versions


def save_version(base_dir: str) -> str:
    """保存当前状态为新版本"""
    versions_dir = os.path.join(base_dir, 'versions')
    os.makedirs(versions_dir, exist_ok=True)

    existing = list_versions(base_dir)
    next_num = len(existing) + 1
    version_name = f'v{next_num}'
    version_dir = os.path.join(versions_dir, version_name)
    os.makedirs(version_dir)

    for fname in ['persona.md', 'fingerprint.json', 'report.md']:
        src = os.path.join(base_dir, fname)
        if os.path.exists(src):
            shutil.copy2(src, version_dir)

    meta = {'version': version_name, 'created_at': datetime.now().isoformat()}
    with open(os.path.join(version_dir, 'meta.json'), 'w') as f:
        json.dump(meta, f, indent=2)

    return version_name


def compare_fingerprints(fp1_path: str, fp2_path: str) -> dict:
    """对比两个版本的语言指纹"""
    with open(fp1_path, 'r', encoding='utf-8') as f:
        fp1 = json.load(f)
    with open(fp2_path, 'r', encoding='utf-8') as f:
        fp2 = json.load(f)

    comparison = {}
    for key in ['punctuation_rate', 'burst_rate']:
        v1, v2 = fp1.get(key), fp2.get(key)
        if v1 is not None and v2 is not None:
            change = round((v2 - v1) / v1 * 100, 1) if v1 != 0 else None
            comparison[key] = {'v1': v1, 'v2': v2, 'change_pct': change}

    for sub in ['median', 'mean']:
        v1 = fp1.get('length', {}).get(sub)
        v2 = fp2.get('length', {}).get(sub)
        if v1 is not None and v2 is not None:
            change = round((v2 - v1) / v1 * 100, 1) if v1 != 0 else None
            comparison[f'length_{sub}'] = {'v1': v1, 'v2': v2, 'change_pct': change}

    return comparison


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['list', 'save', 'compare'])
    parser.add_argument('--dir', default='.')
    parser.add_argument('--fp1', help='Fingerprint JSON 1 (for compare)')
    parser.add_argument('--fp2', help='Fingerprint JSON 2 (for compare)')
    args = parser.parse_args()

    if args.action == 'list':
        print(json.dumps(list_versions(args.dir), indent=2))
    elif args.action == 'save':
        v = save_version(args.dir)
        print(f'已保存版本: {v}')
    elif args.action == 'compare':
        result = compare_fingerprints(args.fp1, args.fp2)
        print(json.dumps(result, ensure_ascii=False, indent=2))
