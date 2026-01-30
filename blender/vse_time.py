bl_info = {
    "name": "Time",
    "author": "Jiaju",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "Video Sequencer > Sidebar",
    "description": "Show start, end and duration timecode (supports Preview Range)",
    "category": "Sequencer",
}

import bpy


def frame_to_timecode(frame, fps):
    total_seconds = frame / fps
    h = int(total_seconds // 3600)
    m = int((total_seconds % 3600) // 60)
    s = int(total_seconds % 60)
    f = int(round((total_seconds - int(total_seconds)) * fps))
    return f"{h:02d}:{m:02d}:{s:02d}.{f:02d}"


def frames_to_seconds(frames, fps):
    return frames / fps


def get_active_range(scene):
    """返回 (start, end, is_preview)"""
    if scene.use_preview_range:
        return (scene.frame_preview_start, scene.frame_preview_end, True)
    else:
        return (scene.frame_start, scene.frame_end, False)


class VSE_PT_time_info(bpy.types.Panel):
    bl_label = "Time"
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Time"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        fps = scene.render.fps / scene.render.fps_base
        start, end, is_preview = get_active_range(scene)

        duration_frames = end - start + 1
        duration_seconds = frames_to_seconds(duration_frames, fps)

        if is_preview:
            layout.label(text="Preview Range", icon="PREVIEW_RANGE")
        else:
            layout.label(text="Scene Range", icon="SCENE_DATA")

        col = layout.column(align=True)
        col.label(text=f"ST: {frame_to_timecode(start, fps)}")
        col.label(text=f"ET: {frame_to_timecode(end, fps)}")
        col.label(text=f"DT: {frame_to_timecode(duration_frames, fps)}")
        col.label(text=f"DS: {duration_seconds:.2f} s")

        layout.separator()
        layout.label(text=f"Total Frames: {duration_frames}")


def register():
    bpy.utils.register_class(VSE_PT_time_info)


def unregister():
    bpy.utils.unregister_class(VSE_PT_time_info)
