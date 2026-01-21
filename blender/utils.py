import math, bpy


def insert_keyframe(
    strip,
    frame: tuple[int, int],
    alpha: tuple[float, float] | None = None,
    pos: tuple[(int, int), (int, int)] | None = None,
    rotation: tuple[float, float] | None = None,
    scale: tuple[float, float] | None = None,
):
    params = (
        [
            (frame[0], "blend_alpha", alpha[0]),
            (frame[1], "blend_alpha", alpha[1]),
        ]
        if alpha
        else []
    )
    for f, k, v in params:
        setattr(strip, k, v)
        strip.keyframe_insert(data_path=k, frame=f)

    params = (
        (
            []
            if scale is None
            else [
                (frame[0], "scale_x", scale[0]),
                (frame[0], "scale_y", scale[0]),
                (frame[1], "scale_x", scale[1]),
                (frame[1], "scale_y", scale[1]),
            ]
        )
        + (
            []
            if pos is None
            else [
                (frame[0], "offset_x", pos[0][0]),
                (frame[0], "offset_y", pos[0][1]),
                (frame[1], "offset_x", pos[1][0]),
                (frame[1], "offset_y", pos[1][1]),
            ]
        )
        + (
            []
            if rotation is None
            else [
                (frame[0], "rotation", math.radians(rotation[0])),
                (frame[1], "rotation", math.radians(rotation[1])),
            ]
        )
    )

    for f, k, v in params:
        setattr(strip.transform, k, v)
        strip.transform.keyframe_insert(data_path=k, frame=f)


def get_screen_size(context):
    render = context.scene.render
    return (render.resolution_x, render.resolution_y)


def get_fps() -> float:
    render = bpy.context.scene.render
    return render.fps / render.fps_base
