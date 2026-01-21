# pyright: reportMissingModuleSource=false
# pyright: reportInvalidTypeForm=false

bl_info = {
    "name": "Image",
    "author": "Jiaju",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "Video Sequencer > Sidebar",
    "description": "Insert image animations into VSE",
    "category": "Sequencer",
}

import bpy, math, os
from bpy.props import (
    StringProperty,
    EnumProperty,
    FloatProperty,
    IntProperty,
)
from utils import *

ANIMATE_DURATION = 0.5
SLIDE_OFFSET = 500
ZOOM_RATIO = 0.4


# --------------------------
# Properties
# --------------------------
class VSEImageAnimProperties(bpy.types.PropertyGroup):
    source: EnumProperty(
        name="Source",
        description="Image source",
        items=[
            ("FS", "File System", ""),
            ("STRIP", "Strip", ""),
        ],
        default="FS",
    )

    channel: EnumProperty(
        name="Channel",
        description="Select the channel to insert the image",
        items=[
            (str(i), f"Channel {i}", f"Insert into channel {i}") for i in range(1, 33)
        ],
        default="1",
    )

    filepath: StringProperty(
        name="Image",
        description="Select an image",
        subtype="FILE_PATH",
        update=lambda self, context: self.update_image_size(),
    )

    img_w: IntProperty(name="Image Width", default=0)
    img_h: IntProperty(name="Image Height", default=0)

    gap: IntProperty(name="Image Gap", default=100)

    in_anim: EnumProperty(
        name="Animation",
        description="Animation type when image ins",
        items=[
            ("NONE", "None", ""),
            ("FADE", "Fade In", ""),
            ("UP", "Up", ""),
            ("DOWN", "Down", ""),
            ("LEFT", "Left", ""),
            ("RIGHT", "Right", ""),
            ("Z+", "Zoom+", ""),
            ("Z-", "Zoom-", ""),
        ],
    )

    in_duration: FloatProperty(
        name="Duration",
        default=ANIMATE_DURATION,
        min=0.1,
        description="Duration of in animation (seconds)",
    )
    in_w: IntProperty(name="Width", min=0, default=0)
    in_h: IntProperty(name="Height", min=0, default=0)
    in_x: IntProperty(name="X", default=0)
    in_y: IntProperty(name="Y", default=0)
    in_alpha: FloatProperty(
        name="Alpha", min=0.0, max=1.0, default=0.0, description="Transparency"
    )
    in_rotation: FloatProperty(name="Rotation", default=0.0, description="Rotation")

    keep_duration: FloatProperty(
        name="Duration",
        default=2.0,
        min=0.1,
        description="How long to keep the image visible",
    )
    keep_w: IntProperty(name="Width", min=0, default=0)
    keep_h: IntProperty(name="Height", min=0, default=0)
    keep_x: IntProperty(name="X", default=0)
    keep_y: IntProperty(name="Y", default=0)
    keep_alpha: FloatProperty(
        name="Alpha", min=0.0, max=1.0, default=1.0, description="Transparency"
    )
    keep_rotation: FloatProperty(name="Rotation", default=0.0, description="Rotation")

    out_anim: EnumProperty(
        name="Animation",
        description="Animation type when image outs",
        items=[
            ("NONE", "None", ""),
            ("FADE", "Fade Out", ""),
            ("UP", "Up", ""),
            ("DOWN", "Down", ""),
            ("LEFT", "Left", ""),
            ("RIGHT", "Right", ""),
            ("Z+", "Zoom+", ""),
            ("Z-", "Zoom-", ""),
        ],
    )

    out_duration: FloatProperty(
        name="Duration",
        default=ANIMATE_DURATION,
        min=0.1,
        description="Duration of out animation (seconds)",
    )
    out_w: IntProperty(name="Width", min=0, default=0)
    out_h: IntProperty(name="Height", min=0, default=0)
    out_x: IntProperty(name="X", default=0)
    out_y: IntProperty(name="Y", default=0)
    out_alpha: FloatProperty(
        name="Alpha", min=0.0, max=1.0, default=0.0, description="Transparency"
    )
    out_rotation: FloatProperty(name="Rotation", default=0.0, description="Rotation")

    def update_image_size(self):
        if not self.filepath:
            return
        path = bpy.path.abspath(self.filepath)
        try:
            img = bpy.data.images.get(path)
            if img is None:
                img = bpy.data.images.load(path)
            w, h = img.size[0], img.size[1]
            self.img_w, self.img_h = w, h
            self.in_w, self.in_h = w, h
            self.keep_w, self.keep_h = w, h
            self.out_w, self.out_h = w, h
        except:
            self.img_w, self.img_h = 0, 0

    def get_screen_size(self, context):
        render = context.scene.render
        return (render.resolution_x, render.resolution_y)

    def calc_img_size_with_gap(self, context):
        if not self.filepath:
            return
        w, h = self.img_w, self.img_h
        sw, sh = self.get_screen_size(context)
        aw = min(sw - self.gap * 2, w)
        ah = min(sh - self.gap * 2, h)

        if w <= aw and h <= ah:
            return (w, h)
        r1 = aw / ah
        r2 = w / h
        return (int(ah / h * w), ah) if r1 > r2 else (aw, int(aw / w * h))


