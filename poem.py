from manimlib import *
import random
import pdb
from PIL import Image

# poem = ["处世若大梦", "胡为劳其生", "所以终日醉", "颓然卧前楹"]
# total_read_time = 10.4
# total_hold_time = 7.7
poem = ["人生得意须尽欢", "莫使金樽空对月", "天生我材必有用", "千金散尽还复来"]
total_read_time = 13.6
total_hold_time = 15


class Poem(Scene):
    def construct(self):
        #  FAFAFA
        self.camera.background_rgba = [250 / 255, 250 / 255, 250 / 255, 1]
        self.camera.fps = 30

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

        background_image = "assets/qmsht.jpg"
        bg_img = Image.open(background_image)
        bg_move_right = random.randint(1, 10) > 5
        bg_ow, bg_oh = bg_img.size
        r = FRAME_HEIGHT / bg_oh
        bg_w = r * bg_ow
        bg_offset = min(0.25 * bg_w, 0.25 * FRAME_WIDTH)
        bg_ox_range = (
            (bg_offset + FRAME_WIDTH / 2, bg_w - FRAME_WIDTH / 2)
            if bg_move_right
            else (FRAME_WIDTH / 2, bg_w - FRAME_WIDTH / 2 - bg_offset)
        )
        bg_x = random.uniform(*bg_ox_range)
        bg_x_range = (
            (bg_x - bg_offset - FRAME_WIDTH / 2, bg_x + FRAME_WIDTH / 2)
            if bg_move_right
            else (bg_x - FRAME_WIDTH / 2, bg_x + bg_offset + FRAME_WIDTH / 2)
        )
        # pdb.set_trace()
        crop_params = (
            int(bg_x_range[0] / r),
            0,
            int(bg_x_range[1] / r),
            bg_img.height,
        )
        poem_bg_path = "assets/poem-bg.jpg"
        bg_img.crop(crop_params).save(poem_bg_path)
        bg = ImageMobject(poem_bg_path, height=FRAME_HEIGHT).to_edge(
            RIGHT if bg_move_right else LEFT, buff=0
        )
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
        bg_move_time = read_time + hold_time + fade_time * 2
        bg_move_speed = bg_offset / bg_move_time
        bg_shift_direction = RIGHT if bg_move_right else LEFT
        # pdb.set_trace()

        self.play(
            FadeIn(bg),
            bg.animate(rate_func=linear).shift(
                bg_shift_direction * fade_time * bg_move_speed
            ),
            run_time=fade_time,
        )

        self.play(
            LaggedStart(
                *[FadeIn(char, shift=DOWN * 0.1, run_time=ch_time) for char in chars],
                lag_ratio=1,
            ),
            bg.animate(rate_func=linear).shift(
                bg_shift_direction * read_time * bg_move_speed,
            ),
            run_time=read_time,
        )

        self.play(
            bg.animate(rate_func=linear).shift(
                bg_shift_direction * hold_time * bg_move_speed
            ),
            run_time=hold_time,
        )

        self.play(
            FadeOut(chars, scale=1.5),
            FadeOut(
                bg,
                shift=bg_shift_direction * fade_time * bg_move_speed,
                rate_func=linear,
            ),
            # FadeOut(bg),
            # bg.animate(rate_func=linear).shift(
            #     bg_shift_direction * fade_time * bg_move_speed
            # ),
            run_time=fade_time,
        )


if __name__ == "__main__":
    from base import *

    cook(Poem, basename=poem[0])
