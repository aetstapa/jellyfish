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
# poem = [
#     "窃疑魏洽",
#     "便欲趋就",
#     "临然举鞭",
#     "迟疑之间",
#     "未及回避",
#     "且理有疑误而成过",
#     "事有形似而类真",
#     "惟大雅含弘",
#     "方能恕之也",
# ]
# total_read_time = 3.6
# total_hold_time = 9.77
# poem = [
#     "白：闻天下谈士相聚而言曰：生不用万户侯，但愿一识韩荆州。",
#     "何令人之景慕，一至于此耶？",
#     "岂不以有周公之风，躬吐握之事，",
#     "使海内豪俊奔走而归之，一登龙门，则声誉十倍。",
#     "所以龙盘凤逸之士，皆欲收名定价于君侯。",
#     "愿君侯不以富贵而骄之，寒贱而忽之，则三千宾中有毛遂。",
#     "使白得颖脱而出，即其人焉。",
# ]
# total_read_time = 3
# total_hold_time = 27.4
# poem = [
#     "白陇西布衣。流落楚汉。",
#     "十五好剑术，徧干诸侯。三十成文章，历抵卿相。",
#     "虽长不满七尺，而心雄万夫。",
#     "王公大臣，许与气义。此畴曩心迹，安敢不尽于君侯哉。",
# ]
# total_read_time = 3
# total_hold_time = 29
# poem = [
#     "君侯制作侔神明。德行动天地。笔参于造化。学究于天人。",
#     "幸愿开张心颜，不以长揖见拒。",
#     "必若接之以高宴，纵之以清谈，请日试万言，倚马可待。",
#     "今天下以君侯为文章之司命，人物之权衡，一经品题，便作佳士。",
#     "而君侯何惜阶前盈尺之地，不使白扬眉吐气，激昂青云耶？",
# ]
# total_read_time = 3
# total_hold_time = 12.2
# poem = [
#     "昔王子师为豫章，未下车，即辟荀慈明，既下车，又辟孔文举。",
#     "山涛作冀州，甄拔三十余人，或为侍中、尚书，先代所美。",
#     "而君侯亦荐一严恊律，入为秘书郎。",
#     "中间崔宗之、房习、祖黎昕、许莹之徒，",
#     "或以才名见知，或以清、白见赏。",
#     "白每观其衔恩抚躬，忠义奋发。",
#     "白以此感激，知君侯推赤心于诸贤腹中，",
#     "所以不归他人，而愿委身国士。傥急难有用，敢效微躯",
# ]
# total_read_time = 3
# total_hold_time = 10.5
# poem = [
#     "且人非尧舜，谁能尽善？白谟猷筹划，安能尽矜？",
#     "至于制作，积成卷轴，则欲尘秽视听，",
#     "恐雕虫小技，不合大人。",
#     "若赐观刍荛，请给以纸墨，兼人书之，",
#     "然后退归闲轩，缮写呈上。",
#     "庶青萍结绿，长价于薛、卞之门，",
#     "幸惟下流，大开奖饰。惟君侯图之。",
# ]
# total_read_time = 3
# total_hold_time = 5.4
# poem = [
#     "会稽愚妇轻买臣",
#     "余亦辞家西入秦",
#     "仰天大笑出门去",
#     "我辈岂是蓬蒿人",
# ]
# total_read_time = 10
# total_hold_time = 3
# poem = [
#     "鸡聚族以争食",
#     "凤孤飞而无邻",
#     "蝘蜓嘲龙，鱼目混珍",
#     "嫫母衣锦，西施负薪",
#     "若使巢由桎梏于轩冕兮",
#     "亦奚异于夔龙蹩躠于风尘",
#     "哭何苦而救楚",
#     "笑何夸而却秦",
#     "吾诚不能学二子",
#     "沽名矫节以耀世兮",
#     "固将弃天地而遗身",
#     "白鸥兮飞来",
#     "长与君兮相亲",
# ]
# total_read_time = 5
# total_hold_time = 12.2
# poem = [
#     "江城如画里",
#     "山晚望晴空",
#     "两水夹明镜",
#     "双桥落彩虹",
#     "人烟寒橘柚",
#     "秋色老梧桐",
#     "谁念北楼上",
#     "临风怀谢公",
# ]
# total_read_time = 17
# total_hold_time = 3
poem = [
    "朝辞白帝彩云间",
    "千里江陵一日还",
    "两岸猿声啼不住",
    "轻舟已过万重山",
]
total_read_time = 10.2
total_hold_time = 14

# bg_img = "assets/poem-bg.jpg"
bg_img = "assets/sanxia.jpg"


class Poem(Scene):
    def construct(self):
        fade_time = 0.8
        read_time = total_read_time - fade_time
        hold_time = total_hold_time - fade_time
        direction = "V"
        # font = "Songti SC"
        # font = "LXGW WenKai"
        font = "Kaiti SC"
        cell_scale = 1
        font_size = 60 * cell_scale
        char_cell_width = (1.2 if direction == "V" else 0.8) * cell_scale
        char_cell_height = (0.8 if direction == "V" else 1.2) * cell_scale
        # color = "#2B2B2B"
        color = "#1F1F1F"
        color = "#FFFFFF"
        force_bg_fit = True

        img = Image.open(bg_img)
        bg = ImageMobject(bg_img)
        bg.scale(
            img.width / (self.camera.get_pixel_width() / FRAME_WIDTH * bg.get_width())
        )
        bg_ow, bg_oh = bg.get_width(), bg.get_height()
        if force_bg_fit or (bg_ow < FRAME_WIDTH or bg_oh < FRAME_HEIGHT):
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