# --------------------------
# Operator
# --------------------------
class VSE_OT_read_img_strip(bpy.types.Operator):
    bl_idname = "jf.image_read_img_strip"
    bl_label = "Read Image Strip"

    def execute(self, context):
        selected_strips = bpy.context.selected_sequences
        if not selected_strips:
            self.report({"WARNING"}, "No strip selected")
        elif len(selected_strips) > 1:
            self.report({"WARNING"}, "Only one image strip is allowed")
        else:
            strip = selected_strips[0]
            if strip.type == "IMAGE":
                filepath = os.path.join(strip.directory, strip.elements[0].filename)
                props = context.scene.vse_image_anim_props
                props.filepath = filepath
                props.update_image_size()
                props.in_w, props.in_h = props.img_w, props.img_h
                props.keep_w, props.keep_h = props.img_w, props.img_h
                props.out_w, props.out_h = props.img_w, props.img_h
                fps = get_fps()
                duration = strip.frame_final_duration / fps
                if duration >= ANIMATE_DURATION * 2:
                    props.in_duration = ANIMATE_DURATION
                    props.keep_duration = duration - ANIMATE_DURATION * 2
                    props.out_duration = ANIMATE_DURATION
            else:
                self.report({"WARNING"}, "Invalid image strip")
        return {"FINISHED"}


class VSE_OT_reset_in_size(bpy.types.Operator):
    bl_idname = "jf.image_reset_in_size"
    bl_label = "Reset In Size"

    def execute(self, context):
        props = context.scene.vse_image_anim_props
        props.in_w, props.in_h = props.img_w, props.img_h
        return {"FINISHED"}


class VSE_OT_in_size_cover(bpy.types.Operator):
    bl_idname = "jf.image_in_size_cover"
    bl_label = "In Size Cover Screen"

    def execute(self, context):
        props = context.scene.vse_image_anim_props
        sw, sh = props.get_screen_size(context)
        w, h = props.img_w, props.img_h
        r1 = sw / sh
        r2 = w / h
        props.in_w, props.in_h = (
            (int(sh / h * w), sh) if r1 >= r2 else (sw, int(sw / w * h))
        )
        return {"FINISHED"}


class VSE_OT_in_size_contain(bpy.types.Operator):
    bl_idname = "jf.image_in_size_contain"
    bl_label = "In Size Contain Screen"

    def execute(self, context):
        props = context.scene.vse_image_anim_props
        sw, sh = props.get_screen_size(context)
        w, h = props.img_w, props.img_h
        r1 = sw / sh
        r2 = w / h
        props.in_w, props.in_h = (
            (int(sh / h * w), sh) if r1 <= r2 else (sw, int(sw / w * h))
        )
        return {"FINISHED"}


class VSE_OT_reset_in_size_by_gap(bpy.types.Operator):
    bl_idname = "jf.image_reset_in_size_by_gap"
    bl_label = "Reset In Size By Gap"

    def execute(self, context):
        props = context.scene.vse_image_anim_props
        props.in_w, props.in_h = props.calc_img_size_with_gap(context)
        return {"FINISHED"}


class VSE_OT_keep_size_cover(bpy.types.Operator):
    bl_idname = "jf.image_keep_size_cover"
    bl_label = "Keep Size Cover Screen"

    def execute(self, context):
        props = context.scene.vse_image_anim_props
        sw, sh = props.get_screen_size(context)
        w, h = props.img_w, props.img_h
        r1 = sw / sh
        r2 = w / h
        props.keep_w, props.keep_h = (
            (int(sh / h * w), sh) if r1 >= r2 else (sw, int(sw / w * h))
        )
        return {"FINISHED"}


