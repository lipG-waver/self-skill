# 🎲 骰子游戏 - 对话式交互指南

## 核心原则

**所有游戏选项必须以对话文本形式展示**，不使用任何弹窗、悬浮菜单或 UI 按钮。
用户通过回复文字或数字来选择选项，一切都在对话流中完成。

## 交互流程

### 1. 启动游戏

当用户触发骰子游戏时，运行：
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/dice_game.py menu
```

这会在对话中显示主菜单，用户回复数字 1-5 选择模式。

### 2. 各模式处理

#### 模式 1：快速掷骰
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/dice_game.py quick
```

#### 模式 2：自定义掷骰
先展示选项：
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/dice_game.py custom-options
```
用户选择后执行：
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/dice_game.py roll {数量} {面数}
```
支持 "3d20" 格式解析：数量=3，面数=20。

#### 模式 3：猜大小
先展示选项：
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/dice_game.py guess-options
```
用户选择后执行：
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/dice_game.py guess {大|小}
```

#### 模式 4：骰子决斗
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/dice_game.py duel
```

#### 模式 5：幸运数字
先展示选项：
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/dice_game.py lucky-options
```
用户选择后执行：
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/dice_game.py lucky {猜的数字}
```

### 3. 循环与退出

每次游戏结束后，脚本会自动输出后续选项：
- 🔄 再来一局 → 重新执行当前模式
- 🏠 回到主菜单 → 运行 `menu` 子命令

用户说"不玩了"、"退出"、"结束"时，友好地结束游戏。

## 对话式设计要点

1. **选项用数字编号** — 用户只需回复数字，降低输入成本
2. **用 emoji 做视觉锚点** — 每个选项前有独特 emoji，便于快速扫描
3. **结果后附带选项** — 每次操作完都给出"接下来做什么"的选项
4. **支持自然语言** — 除数字外也接受"掷骰子"、"再来"等自然语言
5. **不依赖任何 UI 组件** — 纯文本交互，在任何终端/对话界面都能用
