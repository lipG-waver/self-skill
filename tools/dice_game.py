#!/usr/bin/env python3
"""
骰子游戏 - 对话式骰子游戏引擎
所有选项和结果都通过对话文本输出，不依赖任何 UI 弹窗。
"""

import random
import sys
import json


def roll_dice(count=1, sides=6):
    """掷骰子，返回结果列表"""
    return [random.randint(1, sides) for _ in range(count)]


def format_dice_result(results, sides):
    """格式化骰子结果为对话文本"""
    dice_faces_d6 = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}

    lines = []
    lines.append(f"🎲 掷出了 {len(results)} 个 D{sides}：")
    lines.append("")

    for i, val in enumerate(results, 1):
        if sides == 6:
            face = dice_faces_d6.get(val, str(val))
            lines.append(f"  第 {i} 个：{face}  ({val})")
        else:
            lines.append(f"  第 {i} 个：{val}")

    total = sum(results)
    lines.append("")
    lines.append(f"  总计：{total}")

    if len(results) > 1:
        lines.append(f"  最大：{max(results)}  最小：{min(results)}")
        lines.append(f"  平均：{total / len(results):.1f}")

    return "\n".join(lines)


def show_menu():
    """输出对话式主菜单"""
    menu = """
🎲 骰子游戏

请选择你想玩的模式（回复数字即可）：

  1️⃣  快速掷骰 — 直接掷一个六面骰
  2️⃣  自定义掷骰 — 选择骰子数量和面数
  3️⃣  大小猜测 — 猜大小，看运气
  4️⃣  骰子决斗 — 和 AI 比大小
  5️⃣  幸运数字 — 猜一个数字，看能不能掷中

直接回复 1-5 的数字就好！
""".strip()
    print(menu)


def show_custom_dice_options():
    """输出自定义掷骰的对话式选项"""
    options = """
🎯 自定义掷骰

先选骰子面数（回复数字）：

  1️⃣  D4  — 四面骰
  2️⃣  D6  — 六面骰（标准）
  3️⃣  D8  — 八面骰
  4️⃣  D10 — 十面骰
  5️⃣  D12 — 十二面骰
  6️⃣  D20 — 二十面骰（TRPG 经典）
  7️⃣  D100 — 百面骰

选好面数后，再告诉我要掷几个（1-10）。
或者直接说 "3d20" 这样的格式也行！
""".strip()
    print(options)


def show_guess_options(sides=6):
    """输出猜大小的对话式选项"""
    mid = sides * 3 / 2  # 3个骰子的中间值
    options = f"""
🔮 大小猜测

我会掷 3 个 D{sides}（总点数范围 3-{sides * 3}），{mid:.0f} 为分界线。

请猜（回复文字即可）：

  📈 大 — 总点数 > {mid:.0f}
  📉 小 — 总点数 ≤ {mid:.0f}

回复「大」或「小」就好！
""".strip()
    print(options)


def play_guess(guess, sides=6):
    """玩猜大小游戏"""
    results = roll_dice(3, sides)
    total = sum(results)
    mid = sides * 3 / 2

    print(format_dice_result(results, sides))
    print()

    is_big = total > mid
    guess_big = guess in ["大", "big", "大的", "high"]

    if is_big == guess_big:
        print(f"🎉 猜对了！总点数 {total}，是{'大' if is_big else '小'}！")
    else:
        print(f"😅 猜错了！总点数 {total}，是{'大' if is_big else '小'}。")

    print()
    print("还想再玩吗？回复以下选项：")
    print("  🔄 再来一局")
    print("  🏠 回到主菜单")


def play_duel(sides=6):
    """骰子决斗"""
    player = roll_dice(1, sides)
    ai = roll_dice(1, sides)

    print(f"⚔️ 骰子决斗！（D{sides}）")
    print()
    print(f"  你的骰子：{player[0]}")
    print(f"  AI 骰子：{ai[0]}")
    print()

    if player[0] > ai[0]:
        print("🏆 你赢了！")
    elif player[0] < ai[0]:
        print("💀 AI 赢了！")
    else:
        print("🤝 平局！")

    print()
    print("还想再玩吗？回复以下选项：")
    print("  🔄 再来一局")
    print("  🏠 回到主菜单")


def play_lucky_number(guess, sides=6):
    """幸运数字游戏"""
    result = roll_dice(1, sides)

    print(f"🍀 幸运数字（D{sides}）")
    print()
    print(f"  你猜的数字：{guess}")
    print(f"  掷出的数字：{result[0]}")
    print()

    if result[0] == guess:
        print("🎉🎉🎉 完美命中！你是今天的幸运儿！")
    elif abs(result[0] - guess) == 1:
        print("😮 就差一点点！好接近啊！")
    else:
        print(f"😅 没猜中，差了 {abs(result[0] - guess)} 点。")

    print()
    print("还想再玩吗？回复以下选项：")
    print("  🔄 再来一局")
    print("  🏠 回到主菜单")


def show_lucky_number_prompt(sides=6):
    """输出幸运数字的对话式提示"""
    prompt = f"""
🍀 幸运数字

我会掷一个 D{sides}，你来猜会是几！

请回复 1-{sides} 之间的任意数字。
""".strip()
    print(prompt)


def main():
    """命令行入口，支持各种子命令"""
    if len(sys.argv) < 2:
        show_menu()
        return

    action = sys.argv[1]

    if action == "menu":
        show_menu()

    elif action == "quick":
        results = roll_dice(1, 6)
        print(format_dice_result(results, 6))
        print()
        print("还想再玩吗？回复以下选项：")
        print("  🔄 再掷一次")
        print("  🏠 回到主菜单")

    elif action == "custom-options":
        show_custom_dice_options()

    elif action == "roll":
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        sides = int(sys.argv[3]) if len(sys.argv) > 3 else 6
        count = max(1, min(count, 10))
        sides = max(2, min(sides, 100))
        results = roll_dice(count, sides)
        print(format_dice_result(results, sides))
        print()
        print("还想再玩吗？回复以下选项：")
        print("  🔄 再掷一次（同样设定）")
        print("  🎯 换个设定")
        print("  🏠 回到主菜单")

    elif action == "guess-options":
        sides = int(sys.argv[2]) if len(sys.argv) > 2 else 6
        show_guess_options(sides)

    elif action == "guess":
        guess = sys.argv[2] if len(sys.argv) > 2 else "大"
        sides = int(sys.argv[3]) if len(sys.argv) > 3 else 6
        play_guess(guess, sides)

    elif action == "duel":
        sides = int(sys.argv[2]) if len(sys.argv) > 2 else 6
        play_duel(sides)

    elif action == "lucky-options":
        sides = int(sys.argv[2]) if len(sys.argv) > 2 else 6
        show_lucky_number_prompt(sides)

    elif action == "lucky":
        guess = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        sides = int(sys.argv[3]) if len(sys.argv) > 3 else 6
        play_lucky_number(guess, sides)

    else:
        print(f"未知操作：{action}")
        show_menu()


if __name__ == "__main__":
    main()