class VSE_OT_keep_size_contain(bpy.types.Operator):
    bl_idname = "jf.image_keep_size_contain"
    bl_label = "Keep Size Contain Screen"

    def execute(self, context):
        props = context.scene.vse_image_anim_props
        sw, sh = props.get_screen_size(context)
        w, h = props.img_w, props.img_h
        r1 = sw / sh
        r2 = w / h
        props.keep_w, props.keep_h = (
            (int(sh / h * w), sh) if r1 <= r2 else (sw, int(sw / w * h))
        )
        return {"FINISHED"}


class VSE_OT_reset_keep_size(bpy.types.Operator):
    bl_idname = "jf.image_reset_keep_size"
    bl_label = "Reset Keep Size"

    def execute(self, context):
        props = context.scene.vse_image_anim_props
        props.keep_w, props.keep_h = props.img_w, props.img_h
        return {"FINISHED"}


class VSE_OT_reset_keep_size_by_gap(bpy.types.Operator):
    bl_idname = "jf.image_reset_keep_size_by_gap"
    bl_label = "Reset Keep Size By Gap"

    def execute(self, context):
        props = context.scene.vse_image_anim_props
        props.keep_w, props.keep_h = props.calc_img_size_with_gap(context)
        return {"FINISHED"}


class VSE_OT_reset_out_size(bpy.types.Operator):
    bl_idname = "jf.image_reset_out_size"
    bl_label = "Reset Out Size"

    def execute(self, context):
        props = context.scene.vse_image_anim_props
        props.out_w, props.out_h = props.img_w, props.img_h
        return {"FINISHED"}


class VSE_OT_out_size_cover(bpy.types.Operator):
    bl_idname = "jf.image_out_size_cover"
    bl_label = "Out Size Cover Screen"

    def execute(self, context):
        props = context.scene.vse_image_anim_props
        sw, sh = props.get_screen_size(context)
        w, h = props.img_w, props.img_h
        r1 = sw / sh
        r2 = w / h
        props.out_w, props.out_h = (
            (int(sh / h * w), sh) if r1 >= r2 else (sw, int(sw / w * h))
        )
        return {"FINISHED"}


class VSE_OT_out_size_contain(bpy.types.Operator):
    bl_idname = "jf.image_out_size_contain"
    bl_label = "Out Size Contain Screen"

    def execute(self, context):
        props = context.scene.vse_image_anim_props
        sw, sh = props.get_screen_size(context)
        w, h = props.img_w, props.img_h
        r1 = sw / sh
        r2 = w / h
        props.out_w, props.out_h = (
            (int(sh / h * w), sh) if r1 <= r2 else (sw, int(sw / w * h))
        )
        return {"FINISHED"}


class VSE_OT_reset_out_size_by_gap(bpy.types.Operator):
    bl_idname = "jf.image_reset_out_size_by_gap"
    bl_label = "Reset Out Size By Gap"

    def execute(self, context):
        props = context.scene.vse_image_anim_props
        props.out_w, props.out_h = props.calc_img_size_with_gap(context)
        return {"FINISHED"}


