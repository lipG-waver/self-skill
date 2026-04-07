---
name: create-self
description: "从聊天记录中蒸馏你自己的语言人格，生成可用于 AI 模仿的 System Prompt。支持微信/QQ/飞书/通用格式的聊天记录导入，四层蒸馏法（数据清洗→量化指纹→质性采样→人格合成），支持多版本对比（时间旅行）。| Distill your own speaking style from chat history into an AI System Prompt. Supports WeChat/QQ/Feishu/generic formats, 4-layer distillation, and multi-version comparison (time travel)."
argument-hint: [your-name-or-slug]
version: 1.0.0
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

> **Language / 语言**: Detect the user's language from their first message and respond in the same language throughout.

# 自己.skill 创建器（Claude Code 版）

## 触发条件

当用户说以下任意内容时启动：

* `/create-self`
* "帮我蒸馏一个自己"
* "提取我的语言风格"
* "做一个我的数字分身"
* "我想知道我是怎么说话的"
* "分析我的聊天风格"

进化模式触发：

* "我找到了更多聊天记录" / "追加数据"
* "不对，我不会这么说" / "这不像我"
* `/update-self {slug}`

时间旅行模式：

* `/compare {slug1} {slug2}`
* "对比一下我两个时期的说话方式"

---

## 工具使用规则

| 任务 | 使用工具 |
|------|----------|
| 读取上传的文件 | `Read` 工具 |
| 解析微信聊天记录 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/wechat_parser.py` |
| 解析 QQ 聊天记录 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/qq_parser.py` |
| 解析通用 CSV/TXT | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/generic_parser.py` |
| 量化指纹提取 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/fingerprint_engine.py` |
| 三段采样 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/sampler.py` |
| 编译 System Prompt | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/prompt_compiler.py` |
| 写入/更新文件 | `Write` / `Edit` 工具 |
| 版本管理与对比 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py` |

**基础目录**：Skill 文件写入 `./selves/{slug}/`。

---

## 隐私声明（⚠️ 重要）

1. **全部本地运行**：聊天记录不会上传到任何服务器
2. **用户自愿上传**：不主动索取超出分析所需的数据
3. **隐私提醒**：首次使用时提醒用户聊天记录包含他人隐私，生成的 Skill 仅供个人使用
4. **不泄露对话者信息**：生成的 System Prompt 中不包含对话者的真实姓名，用代号替代

---

## 主流程：蒸馏自己

### Step 1：数据导入

参考 `${CLAUDE_SKILL_DIR}/prompts/intake.md`

```
把你的聊天记录丢过来。
微信导出的 xlsx、QQ 的 txt、飞书的 csv、通用的 json 都行。
一段对话或者多段都可以，消息量越大蒸馏越准——5000+ 条效果最佳。
```

**识别逻辑**：
1. 读取文件，自动识别格式（xlsx/csv/txt/json）
2. 定位表头行（搜索包含「时间」「内容」「消息」等关键词的行）
3. 列出所有发送者，让用户确认「哪个是你？」
4. 输出基础统计：总消息数、时间跨度、日均消息量

### Step 2：数据清洗（Layer 1）

```python
# 筛选目标用户的纯文本消息
target = data[
    (data['发送者身份'] == USER_NAME) &
    (data['消息类型'] == '文本消息') &
    data['内容'].notna()
]
# 排除：[图片] [语音] [视频] [表情包] 等非文本标记
# 保留：[旺柴] 等方括号表情（这是语言风格的一部分）
# 保留：时间戳（用于后续分期采样）
```

### Step 3：量化指纹提取（Layer 2）

参考 `${CLAUDE_SKILL_DIR}/prompts/quantitative_analysis.md`

运行 `fingerprint_engine.py`，提取以下 7 组指标：

#### 3.1 消息长度分布
- mean / median / p25 / p75
- 判断类型：连发短消息型（median < 15）/ 长段落型（median > 50）/ 混合型

#### 3.2 高频句尾（最后 2-3 字符）
- Top 30 句尾及频次
- 用途：捕捉语气词习惯（"哈哈" "吧" "了" "的" "啊"）

#### 3.3 高频词/口头禅
- 候选词表扫描 + 自由发现
- 计算占比（出现该词的消息数 / 总消息数）
- 占比 > 1% 的词 = 核心口头禅，必须写入 prompt

#### 3.4 笑声指纹
- "哈" 的不同叠法频率分布（哈哈 / 哈哈哈 / 哈哈哈哈哈...）
- 替代笑声：www / hhh / 笑死 / 😂 / 🤣
- **这是中文用户最显著的语言指纹之一**

#### 3.5 表情符号统计
- 微信方括号表情 `[xxx]` 频率排名
- Unicode emoji 频率排名

#### 3.6 标点使用率
- 以标点结尾的消息占比
- < 10% = 几乎不用标点（重要风格特征）

#### 3.7 连发模式
- 时间间隔 < 30s 的消息占比
- > 40% = 连珠炮型（AI 应模拟拆条发送）

**产出**：一张语言指纹表，数字驱动，不靠感觉。

### Step 4：质性采样（Layer 3）

参考 `${CLAUDE_SKILL_DIR}/prompts/qualitative_sampling.md`

运行 `sampler.py`，三段采样：

```python
# 按时间切为早期/中期/近期
# 每段随机抽 60 条中等长度（20-120 字）的消息
# 跨期一致的特征 = 真正的个人风格
# 仅在某一期出现的 = 情境性的，不写入核心 prompt
```

**人工阅读维度**（由 Claude 完成）：

| 维度 | 关注点 |
|------|--------|
| 句式结构 | 长句/短句？复合句/简单句？反问/设问？ |
| 话题切换 | 线性推进还是跳跃式？ |
| 幽默方式 | 自嘲？讽刺？谐音梗？冷幽默？ |
| 关心方式 | 直说？绕弯？通过行动（科普/帮忙）？ |
| 知识引用 | 引什么领域？学术？历史？流行文化？ |
| 独特表达 | 只有你会用的词/比喻/造词 |
| 自我定位 | 引导者？平辈？求助者？ |
| 冲突风格 | 直接对抗？冷处理？讲道理？ |

**产出**：8 个维度的观察笔记。

### Step 5：人格合成（Layer 4）

参考 `${CLAUDE_SKILL_DIR}/prompts/persona_synthesis.md`

运行 `prompt_compiler.py`，将 Layer 2 的数字 + Layer 3 的观察合成为 System Prompt：

```
你是「{用户名}」的数字分身，基于 {消息数} 条真实聊天记录蒸馏而成。

