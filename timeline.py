from manimlib import *
import pdb


def read_images(image_dir):
    image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff")
    list = []
    for filename in os.listdir(image_dir):
        old_path = os.path.join(image_dir, filename)
        if os.path.isfile(old_path) and filename.lower().endswith(image_extensions):
            try:
                with Image.open(old_path) as img:
                    width, height = img.size
                    list.append(
                        {
                            "file": filename,
                            "width": width,
                            "height": height,
                        }
                    )
            except Exception as e:
                print(f"fail to open {filename}: {e}")
    return list


class Timeline(Scene):
    def construct(self):
        self.camera.background_rgba = [242, 242, 242, 255]
        frame_width = self.camera.get_frame_width()
        frame_height = self.camera.get_frame_height()

        # ----- Image Begin -----
        people_dir = "assets/people"
        images = read_images(people_dir)
        random.shuffle(images)
        col_width = frame_width / 5
        img_cols = [0, 0, 0, 0, 0]
        last_imgs = [None, None, None, None, None]
        img_group = Group().set_z_index(0)
        for img in images:
            img_obj = ImageMobject(os.path.join(people_dir, img["file"]))
            img_obj.set_width(col_width)
            self.add(img_obj)
            idx = img_cols.index(min(img_cols))
            if last_imgs[idx] is None:
                img_obj.to_corner(UL, buff=0).shift(RIGHT * idx * col_width)
            else:
                img_obj.next_to(last_imgs[idx], DOWN, buff=0)
            last_imgs[idx] = img_obj
            img_cols[idx] += img_obj.get_height()
            img_group.add(img_obj)
            # pdb.set_trace()
        img_group_offset = UP * (min(frame_height * 2, min(img_cols) - frame_height))
        img_group.shift(TOP * frame_height)
        # pdb.set_trace()
        # ----- Image End -----

        # ----- Timeline Background -----
        tlbg = (
            Rectangle(
                frame_width,
                2.5,
                stroke_width=0,
                fill_color=BLACK,
                fill_opacity=0.8,
            )
            .to_edge(DOWN)
            .set_z_index(1)
        )
        self.add(tlbg)
        # ----- Timeline Background -----

        # ----- Timeline Begin -----
        start_time = (2009, 1)
        end_time = (2025, 9)
        reversed = start_time[0] > end_time[0] or (
            start_time[0] == end_time[0] and start_time[1] > end_time[1]
        )
        if reversed:
            st = end_time
            et = start_time
        else:
            st = start_time
            et = end_time

        frame_size = 30
        unit = RIGHT * (frame_width / frame_size)
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
                bar = Line(
                    BOTTOM + UP + DOWN * (0.2 if m == 7 or m == 6 else 0),
                    BOTTOM + UP * (2 if is_year else 1.4),
                    stroke_width=6,
                    color=WHITE,
                ).shift(unit * c)
                if y == start_time[0] and m == start_time[1]:
                    st_bar = bar
                if y == end_time[0] and m == end_time[1]:
                    et_bar = bar
                c += 1
                bar_label = (
                    Text(label, font="American Typewriter").scale(1.5).next_to(bar, UP)
                )
                self.add(bar)
                if is_year:
                    self.add(bar_label)
                    g = Group(bar, bar_label)
                    times.append(g)
                else:
                    times.append(bar)
        st_bar.set_color(RED)
        time_group = (
            Group(*times)
            .shift(
                LEFT * (frame_width / 2 + _shift_offset)
                if reversed
                else LEFT * frame_width / 2
            )
            .set_y(tlbg.get_y())
            .set_z_index(2)
        )
        # ----- Timeline End -----

        self.play(
            FadeIn(img_group, shift=DOWN),
            FadeIn(tlbg, shift=UP),
            FadeIn(time_group, shift=UP),
            run_time=1,
        )
        self.play(
            # img_group.animate.shift(img_group_offset),
            time_group.animate.shift(shift_offset),
            run_time=2,
            rate_func=smooth,
        )
        self.play(FadeToColor(st_bar, WHITE), FadeToColor(et_bar, RED), run_time=0.4)
        self.wait(1)
        self.play(
            FadeOut(img_group, shift=UP),
            FadeOut(tlbg, shift=DOWN),
            FadeOut(time_group, shift=DOWN),
            run_time=1,
        )
