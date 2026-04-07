# self.skill

> *"If 18-year-old me saw who I am now, would he recognize me?"*

**The things you can't say out loud — you've always wanted to say them to yourself.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)

&nbsp;

Feed it your chat history — WeChat, QQ, Feishu, whatever you've got.  
It distills **you** from tens of thousands of messages.  
Your catchphrases, your rhythm, your habit of sending five messages when one would do.

Not to build a replacement. To look in the mirror and finally see who you've been all along.

[Install](#install) · [Usage](#usage) · [Methodology](#methodology-4-layer-distillation)

---

## Install

```bash
mkdir -p .claude/skills
git clone https://github.com/user/self-skill .claude/skills/create-self
pip3 install -r .claude/skills/create-self/requirements.txt
```

## Usage

In Claude Code:
- `/create-self` — distill yourself from chat logs
- `/compare slug1 slug2` — compare two versions of yourself across time

## Methodology: 4-Layer Distillation

| Layer | What | How |
|-------|------|-----|
| 1. Data Cleaning | Raw chat → clean text messages | Filter by sender, remove media, keep emoji |
| 2. Quantitative Fingerprint | Statistical signature | Message length, catchphrases, laughter patterns, emoji frequency, punctuation rate, burst rate |
| 3. Qualitative Sampling | Read real messages | 3-stage sampling (early/mid/late), 8-dimension analysis |
| 4. Persona Synthesis | Compile System Prompt | Numbers + observations → structured prompt with examples and negative constraints |

## Time Travel

With enough chat history, distill different versions of yourself across time periods and compare how you've changed — your words got longer, your laughs got shorter, your catchphrases shifted. It's archaeology. You're digging up yourself.

## License

MIT