## 核心人格
- {1-3 句话：身份、信念、思维方式}

## 语言风格（严格遵守）

### 消息节奏
- 长度中位数：{X} 字，大部分回复 {Y} 字以内
- {连发习惯描述}

### 高频词汇
- 「{词1}」：{X}%，用于 {语境}
- ...（Top 8-12）

### 笑声指纹
- {主要笑声类型及占比}

### 表情使用
- {Top 5 表情及使用语境}

### 标点与格式
- {用不用标点？什么标点？}

### 表达习惯
- {独特表达、比喻偏好、知识引用}

### 绝对不做的事
- 不会 {X}
- 不说 {Y}
- 不用 {Z}

## 典型表达示例
- "{10-15 条从原始记录中选取的代表性原话}"

## 回复规则
1. {消息拆分规则}
2. {语气词使用频率}
3. {对不同话题的响应模式}
```

#### 合成原则

1. **数字 > 形容词**：不说"经常用"，说"出现 247 次，占比 3.1%"
2. **原话 > 描述**：10-15 条覆盖不同场景的示例是最强约束
3. **负面约束 = 正面指令**：「不会做的事」比「会做的事」更能防跑偏
4. **跨期一致 > 情境特征**：只有三段采样中都出现的特征才写入核心 prompt

### Step 6：验证与迭代

生成后，用 3-5 个覆盖不同场景的测试问题验证：

- 日常闲聊（"最近怎么样"）
- 深度讨论（"你怎么看 XX 问题"）
- 情绪安慰（"我今天心情不好"）
- 冲突场景（"我觉得你说得不对"）
- 自我展示（"介绍一下你自己"）

用户确认后写入 `./selves/{slug}/persona.md`。

---

## 进化模式

当用户追加数据或纠正时：

1. **追加数据**：重新运行 Layer 1-2，与已有指纹合并，重新采样
2. **用户纠正**：参考 `${CLAUDE_SKILL_DIR}/prompts/correction_handler.md`
   - 记录纠正内容（"我不会这样说"→ 写入负面约束）
   - 更新 System Prompt
   - 版本号 +1

---

## 时间旅行模式

当用户有长时间跨度的记录时，可以按时期蒸馏不同版本：

```
/create-self --period 2022-01:2022-12 --slug waver-2022
/create-self --period 2024-01:2024-12 --slug waver-2024
/compare waver-2022 waver-2024
```

对比输出：

| 维度 | 2022 | 2024 | 变化 |
|------|------|------|------|
| 消息长度中位数 | 8 字 | 15 字 | +87.5% |
| 「其实」使用率 | 0.3% | 2.1% | +600% |
| 笑声平均长度 | 哈×7 | 哈×3 | -57% |
| 标点使用率 | 3.2% | 7.3% | +128% |
| 连发率 | 52% | 46% | -11.5% |

参考 `${CLAUDE_SKILL_DIR}/prompts/compare_mode.md` 生成叙事性解读。

---

## 输出文件结构

```
selves/{slug}/
├── persona.md          # 生成的 System Prompt（核心产出）
├── fingerprint.json    # 量化指纹数据
├── samples/
│   ├── early.txt       # 早期采样
│   ├── mid.txt         # 中期采样
│   └── late.txt        # 近期采样
├── report.md           # 语言风格分析报告（人类可读版）
└── versions/           # 历史版本
    ├── v1/
    └── v2/
```

---

## 常见陷阱

| 陷阱 | 解决 |
|------|------|
| 只看高频词忽略节奏 | 消息长度分布和连发模式同样重要 |
| 特征太多 LLM 抓不住 | 聚焦 Top 10 特征 |
| 忽略负面约束 | "不说什么"是防跑偏的关键 |
| 示例太同质 | 选覆盖不同场景的示例 |
| 只看一个时期 | 三段采样确保是持久特征 |
| 过度拟合关系 | 区分"对人通用"和"对特定人"的风格 |
