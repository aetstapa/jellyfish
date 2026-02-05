from manimlib import *
import random
import pdb
from PIL import Image

# poem = ["处世若大梦", "胡为劳其生", "所以终日醉", "颓然卧前楹"]
# total_read_time = 10.4
# total_hold_time = 7.7
# poem = ["人生得意须尽欢", "莫使金樽空对月", "天生我材必有用", "千金散尽还复来"]
# total_read_time = 13.6
# total_hold_time = 15
# poem = [
#     "日照锦城头",
#     "朝光散花楼",
#     "金窗夹绣户",
#     "珠箔悬银钩",
#     "飞梯绿云中",
#     "极目散我忧",
#     "暮雨向三峡",
#     "春江绕双流",
#     "今来一登望",
#     "如上九天游",
# ]
# total_read_time = 22.67
# total_hold_time = 5
# poem = ["蜀国多仙山", "峨眉邈难匹", "周流试登览", "绝怪安可悉"]
# total_read_time = 8.7
# total_hold_time = 2
# poem = [
#     "渡远荆门外",
#     "来从楚国游",
#     "山随平野尽",
#     "江入大荒流",
#     "月下飞天镜",
#     "云生结海楼",
#     "仍怜故乡水",
#     "万里送行舟",
# ]
# total_read_time = 18.17
# total_hold_time = 2
# poem = [
#     "吾爱孟夫子",
#     "风流天下闻",
#     "红颜弃轩冕",
#     "白首卧松云",
#     "醉月频中圣",
#     "迷花不事君",
#     "高山安可仰",
#     "徒此揖清芬",
# ]
# total_read_time = 18.93
# total_hold_time = 8.77
# poem = ["日照香炉生紫烟", "遥看瀑布挂前川", "飞流直下三千尺", "疑是银河落九天"]
# total_read_time = 18.93
# total_hold_time = 8.77
# poem = ["吴会一浮云", "飘如远行客", "功业莫从就", "岁光屡奔迫"]
# total_read_time = 9.17
# total_hold_time = 2
# poem = ["三百六十日", "日日醉如泥", "虽为李白妇", "何异太常妻"]
# total_read_time = 7.83
# total_hold_time = 2
poem = [
    "窃疑魏洽",
    "便欲趋就",
    "临然举鞭",
    "迟疑之间",
    "未及回避",
    "且理有疑误而成过",
    "事有形似而类真",
    "惟大雅含弘",
    "方能恕之也",
]
total_read_time = 3.6
total_hold_time = 9.77

bg_img = "assets/poem-bg.jpg"
# bg_img = "assets/dog.jpg"


class Poem(Scene):
    def construct(self):
        fade_time = 0.8
        read_time = total_read_time - fade_time
        hold_time = total_hold_time - fade_time
        direction = "V"
        # font = "Songti SC"
        # font = "LXGW WenKai"
        font = "Kaiti SC"
        font_size = 60
        char_cell_width = 1.2
        char_cell_height = 0.8
        # color = "#2B2B2B"
        color = "#1F1F1F"

        img = Image.open(bg_img)
        bg = ImageMobject(bg_img)
        bg.scale(
            img.width / (self.camera.get_pixel_width() / FRAME_WIDTH * bg.get_width())
        )
        bg_ow, bg_oh = bg.get_width(), bg.get_height()
        print(bg_ow, bg_oh)
        if bg_ow < FRAME_WIDTH or bg_oh < FRAME_HEIGHT:
            r1 = bg_ow / bg_oh
            r2 = FRAME_WIDTH / FRAME_HEIGHT
            if r1 > r2:
                bg.set_height(FRAME_HEIGHT)
            else:
                bg.set_width(FRAME_WIDTH)
        bg_speed = 0.05
        total_time = total_read_time + total_hold_time
        max_move_distance = bg_speed * total_time
        dx = min(bg.get_width() - FRAME_WIDTH, max_move_distance)
        dy = min(bg.get_height() - FRAME_HEIGHT, max_move_distance)
        x_dir = LEFT if random.choice([True, False]) else RIGHT
        y_dir = UP if random.choice([True, False]) else DOWN
        distance = x_dir * dx + y_dir * dy
        bg.shift(-distance / 2)
        d_fade = fade_time / total_time * distance
        d_read = read_time / total_time * distance
        d_hold = hold_time / total_time * distance
        # pdb.set_trace()

        chars = VGroup()
        for i, sentence in enumerate(poem):
            for j in range(len(sentence)):
                ch = sentence[j]
                cell = Rectangle(
                    width=char_cell_width,
                    height=char_cell_height,
                    stroke_width=0,
                )
                char = Text(ch, font=font, font_size=font_size, fill_color=color)
                char.move_to(cell.get_center())
                char_cell = VGroup(cell, char)
                target = (
                    [-i * char_cell_width, -j * char_cell_height, 0]
                    if direction == "V"
                    else [j * char_cell_width, -i * char_cell_height, 0]
                )
                char_cell.move_to(target)
                chars.add(char_cell)
        chars.move_to(ORIGIN)

        total_chars = len(chars)
        ch_time = read_time / max(total_chars, 1)
        # pdb.set_trace()

        self.play(
            FadeIn(bg),
            bg.animate(rate_func=linear).shift(d_fade),
            run_time=fade_time,
        )

        self.play(
            LaggedStart(
                *[FadeIn(char, shift=DOWN * 0.1, run_time=ch_time) for char in chars],
                lag_ratio=1,
            ),
            bg.animate(rate_func=linear).shift(d_read),
            run_time=read_time,
        )

        self.play(
            bg.animate(rate_func=linear).shift(d_hold),
            run_time=hold_time,
        )

        self.play(
            FadeOut(chars, scale=1.5),
            FadeOut(bg, shift=d_fade, rate_func=linear),
            run_time=fade_time,
        )


if __name__ == "__main__":
    from base import *

    cook(Poem, basename=poem[0])
