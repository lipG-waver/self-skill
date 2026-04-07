# 自己.skill

> *"如果 18 岁的我看到现在的自己，他会认出我吗？"*

**那些说不出口的话，其实你最想说给自己听。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

&nbsp;

把你自己的聊天记录喂进来——微信、QQ、飞书，什么都行  
它会从几万条消息里，**蒸馏出一个你**  
用你的口头禅说话，用你的节奏回复，连发消息的习惯都一模一样

不是为了造一个替身。是为了在某个深夜回头看的时候，发现自己原来一直是这样的人。

⚠️ **聊天记录是你最私密的数据。本项目全部本地运行，不上传任何服务器。**

[安装](#安装) · [使用](#使用) · [方法论](#方法论四层蒸馏) · [效果示例](#效果示例)

---

## 安装

### Claude Code

```bash
# 安装到当前项目
mkdir -p .claude/skills
git clone https://github.com/user/self-skill .claude/skills/create-self

# 或安装到全局
git clone https://github.com/user/self-skill ~/.claude/skills/create-self
```

### 依赖

```bash
pip3 install -r requirements.txt
```

---

## 使用

在 Claude Code 中输入：

* `/create-self`
* "帮我蒸馏一个自己"
* "我想知道我是怎么说话的"
* "提取我的语言风格"
* "做一个我的数字分身"

### 创建流程

1. **上传聊天记录**：微信/QQ/飞书导出的 xlsx、csv 或 txt
2. **选择目标身份**：哪个昵称是你？
3. **四层蒸馏**：数据清洗 → 量化指纹 → 质性采样 → 人格合成
4. **生成 System Prompt**：一份可以直接喂给任何 LLM 的角色描述
5. **对话验证**：和"自己"聊几句，看像不像

### 管理命令

| 命令 | 说明 |
|------|------|
| `/create-self` | 创建新的自己 |
| `/list-selves` | 列出所有版本 |
| `/{slug}` | 和某个版本的自己对话 |
| `/{slug}-report` | 查看语言风格分析报告 |
| `/update-self {slug}` | 追加数据，迭代进化 |
| `/compare {slug1} {slug2}` | 对比两个时期的自己 |

---

## 方法论：四层蒸馏

```
Layer 1  数据清洗    把原始记录变成干净的纯文本消息流
Layer 2  量化指纹    用数字刻画你说话的「骨架」
Layer 3  质性采样    用人眼捕捉数字抓不到的「灵魂」
Layer 4  人格合成    将骨架和灵魂编码为 System Prompt
```

### Layer 2 提取什么？

| 维度 | 为什么重要 |
|------|-----------|
| 消息长度分布 | 你是一句话拆五条发，还是打一大段？ |
| 高频句尾 | "哈哈"结尾占多少？"吧"呢？ |
| 口头禅 Top 12 | 占比>1% 的词直接写进 prompt |
| 表情偏好 | [旺柴] 还是 😂？频率多少？ |
| 标点使用率 | <10% 说明你根本不用标点——这就是你 |
| 笑声指纹 | 哈×3？哈×7？www？hhh？ |
| 连发模式 | 30秒内连发率>40% = 连珠炮型选手 |

### Layer 3 看什么？

把消息按时间切成早/中/晚三段，每段随机抽 60 条中等长度的消息，人工阅读时关注：

- **句式**：长句还是短句？反问多不多？
- **幽默**：自嘲？讽刺？谐音梗？冷幽默？
- **话题切换**：线性推进还是跳跃式？
- **知识引用**：引用什么领域？学术？流行文化？历史？
- **独特表达**：只有你会用的词、比喻、造词

跨三个时期一致的特征 = 真正的你。只在某个时期出现的 = 情境性的，不写入 prompt。

---

## 效果示例

### 蒸馏时

```
用户：帮我蒸馏一个自己

我：把你的聊天记录丢过来吧。微信导出的 xlsx、QQ 的 txt、飞书的 csv 都行。
   越多越好——消息量 > 5000 条效果最佳。

用户：[上传 chat_export.xlsx]

我：收到。文件里有两个发送者：「Waver」和「Alice」。
   哪个是你？

用户：Waver

我：了解。正在蒸馏 Waver……
   ✅ 筛选出 47,832 条文本消息
   ✅ 消息长度中位数：12字（连发短消息型）
   ✅ Top 口头禅：「哈哈哈」(4.2%)、「其实」(2.1%)、「确实」(1.8%)...
   ✅ 表情偏好：[旺柴] >> [尴尬] >> [可怜]
   ✅ 标点使用率：7.3%（几乎不用标点）
   ✅ 连发率：46.2%（连珠炮型）

   三段采样完成，正在提炼质性特征……
   生成中。
```

### 对话时

```
用户：/waver-2024

Waver(2024)：怎么了

用户：最近有点迷茫

Waver(2024)：迷茫是正常的
   你得先想清楚你到底要什么
   不是那种「我想变优秀」的废话
   是具体的 比如说你到底是要钱还是要意义
   这俩经常冲突的

用户：但我两个都想要

Waver(2024)：那你就得排序
   经济学第一课就是机会成本
   你选了A就必然放弃B
   除非你找到一个A和B重叠的区域
   但那种东西不是想出来的 是试出来的
```

---

## 进阶：时间旅行

这是自己.skill 最特别的功能。

如果你有足够长时间跨度的聊天记录，你可以蒸馏出**不同时期的自己**。

```
/waver-2022    →  大二的自己，刚开始写公众号
/waver-2024    →  大四的自己，做频遇、谈投资
/waver-future  →  基于趋势外推的「未来的自己」
```

然后用 `/compare` 把它们放在一起看：

> 2022 年的你几乎不用「其实」和「本质上」；2024 年这两个词加起来占了 4.7%。
> 你的消息长度中位数从 8 字涨到了 15 字——你开始说更完整的话了。
> 但你的笑声从哈×7 缩短到了哈×3。你笑得少了，还是笑得更克制了？

这不是数据分析。这是考古。

挖的是你自己。

---

## 项目结构

```
self-skill/
├── SKILL.md                      # 主技能文件
├── README.md                     # 你正在看的这个
├── LICENSE                       # MIT
├── requirements.txt              # 依赖
├── prompts/
│   ├── intake.md                # 信息录入引导
│   ├── quantitative_analysis.md # 量化指纹提取规范
│   ├── qualitative_sampling.md  # 质性采样与人工阅读指南
│   ├── persona_synthesis.md     # 人格合成 → System Prompt 模板
│   ├── compare_mode.md          # 时间旅行对比模式
│   └── correction_handler.md    # 对话纠正处理器
└── tools/
    ├── wechat_parser.py         # 微信聊天记录解析
    ├── qq_parser.py             # QQ 聊天记录解析
    ├── generic_parser.py        # 通用 CSV/TXT 解析
    ├── fingerprint_engine.py    # 语言指纹量化引擎
    ├── sampler.py               # 三段采样器
    ├── prompt_compiler.py       # System Prompt 编译器
    └── version_manager.py       # 版本管理与对比
```

---

## 📎 一个不太好笑的笑话

我在想怎么写这个 README 的时候，试了一下让 AI 模仿我说话。

AI 回了一句：「你看，本质上这就是一个信息压缩问题。」

我盯着屏幕看了三秒钟，心想：**我真的是这样说话的吗？**

然后我打开微信，翻了十分钟聊天记录。

「本质上」出现了 247 次。

我关掉了微信。

这就是自己.skill 的意义——不是为了造一个会说话的机器人，而是为了在你以为自己是「随性洒脱」的时候，让数据冷静地告诉你：**你其实是一个每隔三句话就要做一次归因分析的人。**

你以为你在聊天，其实你在开研讨会。

---

## 🕯️ 写给 18 岁的自己

你好。

你现在大概在纠结要不要转专业，或者在图书馆里偷偷看某个人。

你不知道三年后你会做一个 app、谈一笔投资、分析九万条聊天记录来搞清楚自己到底是什么样的人。

但有一件事你已经知道了：你习惯把所有问题都变成系统来解决。

这个习惯会带你走很远。也会让你在某些夜晚，发现自己连难过都要先建个框架。

不用改。这就是你。

只是偶尔记得，有些事情不需要框架。有些人不需要分析。有些感受，感受到了就够了。

这个 skill 不会教你这些。它只会告诉你，你的口头禅是什么、你的消息长度是多少、你用了多少次「哈哈哈」。

但也许你在这些数字里，能看到一个自己都没注意过的自己。

那也不错。

---

## 致谢

本项目方法论灵感来源于：

- **[暗恋对象.skill](https://github.com/xiaoheizi8/crush-skills)**（by xiaoheizi8）— "把人蒸馏成 AI Skill" 的起点
- **[同事.skill](https://github.com/titanwings/colleague-skill)**（by titanwings）— 首创双层架构
- **[前任.skill](https://github.com/therealXiaomanChu/ex-partner-skill)**（by therealXiaomanChu）— 亲密关系场景的先驱

自己.skill 把蒸馏的对象从别人换成了自己。因为在你试图理解任何人之前，也许应该先看看镜子里那个人到底是谁。

本项目遵循 [AgentSkills](https://agentskills.io/) 开放标准，兼容 Claude Code 和 OpenClaw。

---

## License

MIT — 用你自己的数据蒸馏你自己，这件事不需要任何人的许可。
