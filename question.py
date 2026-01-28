from manimlib import *


class QuestionWithOptions(Scene):
    def construct(self):
        # FAFAFA
        self.camera.background_rgba = [250 / 255, 250 / 255, 250 / 255, 1]
        self.camera.fps = 30

        question_text = "下面哪个选项是正确的？"
        options = ["A. 选项一", "B. 选项二", "C. 选项三", "D. 选项四"]
        in_time = 4
        keep_time = 5
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
            run_time=out_time
        )