class VSE_OT_add_image_with_anim(bpy.types.Operator):
    bl_idname = "jf.image_add_image_anim"
    bl_label = "Add Image With Animation"
    bl_description = "Insert the selected image with in/out animations"

    def set_ease(
        self,
        strip,
        data_path,
        frame_start,
        frame_end,
        interpolation="BEZIER",
        easing="EASE_OUT",
    ):
        scene = bpy.context.scene
        if not scene.animation_data or not scene.animation_data.action:
            return
        full_path = f'sequence_editor.sequences_all["{strip.name}"].{data_path}'
        fc = scene.animation_data.action.fcurves.find(full_path)
        if fc:
            for kp in fc.keyframe_points:
                if frame_start <= kp.co.x <= frame_end:
                    kp.interpolation = interpolation
                    kp.easing = easing
            fc.update()

    def insert_keyframe(
        self,
        strip,
        frame: (int, int),
        alpha: (float, float),
        scale: (float, float),
        pos: ((int, int), (int, int)),
        rotation: (float, float),
    ):
        params = [
            (frame[0], "blend_alpha", alpha[0]),
            (frame[1], "blend_alpha", alpha[1]),
        ]
        for f, k, v in params:
            setattr(strip, k, v)
            strip.keyframe_insert(data_path=k, frame=f)
        params = [
            (frame[0], "scale_x", scale[0]),
            (frame[0], "scale_y", scale[0]),
            (frame[0], "offset_x", pos[0][0]),
            (frame[0], "offset_y", pos[0][1]),
            (frame[0], "rotation", math.radians(rotation[0])),
            (frame[1], "scale_x", scale[1]),
            (frame[1], "scale_y", scale[1]),
            (frame[1], "offset_x", pos[1][0]),
            (frame[1], "offset_y", pos[1][1]),
            (frame[1], "rotation", math.radians(rotation[1])),
        ]
        for f, k, v in params:
            setattr(strip.transform, k, v)
            strip.transform.keyframe_insert(data_path=k, frame=f)

        for p in ["blend_alpha", "transform.offset_x", "transform.offset_y"]:
            self.set_ease(strip, p, frame[0], frame[1], "BEZIER", "EASE_IN_OUT")
        for p in ["transform.scale_x", "transform.scale_y"]:
            self.set_ease(strip, p, frame[0], frame[1], "BEZIER", "EASE_OUT")
        self.set_ease(strip, "transform.rotation", frame[0], frame[1], "BEZIER", "AUTO")

    def execute(self, context):
        props = context.scene.vse_image_anim_props
        filepath = bpy.path.abspath(props.filepath)

        seq = context.scene.sequence_editor
        if not seq:
            seq = context.scene.sequence_editor_create()

        if props.in_anim != "NONE":
            props.in_duration = ANIMATE_DURATION
        in_anim = props.in_anim
        if in_anim == "NONE":
            pass
        else:
            props.in_alpha = 0
            props.in_rotation = props.keep_rotation
            if in_anim == "FADE":
                props.in_w, props.in_h = props.keep_w, props.keep_h
                props.in_x, props.y = props.keep_x, props.keep_y
            elif in_anim == "UP":
                props.in_w, props.in_h = props.keep_w, props.keep_h
                props.in_x, props.in_y = props.keep_x, props.keep_y - SLIDE_OFFSET
            elif in_anim == "DOWN":
                props.in_w, props.in_h = props.keep_w, props.keep_h
                props.in_x, props.in_y = props.keep_x, props.keep_y + SLIDE_OFFSET
            elif in_anim == "LEFT":
                props.in_w, props.in_h = props.keep_w, props.keep_h
                props.in_x, props.in_y = props.keep_x + SLIDE_OFFSET, props.keep_y
            elif in_anim == "RIGHT":
                props.in_w, props.in_h = props.keep_w, props.keep_h
                props.in_x, props.in_y = props.keep_x - SLIDE_OFFSET, props.keep_y
            elif in_anim == "Z+":
                props.in_w = int(props.keep_w * ZOOM_RATIO)
                props.in_h = int(props.keep_h * ZOOM_RATIO)
                props.in_x, props.in_y = props.keep_x, props.keep_y
            elif in_anim == "Z-":
                props.in_w = int(props.keep_w * (2 - ZOOM_RATIO))
                props.in_h = int(props.keep_h * (2 - ZOOM_RATIO))
                props.in_x, props.in_y = props.keep_x, props.keep_y
            else:
                raise ValueError(f"Unexpected in animation type: {in_anim}")

        if props.out_anim != "NONE":
            props.out_duration = ANIMATE_DURATION

        out_anim = props.out_anim
        if out_anim == "NONE":
            pass
        else:
            props.out_alpha = 0
            props.out_rotation = props.keep_rotation
            if out_anim == "FADE":
                props.out_w, props.out_h = props.keep_w, props.keep_h
                props.out_x, props.out_y = props.keep_x, props.keep_y
            elif out_anim == "UP":
                props.out_w, props.out_h = props.keep_w, props.keep_h
                props.out_x, props.out_y = props.keep_x, props.keep_y + SLIDE_OFFSET
            elif out_anim == "DOWN":
                props.out_w, props.out_h = props.keep_w, props.keep_h
                props.out_x, props.out_y = props.keep_x, props.keep_y - SLIDE_OFFSET
            elif out_anim == "LEFT":
                props.out_w, props.out_h = props.keep_w, props.keep_h
                props.out_x, props.out_y = props.keep_x - SLIDE_OFFSET, props.keep_y
            elif out_anim == "RIGHT":
                props.out_w, props.out_h = props.keep_w, props.keep_h
                props.out_x, props.out_y = props.keep_x + SLIDE_OFFSET, props.keep_y
            elif out_anim == "Z+":
                props.out_w = int(props.keep_w * (2 - ZOOM_RATIO))
                props.out_h = int(props.keep_h * (2 - ZOOM_RATIO))
                props.out_x, props.out_y = props.keep_x, props.keep_y
            elif out_anim == "Z-":
                props.out_w = int(props.keep_w * ZOOM_RATIO)
                props.out_h = int(props.keep_h * ZOOM_RATIO)
                props.out_x, props.out_y = props.keep_x, props.keep_y
            else:
                raise ValueError(f"Unexpected out animation type: {out_anim}")

        fps = get_fps()
        in_frames = int(props.in_duration * fps)
        keep_frames = int(props.keep_duration * fps)
        out_frames = int(props.out_duration * fps)

        if props.source == "STRIP":
            selected_strips = bpy.context.selected_sequences
            if not selected_strips:
                self.report({"WARNING"}, "No strip selected")
                return {"FINISHED"}
            elif len(selected_strips) > 1:
                self.report({"WARNING"}, "Only one image strip is allowed")
                return {"FINISHED"}
            else:
                strip = selected_strips[0]
                start_frame = int(strip.frame_start)
                channel = strip.channel
                seq_editor = bpy.context.scene.sequence_editor
                seq_editor.sequences.remove(strip)
        elif props.source == "FS":
            start_frame = context.scene.frame_current
            channel = int(props.channel)
        else:
            raise ValueError(f"Invalid source: {props.source}")

        img_strip = seq.sequences.new_image(
            name=filepath.split("/")[-1],
            filepath=filepath,
            channel=channel,
            frame_start=start_frame,
        )
        img_strip.frame_final_duration = in_frames + keep_frames + out_frames

        self.insert_keyframe(
            img_strip,
            frame=(start_frame, start_frame + in_frames),
            alpha=(props.in_alpha, props.keep_alpha),
            scale=(props.in_w / props.img_w, props.keep_w / props.img_w),
            pos=((props.in_x, props.in_y), (props.keep_x, props.keep_y)),
            rotation=(props.in_rotation, props.keep_rotation),
        )

        start_frame += in_frames + keep_frames
        self.insert_keyframe(
            img_strip,
            frame=(start_frame, start_frame + out_frames),
            alpha=(props.keep_alpha, props.out_alpha),
            scale=(props.keep_w / props.img_w, props.out_w / props.img_w),
            pos=((props.keep_x, props.keep_y), (props.out_x, props.out_y)),
            rotation=(props.keep_rotation, props.out_rotation),
        )

        self.report({"INFO"}, f"Inserted {filepath.split('/')[-1]}")
        return {"FINISHED"}


