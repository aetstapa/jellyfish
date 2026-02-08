from manimlib import *

# question_text = "假如你对工资不满意，正确的做法是"
# options = [
#     "A、大骂资本家剥削劳动人民",
#     "B、老子不干了，跳槽走人",
#     "C、跟老板谈判，要求涨工资",
# ]
# question_text = "李白为什么“臭不要脸”地赞美孟浩然？"
# options = ["A、真心赞美孟浩然", "B、使用彩虹屁来获得孟浩然的好感", "C、捧杀孟浩然"]
# in_time = 20.57
# keep_time = 3
# question_text = "李白为什么要喝那么多酒？"
# options = [
#     "A、乔迁新居，心情很愉快",
#     "B、不喝酒写不出好诗",
#     "C、入赘豪门，有钱了，报复性消费",
# ]
# in_time = 17.03
# keep_time = 3
# question_text = "李白是不是故意冲撞李长史？"
# options = ["A、绝对是故意的", "B、不是"]
# in_time = 8.2
# keep_time = 9.5
# question_text = "李白应该给谁送礼？"
# options = [
#     "A、韩荆州本人",
#     "B、韩的家人：父母、夫人、小妾、子女",
#     "C、韩的部下",
#     "D、韩的朋友",
# ]
# in_time = 21.6
# keep_time = 3
# question_text = "朱买臣的前妻为什么自尽？"
# options = [
#     "A、前妻对自己的前倨后恭的行为感到后悔",
#     "B、前妻认为朱买臣是在羞辱她，受不了羞辱而自尽",
#     "C、不是自尽，而是被朱买臣谋杀",
# ]
# in_time = 24.6
# keep_time = 11.2
# question_text = "这首歌是改编自李白的那首诗？"
# options = ["A、秋登宣城谢脁北楼", "B、谢公亭", "C、宣城见杜鹃花"]
# in_time = 16
# keep_time = 3
# question_text = "李璘为什么要招募李白？"
# options = [
#     "A、李璘欣赏李白的才华",
#     "B、李璘欣赏李白的正直的品格",
#     "C、李白和李璘都姓李",
# ]
# in_time = 17
# keep_time = 2
question_text = "李白为什么两次娶前宰相的孙女？"
options = [
    "A、解决旅游产生的财政危机",
    "B、李白和两任夫人是真心相爱的",
    "C、李白牙口不好",
]
in_time = 27
keep_time = 2


class Question(Scene):
    def construct(self):
        question_time_ratio = 0.3
        question_time = in_time * question_time_ratio
        option_time = in_time * (1 - question_time_ratio) / len(options)
        out_time = 0.5

        font = "Kaiti SC"
        font_color = "#0F1419"
        question_scale = 1.2
        option_scale = 1.0
        line_spacing = 0.5

        question = Text(question_text, font=font).set_color(font_color)
        question.scale(question_scale)

        option_mobjects = []
        max_width = 0
        for opt in options:
            option_text = Text(opt, font=font).set_color(font_color)
            option_text.scale(option_scale)
            option_mobjects.append(option_text)
            max_width = max(max_width, option_text.get_width())

        options_group = VGroup(*option_mobjects)
        options_group.arrange(DOWN, buff=line_spacing)
        for opt in option_mobjects:
            opt.align_to(option_mobjects[0], LEFT)

        options_group.move_to(
            question.get_center()[0] * RIGHT + options_group.get_center()[1] * UP,
            aligned_edge=ORIGIN,
        )
        options_group.move_to(question.get_center()[0] * RIGHT)

        question.next_to(options_group, UP, buff=0.8)

        self.play(FadeIn(question, shift=DOWN), run_time=question_time)
        for opt in option_mobjects:
            # self.play(FadeIn(opt, shift=DOWN * 0.5))
            self.play(FadeIn(opt, shift=LEFT), run_time=option_time)

        self.wait(keep_time)

        self.play(
            FadeOut(question, shift=UP),
            *[
                FadeOut(o, shift=LEFT if i % 2 == 0 else RIGHT)
                for i, o in enumerate(option_mobjects)
            ],
            run_time=out_time,
        )


if __name__ == "__main__":
    from base import *

    cook(Question, basename=question_text)
