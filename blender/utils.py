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
        params.append(("rotation", rotation))

    for k, v in params:
        setattr(strip.transform, k, v)
        strip.transform.keyframe_insert(data_path=k, frame=frame)


def get_screen_size(context):
    render = context.scene.render
    return (render.resolution_x, render.resolution_y)


def get_fps() -> float:
    render = bpy.context.scene.render
    return render.fps / render.fps_base
