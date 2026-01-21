from manimlib import *
from PIL import Image
import pdb

PIECE_WIDTH = FRAME_WIDTH / 2
PIECE_HEIGHT = FRAME_HEIGHT / 2
ANIM_TIME = 2


class Timeline(Scene):

    def render_shadow(self, obj, layers=10, max_opacity=0.2, offset=0.1):
        shadows = VGroup()
        for i in range(layers):
            s = obj.copy()
            s.set_fill(BLACK, opacity=max_opacity / layers)
            s.set_stroke(width=0)
            # 每一层逐渐扩大并偏移，模拟模糊感
            s.scale(1 + i * 0.01)
            s.shift(offset * DOWN + offset * RIGHT)
            shadows.add(s)
        return shadows

    def construct(self):
        self.camera.background_rgba = [1, 1, 1, 1]

        start_time = (700, 1)
        end_time = (701, 1)
        reversed = start_time[0] > end_time[0] or (
            start_time[0] == end_time[0] and start_time[1] > end_time[1]
        )

        colors = ["#98FB98", "#B19CD9", "#C04000", "#002366"]
        colors1 = ["#FFB7C5", "#77B5FE", "#E3A857", "#800020"]
        colors2 = ["#FFF44F", "#AAF0D1", "#6B8E23", "#2F4F4F"]
        seasons = VGroup()
        radius = ((FRAME_WIDTH / 2) ** 2 + (FRAME_HEIGHT / 2) ** 2) ** 0.5
        offset_angle = PI / 8

        for i in range(4):
            piece = AnnularSector(
                start_angle=i * PI / 2 + offset_angle,
                angle=PI / 2,
                inner_radius=0,
                outer_radius=radius,
                stroke_width=0,
                fill_color=colors[i],
            )
            seasons.add(piece)

        # ----- Timeline Begin -----
        if reversed:
            st = end_time
            et = start_time
        else:
            st = start_time
            et = end_time

        frame_size = 30
        unit = RIGHT * (FRAME_WIDTH / frame_size)
        _shift_offset = unit * (
            et[1] - st[1]
            if st[0] == et[0]
            else 13 - st[1] + et[1] - 1 + (et[0] - st[0] - 1) * 12
        )
        shift_offset = (RIGHT if reversed else LEFT) * _shift_offset

        m = st[1] - int(frame_size / 2)
        st = (st[0], m) if m > 0 else (st[0] - 1 + int(m / 12), +m % -12 + 12)
        m = et[1] + int(frame_size / 2)
        et = (et[0], m) if m <= 12 else (et[0] + int(m / 12), m % 12 + 1)
        # pdb.set_trace()

        c = 0
        times = []
        st_bar = None
        et_bar = None
        for y in range(st[0], et[0] + 1):
            m1 = st[1] if y == st[0] else 1
            m2 = et[1] if y == et[0] else 12
            for m in range(m1, m2 + 1):
                label = f"{y}" if m == 1 else f"{m}"
                is_year = m == 1
                is_middle_month = m == 7 or m == 6
                bar_h = 1.2 if is_year else (1 if is_middle_month else 0.6)
                bar = (
                    Rectangle(width=0.15, height=bar_h)
                    .set_stroke(width=0)
                    .set_fill(WHITE, opacity=1)
                    .move_to(BOTTOM + UP)
                    .shift(unit * c)
                )
                if is_year:
                    bar.shift(UP * 0.3)
                if is_middle_month:
                    bar.shift(DOWN * 0.2)
                if y == start_time[0] and m == start_time[1]:
                    st_bar = bar
                if y == end_time[0] and m == end_time[1]:
                    et_bar = bar
                bar_shadow = self.render_shadow(bar)
                c += 1
                bar_label = Text(
                    label, font="American Typewriter", font_size=60
                ).next_to(bar, UP)
                # self.add(bar)
                if is_year:
                    bar_lablel_shadow = self.render_shadow(bar_label)
                    # self.add(bar_lablel_shadow, bar_label)
                    times.append(bar_shadow)
                    g = Group(bar, bar_lablel_shadow, bar_label)
                    times.append(g)
                else:
                    times.append(bar_shadow)
                    times.append(bar)
        st_bar.set_color(RED)
        time_group = (
            Group(*times)
            .shift(
                LEFT * (FRAME_WIDTH / 2 + _shift_offset)
                if reversed
                else LEFT * FRAME_WIDTH / 2
            )
            .set_z_index(2)
        )
        # ----- Timeline End -----

        direction = 1 if reversed else -1
        self.play(
            FadeIn(seasons),
            Rotate(seasons, angle=PI / 2 * direction),
            FadeIn(time_group, shift=UP),
            run_time=1,
        )
        self.play(
            Rotate(seasons, angle=PI * 5 * direction),
            *[v.animate.set_fill(colors2[i]) for i, v in enumerate(seasons)],
            time_group.animate.shift(shift_offset),
            run_time=ANIM_TIME,
            rate_func=smooth,
        )
        self.play(FadeToColor(st_bar, WHITE), FadeToColor(et_bar, RED), run_time=0.4)
        self.wait(1)
        self.play(
            FadeOut(seasons),
            Rotate(seasons, angle=PI / 2 * direction),
            FadeOut(time_group, shift=DOWN),
            run_time=1,
        )
