from manimlib import *
import pdb


class Poem(Scene):
    def construct(self):
        poem = ["明月松间照清泉", "石上流", "竹喧归浣女", "莲动下渔舟"]
        fadein_time = 10
        hold_time = 1.5
        fadeout_time = 1.0
        direction = "V"
        reverse = True
        align = "head"
        font = "LXGW WenKai"
        font_size = 60
        color = "#2B2B2B"

        self.camera.background_rgba = [1, 1, 1, 1]

        lines = VGroup()
        all_chars = VGroup()

        for sentence in poem:
            chars = VGroup(
                *[
                    Text(
                        char,
                        font=font,
                        font_size=font_size,
                        weight=BOLD,
                    ).set_color(color)
                    for char in sentence
                ]
            )
            if direction == "V":
                chars.arrange(DOWN, buff=0.2)
            else:
                chars.arrange(RIGHT, buff=0.2)
            lines.add(chars)
            all_chars.add(*chars)

        if direction == "V":
            if align == "head":
                aligned_edge = UP
            elif align == "tail":
                aligned_edge = DOWN
            else:
                aligned_edge = ORIGIN
            lines.arrange(
                LEFT if reverse else RIGHT,
                buff=0.2,
                aligned_edge=aligned_edge,
            )
        else:
            if align == "head":
                aligned_edge = LEFT
            elif align == "tail":
                aligned_edge = RIGHT
            else:
                aligned_edge = ORIGIN
            lines.arrange(
                UP if reverse else DOWN,
                buff=0.2,
                aligned_edge=aligned_edge,
            )

        total_chars = len(all_chars)
        ch_time = fadein_time / max(total_chars, 1)
        # pdb.set_trace()

        self.play(
            LaggedStart(
                *[
                    FadeIn(char, shift=DOWN * 0.1, run_time=ch_time)
                    for char in all_chars
                ],
                lag_ratio=1,
            )
        )

        self.wait(hold_time)

        self.play(FadeOut(all_chars, run_time=fadeout_time, shift=DOWN * 0.1))