# --------------------------
# UI Panel
# --------------------------
class VSE_PT_image_anim_panel(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Jellyfish"
    bl_label = "Image"

    def draw(self, context):
        layout = self.layout
        props = context.scene.vse_image_anim_props

        layout.prop(props, "source")
        source_box = layout.box()
        if props.source == "FS":
            source_box.prop(props, "channel")
            source_box.prop(props, "filepath")
        else:
            source_box.operator("jf.image_read_img_strip", text="", icon="EYEDROPPER")

        ow, oh = props.img_w, props.img_h

        # -------- In --------
        in_box = layout.box()
        in_box.label(text="In", icon="TRIA_RIGHT")
        in_box.prop(props, "in_anim")
        if props.source == "FS":
            in_box.prop(props, "in_duration")
        if props.in_anim == "NONE":
            size_col = in_box.column(align=True)
            row = size_col.row(align=True)
            row.prop(props, "in_w", text="W")
            row.prop(props, "in_h", text="H")
            size_row1 = size_col.row(align=True)
            size_row1.operator(
                "jf.image_reset_in_size_by_gap", text="Gap", icon="FULLSCREEN_EXIT"
            )
            size_row1.operator("jf.image_reset_in_size", text="Reset", icon="LOOP_BACK")
            size_row2 = size_col.row(align=True)
            size_row2.operator(
                "jf.image_in_size_cover", text="Cover", icon="CLIPUV_DEHLT"
            )
            size_row2.operator(
                "jf.image_in_size_contain", text="Contain", icon="CLIPUV_HLT"
            )
            w, h = props.in_w, props.in_h
            if w > ow or h > oh:
                in_box.label(text="Out of origin size", icon="ERROR")
            pos_row = in_box.row(align=True)
            pos_row.prop(props, "in_x", text="X")
            pos_row.prop(props, "in_y", text="Y")
            row = in_box.row(align=True)
            row.prop(props, "in_alpha")
            row.prop(props, "in_rotation")

        # -------- KEEP --------
        keep_box = layout.box()
        keep_box.label(text="Keep", icon="PAUSE")
        keep_box.prop(props, "keep_duration")
        size_col = keep_box.column(align=True)
        row = size_col.row(align=True)
        row.prop(props, "keep_w", text="W")
        row.prop(props, "keep_h", text="H")
        size_row1 = size_col.row(align=True)
        size_row1.operator(
            "jf.image_reset_keep_size_by_gap", text="Gap", icon="FULLSCREEN_EXIT"
        )
        size_row1.operator("jf.image_reset_keep_size", text="Reset", icon="LOOP_BACK")
        size_row2 = size_col.row(align=True)
        size_row2.operator(
            "jf.image_keep_size_cover", text="Cover", icon="CLIPUV_DEHLT"
        )
        size_row2.operator(
            "jf.image_keep_size_contain", text="Contain", icon="CLIPUV_HLT"
        )
        w, h = props.keep_w, props.keep_h
        if w > ow or h > oh:
            keep_box.label(text="Out of origin size", icon="ERROR")
        pos_row = keep_box.row(align=True)
        pos_row.prop(props, "keep_x", text="X")
        pos_row.prop(props, "keep_y", text="Y")
        row = keep_box.row(align=True)
        row.prop(props, "keep_alpha")
        row.prop(props, "keep_rotation")

        # -------- EXIT --------
        out_box = layout.box()
        out_box.label(text="Out", icon="TRIA_LEFT")
        out_box.prop(props, "out_anim")
        if props.source == "FS":
            out_box.prop(props, "out_duration")
        if props.out_anim == "NONE":
            size_col = out_box.column(align=True)
            row = size_col.row(align=True)
            row.prop(props, "out_w", text="W")
            row.prop(props, "out_h", text="H")
            size_row1 = size_col.row(align=True)
            size_row1.operator(
                "jf.image_reset_out_size_by_gap", text="Gap", icon="FULLSCREEN_EXIT"
            )
            size_row1.operator(
                "jf.image_reset_out_size", text="Reset", icon="LOOP_BACK"
            )
            size_row2 = size_col.row(align=True)
            size_row2.operator(
                "jf.image_out_size_cover", text="Cover", icon="CLIPUV_DEHLT"
            )
            size_row2.operator(
                "jf.image_out_size_contain", text="Contain", icon="CLIPUV_HLT"
            )
            w, h = props.out_w, props.out_h
            if w > ow or h > oh:
                out_box.label(text="Out of origin size", icon="ERROR")
            pos_row = out_box.row(align=True)
            pos_row.prop(props, "out_x", text="X")
            pos_row.prop(props, "out_y", text="Y")
            row = out_box.row(align=True)
            row.prop(props, "out_alpha")
            row.prop(props, "out_rotation")

        layout.separator()
        layout.operator("jf.image_add_image_anim", text="Insert")


# --------------------------
# Register
# --------------------------
classes = [
    VSEImageAnimProperties,
    VSE_OT_read_img_strip,
    VSE_OT_add_image_with_anim,
    VSE_OT_reset_in_size,
    VSE_OT_in_size_cover,
    VSE_OT_in_size_contain,
    VSE_OT_reset_in_size_by_gap,
    VSE_OT_reset_keep_size,
    VSE_OT_keep_size_cover,
    VSE_OT_keep_size_contain,
    VSE_OT_reset_keep_size_by_gap,
    VSE_OT_reset_out_size,
    VSE_OT_out_size_cover,
    VSE_OT_out_size_contain,
    VSE_OT_reset_out_size_by_gap,
    VSE_PT_image_anim_panel,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.vse_image_anim_props = bpy.props.PointerProperty(
        type=VSEImageAnimProperties
    )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.vse_image_anim_props


if __name__ == "__main__":
    register()
