# pyright: reportMissingModuleSource=false
# pyright: reportInvalidTypeForm=false

bl_info = {
    "name": "Video in-out",
    "author": "Jiaju",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "Video Sequencer > Sidebar",
    "description": "Add in-out frames for video",
    "category": "Sequencer",
}

import bpy
from bpy.props import (
    FloatProperty,
    PointerProperty,
)
from utils import *


class JFInOutProps(bpy.types.PropertyGroup):
    pre_fade_time: FloatProperty(
        name="Fade",
        description="",
        default=1.0,
        min=0.1,
        step=10,
        precision=2,
    )
    pre_keep_time: FloatProperty(
        name="Keep",
        description="",
        default=0.0,
        min=0.0,
    )
    post_fade_time: FloatProperty(
        name="Fade",
        description="",
        default=1.0,
        min=0.1,
        step=10,
        precision=2,
    )
    post_keep_time: FloatProperty(
        name="Keep",
        description="",
        default=0.0,
        min=0.0,
    )


class VSE_OT_insert(bpy.types.Operator):
    bl_idname = "jf.vio_insert"
    bl_label = "Add Video in-out Frames"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        seq = scene.sequence_editor
        props = scene.jf_vio_props
        fps = get_fps()

        strips = [s for s in seq.sequences if s.select and s.type == "MOVIE"]

        if not strips:
            self.report({"ERROR"}, "No movie strip selected")
            return {"CANCELLED"}
        elif len(strips) > 1:
            self.report({"ERROR"}, "Only one movie strip is allowed")
            return {"CANCELLED"}

        pre_ext_len = int((props.pre_fade_time + props.pre_keep_time) * fps)
        post_ext_len = int((props.post_fade_time + props.post_keep_time) * fps)

        strip = strips[0]
        ok = check_free_space(seq, strip, free_pre=pre_ext_len, free_post=post_ext_len)
        if not ok:
            self.report({"ERROR"}, "No enough space for extent")
            return {"CANCELLED"}

        strip.frame_offset_start -= pre_ext_len
        strip.frame_offset_end -= post_ext_len

        insert_keyframe(strip, frame=strip.frame_final_start, alpha=0.0)
        insert_keyframe(
            strip, frame=strip.frame_final_start + props.pre_fade_time * fps, alpha=1.0
        )
        insert_keyframe(
            strip, frame=strip.frame_final_end - props.post_fade_time * fps, alpha=1.0
        )
        insert_keyframe(strip, frame=strip.frame_final_end - 1, alpha=0.0)

        return {"FINISHED"}


class VSE_PT_VIO(bpy.types.Panel):
    bl_label = "Video in-out"
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Jellyfish"

    def draw(self, context):
        layout = self.layout
        props = context.scene.jf_vio_props

        pre_box = layout.box()
        pre_box.label(text="Pre")
        col = pre_box.column(align=True)
        col.prop(props, "pre_fade_time")
        col.prop(props, "pre_keep_time")

        post_box = layout.box()
        post_box.label(text="Post")
        col = post_box.column(align=True)
        col.prop(props, "post_fade_time")
        col.prop(props, "post_keep_time")

        layout.operator("jf.vio_insert", text="Insert")


classes = (
    JFInOutProps,
    VSE_OT_insert,
    VSE_PT_VIO,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.jf_vio_props = PointerProperty(type=JFInOutProps)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.jf_vio_props


if __name__ == "__main__":
    register()
