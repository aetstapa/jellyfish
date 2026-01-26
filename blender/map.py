# pyright: reportMissingModuleSource=false
# pyright: reportInvalidTypeForm=false

bl_info = {
    "name": "Map",
    "author": "Jiaju",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "Video Sequencer > Sidebar",
    "description": "Insert map animations into VSE",
    "category": "Sequencer",
}

import bpy, os
from bpy.props import (
    IntProperty,
    StringProperty,
)
from utils import *


class JFMapProps(bpy.types.PropertyGroup):
    pin_path: StringProperty(
        name="Image",
        description="Select an pin image",
        subtype="FILE_PATH",
    )
    x: IntProperty(name="X", description="Pin X pixel", default=0)
    y: IntProperty(name="Y", description="Pin Y pixel", default=0)


class JF_OT_add_anim(bpy.types.Operator):
    bl_idname = "jf.map_add_anim"
    bl_label = "Add map animation"

    def execute(self, context):
        props = context.scene.jf_map_props
        if not props.pin_path:
            self.report({"WARNING"}, "Select pin image first")
            return {"FINISHED"}

        scene = bpy.context.scene
        seq = scene.sequence_editor
        if not seq:
            seq = scene.sequence_editor_create()

        fps = get_fps()
        fade_time = 0.5
        fade_frames = fps * fade_time

        selected_strips = bpy.context.selected_sequences
        if not selected_strips:
            self.report({"WARNING"}, "No strip selected")
        elif len(selected_strips) > 1:
            self.report({"WARNING"}, "Only one map image strip is allowed")
        else:
            strip = selected_strips[0]
            if strip.type == "IMAGE":
                img_strip = strip
            elif strip.type == "META" and strip.sequences[0].type == "IMAGE":
                img_strip = strip.sequences[0]
            else:
                self.report({"WARNING"}, "Invalid image strip")
                return {"FINISHED"}

            channel = strip.channel
            filepath = os.path.join(img_strip.directory, img_strip.elements[0].filename)
            duration = strip.frame_final_duration
            if duration < fade_frames * 2:
                self.report(
                    {"WARNING"},
                    f"strip duration too short, less than {fade_time * 2}s",
                )
                return {"FINISHED"}
            frame_final_start = strip.frame_final_start
            seq.sequences.remove(strip)
            strip = seq.sequences.new_image(
                name=filepath.split("/")[-1],
                filepath=filepath,
                channel=channel,
                frame_start=frame_final_start,
            )
            strip.frame_final_duration = duration

        (ow, oh) = read_img_size(filepath)
        sw, sh = get_screen_size(context)
        r1 = sw / sh
        r2 = ow / oh
        w, h = (int(sh / oh * ow), sh) if r1 >= r2 else (sw, int(sw / ow * oh))
        scale1 = w / ow
        scale2 = 1
        offset_x = (ow / 2 - props.x) * scale2
        offset_y = (props.y - oh / 2) * scale2

        insert_keyframe(
            strip,
            frame=strip.frame_final_start,
            alpha=0,
            scale=scale1,
            offset_x=0,
            offset_y=0,
        )
        insert_keyframe(
            strip,
            frame=strip.frame_final_start + fade_frames,
            alpha=1,
        )
        map_frame = min(
            strip.frame_final_start + fade_frames * 2,
            int((strip.frame_final_start + strip.frame_final_end) / 2),
        )
        insert_keyframe(
            strip,
            frame=map_frame,
            offset_x=offset_x,
            offset_y=offset_y,
            scale=scale2,
        )
        insert_keyframe(
            strip,
            frame=strip.frame_final_end - fade_frames,
            alpha=1,
        )
        insert_keyframe(
            strip,
            frame=strip.frame_final_end,
            alpha=0,
        )

        pin_w, pin_h = read_img_size(props.pin_path)
        target_pin_scale = 50 / pin_w
        pin_frame = int(map_frame - fps * 0.5)
        pin_strip = seq.sequences.new_image(
            "pin",
            filepath=props.pin_path,
            frame_start=pin_frame,
            channel=channel + 1,
        )
        pin_strip.frame_final_end = strip.frame_final_end
        insert_keyframe(
            pin_strip, frame=pin_frame, alpha=0, scale=target_pin_scale * 10
        )
        insert_keyframe(pin_strip, frame=map_frame, alpha=1, scale=target_pin_scale)
        insert_keyframe(
            pin_strip,
            frame=pin_strip.frame_final_end - fade_frames,
            alpha=1,
            scale=target_pin_scale,
        )
        insert_keyframe(pin_strip, frame=pin_strip.frame_final_end, alpha=0, scale=0)

        for s in seq.sequences_all:
            s.select = False
        strip.select = True
        pin_strip.select = True
        seq.active_strip = strip

        override = None
        for area in bpy.context.window.screen.areas:
            if area.type == "SEQUENCE_EDITOR":
                for region in area.regions:
                    if region.type == "WINDOW":
                        override = {
                            "window": bpy.context.window,
                            "screen": bpy.context.window.screen,
                            "area": area,
                            "region": region,
                            "scene": scene,
                        }
                        break
            if override:
                break

        if override is None:
            raise RuntimeError("Open Video Sequencer first")

        bpy.ops.sequencer.meta_make(override)
        self.report({"INFO"}, f"Inserted map animation")

        return {"FINISHED"}


class JF_PT_map_panel(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Jellyfish"
    bl_label = "Map"

    def draw(self, context):
        layout = self.layout
        props = context.scene.jf_map_props

        layout.prop(props, "pin_path")

        pin_row = layout.row(align=True, heading="Pin")
        pin_row.prop(props, "x")
        pin_row.prop(props, "y")

        layout.operator("jf.map_add_anim", text="Insert")


classes = [
    JFMapProps,
    JF_OT_add_anim,
    JF_PT_map_panel,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.jf_map_props = bpy.props.PointerProperty(type=JFMapProps)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.jf_map_props


if __name__ == "__main__":
    register()
