import math, bpy


def insert_keyframe(
    strip,
    frame: int,
    alpha: float | None = None,
    offset_x: int | None = None,
    offset_y: int | None = None,
    scale_x: float | None = None,
    scale_y: float | None = None,
    scale: float | None = None,
    rotation: float | None = None,
):
    if alpha is not None:
        setattr(strip, "blend_alpha", alpha)
        strip.keyframe_insert(data_path="blend_alpha", frame=frame)
    params = []
    if offset_x is not None:
        params.append(("offset_x", offset_x))
    if offset_y is not None:
        params.append(("offset_y", offset_y))
    if scale_x is not None:
        params.append(("scale_x", scale_x))
    if scale_y is not None:
        params.append(("scale_y", scale_y))
    if scale is not None:
        params.append(("scale_x", scale))
        params.append(("scale_y", scale))
    if rotation is not None:
        params.append(("rotation", math.radians(rotation)))

    for k, v in params:
        setattr(strip.transform, k, v)
        strip.transform.keyframe_insert(data_path=k, frame=frame)


def get_screen_size(context):
    render = context.scene.render
    return (render.resolution_x, render.resolution_y)


def get_fps() -> float:
    render = bpy.context.scene.render
    return round(render.fps / render.fps_base)


def read_img_size(filepath: str) -> tuple[int, int]:
    img = bpy.data.images.get(filepath)
    if img is None:
        img = bpy.data.images.load(filepath)
    return (img.size[0], img.size[1])


def check_free_space(seq, strip, free_pre: int, free_post: int):
    same_channel = [
        s for s in seq.sequences_all if s.channel == strip.channel and s != strip
    ]

    prev_end = None
    for s in same_channel:
        if s.frame_final_end <= strip.frame_final_start:
            if prev_end is None or s.frame_final_end > prev_end:
                prev_end = s.frame_final_end

    next_start = None
    for s in same_channel:
        if s.frame_final_start >= strip.frame_final_end:
            if next_start is None or s.frame_final_start < next_start:
                next_start = s.frame_final_start

    pre_gap = (
        strip.frame_final_start - prev_end if prev_end is not None else float("inf")
    )
    post_gap = (
        next_start - strip.frame_final_end if next_start is not None else float("inf")
    )

    ok = pre_gap >= free_pre and post_gap >= free_post

    return ok, pre_gap, post_gap
