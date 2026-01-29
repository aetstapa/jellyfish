from manimlib import *


class Warning(Scene):
    def construct(self):
        # FAFAFA
        self.camera.background_rgba = [250 / 255, 250 / 255, 250 / 255, 1]
        self.camera.fps = 30

        font_size = 40
        font_color = "#0F1419"
        # font_family = "LXGW WenKai"
        font_family = "Kaiti SC"

        rules = [
            "1、内部康复资料，私自观看，后果自负，本院概不负责",
            "2、很多知识是现学现卖，难免出错，请各位病友秉持怀疑之神经",
            "3、内容有点荒诞庸俗，请不满十八岁的大宝贝在父母陪同下观看",
        ]

        bg = ImageMobject("assets/slingshot1.png", height=6).move_to(ORIGIN)
        self.add(bg)
        title = (
            Text(
                "Glass Warning",
                font=font_family,
                font_size=font_size * 2,
                weight=BOLD,
            )
            .set_color(font_color)
            .move_to(UP * 2)
        )
        self.play(FadeIn(title, shift=DOWN * 1))
        self.wait(0.4)

        lines = VGroup()
        for r in rules:
            lines.add(
                Text(r, font=font_family, font_size=font_size).set_color(font_color)
            )
        lines.arrange(DOWN, buff=0.5, aligned_edge=LEFT).next_to(
            title, direction=DOWN, buff=1
        )
        self.play(LaggedStart(*[FadeIn(line, shift=UP) for line in lines], lag_ratio=2))

        signature = (
            Text("院长：猴弹玻", font=font_family, font_size=font_size)
            .set_color(font_color)
            .to_corner(DR)
        )
        self.play(FadeIn(signature, shift=LEFT))

        self.wait(5)

        self.play(
            FadeOut(title, shift=UP),
            FadeOut(lines, shift=DOWN),
            FadeOut(signature, shift=RIGHT),
            FadeOut(bg, scale=0.2),
        )


if __name__ == "__main__":
    from base import *

    cook(
        Warning,
        basename="warning",
    )
