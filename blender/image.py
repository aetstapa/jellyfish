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

import bpy, os
from bpy.props import (
    StringProperty,
    EnumProperty,
    FloatProperty,
    IntProperty,
    BoolProperty,
)
from utils import *

IN_TIME = 0.8


# --------------------------
# Properties
# --------------------------
class JFImageProps(bpy.types.PropertyGroup):
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
        description="Select an image strip",
        subtype="FILE_PATH",
        update=lambda self, context: self.update_image_size(),
    )

    img_w: IntProperty(name="Image Width", default=0)
    img_h: IntProperty(name="Image Height", default=0)

    gap: IntProperty(name="Image Gap", default=100)

    anim_type: EnumProperty(
        name="Animation",
        description="Animation quick setting",
        items=[
            ("MOV_LEFT", "Move to LEFT", ""),
            ("MOV_RIGHT", "Move to RIGHT", ""),
            ("MOV_UP", "Move to UP", ""),
            ("MOV_DOWN", "Move to DOWN", ""),
            ("FADE", "Fade IN and OUT", ""),
            ("UD", "UP in, DOWN out", ""),
            ("DU", "DOWN in, UP out", ""),
            ("LR", "LEFT in, RIGHT out", ""),
            ("RL", "RIGHT in, LEFT out", ""),
            ("ZOOM+", "ZOOM+ in, ZOOM+ out", ""),
            ("ZOOM-", "ZOOM- in, ZOOM- out", ""),
        ],
        default="MOV_RIGHT",
    )

    size_type: EnumProperty(
        name="Size",
        description="Size type setting",
        items=[
            ("ORIGIN", "Origin", ""),
            ("COVER", "Cover", ""),
            ("CONTAIN", "Contain", ""),
            ("1/2w", "1/2 of width", ""),
            ("1/4w", "1/4 of width", ""),
            ("1/6w", "1/6 of width", ""),
            ("1/8w", "1/8 of width", ""),
            ("1/2w", "1/2 of height", ""),
            ("1/4w", "1/4 of height", ""),
            ("1/6w", "1/6 of height", ""),
            ("1/8w", "1/8 of height", ""),
        ],
        default="ORIGIN",
    )

    origin_type: EnumProperty(
        name="Origin",
        description="Origin position",
        items=[
            ("UL", "Up-Left", ""),
            ("U", "Up", ""),
            ("UR", "Up-Right", ""),
            ("L", "Left", ""),
            ("C", "Center", ""),
            ("R", "Right", ""),
            ("DL", "Down-Left", ""),
            ("D", "Down", ""),
            ("DR", "Down-Right", ""),
        ],
        default="C",
    )

    k1_w: IntProperty(name="Width", min=0, default=0)
    k1_h: IntProperty(name="Height", min=0, default=0)
    k1_x: IntProperty(name="X", default=0)
    k1_y: IntProperty(name="Y", default=0)
    k1_a: FloatProperty(
        name="Alpha", min=0.0, max=1.0, default=0.0, description="Transparency"
    )
    k1_r: FloatProperty(name="Rotation", default=0.0, description="Rotation")
    k1_enable_rotation: BoolProperty(name="Enable Rotation", default=True)

    k12_t: FloatProperty(
        name="Duration",
        default=IN_TIME,
        min=0.1,
        description="Duration from k1 to k2",
    )

    k2_w: IntProperty(name="Width", min=0, default=0)
    k2_h: IntProperty(name="Height", min=0, default=0)
    k2_x: IntProperty(name="X", default=0)
    k2_y: IntProperty(name="Y", default=0)
    k2_a: FloatProperty(
        name="Alpha", min=0.0, max=1.0, default=1.0, description="Transparency"
    )
    k2_r: FloatProperty(name="Rotation", default=0.0, description="Rotation")
    k2_enable_pos: BoolProperty(name="Enable Position", default=True)
    k2_enable_size: BoolProperty(name="Enable Size", default=True)
    k2_enable_alpha: BoolProperty(name="Enable Alpha", default=True)
    k2_enable_rotation: BoolProperty(name="Enable Rotation", default=True)

    k23_t: FloatProperty(
        name="Duration",
        default=2.0,
        min=0.1,
        description="Duration from k2 to k3",
    )

    k3_t: FloatProperty(
        name="Duration",
        default=IN_TIME,
        min=0.1,
        description="Duration of out animation (seconds)",
    )
    k3_w: IntProperty(name="Width", min=0, default=0)
    k3_h: IntProperty(name="Height", min=0, default=0)
    k3_x: IntProperty(name="X", default=0)
    k3_y: IntProperty(name="Y", default=0)
    k3_a: FloatProperty(
        name="Alpha", min=0.0, max=1.0, default=1.0, description="Transparency"
    )
    k3_r: FloatProperty(name="Rotation", default=0.0, description="Rotation")
    same_with_k2: BoolProperty(
        name="Same with K2", default=False, description="Same params with K2 keyframe"
    )
    k3_enable_pos: BoolProperty(name="Enable Position", default=True)
    k3_enable_size: BoolProperty(name="Enable Size", default=True)
    k3_enable_alpha: BoolProperty(name="Enable Alpha", default=True)
    k3_enable_rotation: BoolProperty(name="Enable Rotation", default=True)

    k34_t: FloatProperty(
        name="Duration",
        default=IN_TIME,
        min=0.1,
        description="Duration from k3 to k4",
    )

    k4_w: IntProperty(name="Width", min=0, default=0)
    k4_h: IntProperty(name="Height", min=0, default=0)
    k4_x: IntProperty(name="X", default=0)
    k4_y: IntProperty(name="Y", default=0)
    k4_a: FloatProperty(
        name="Alpha", min=0.0, max=1.0, default=0.0, description="Transparency"
    )
    k4_r: FloatProperty(name="Rotation", default=0.0, description="Rotation")
    k4_enable_rotation: BoolProperty(name="Enable Rotation", default=True)

    def check_filepath(self):
        if not self.filepath:
            self.report({"WARNING"}, "No strip inspected")
            return False
        return True

    def update_image_size(self):
        if not self.check_filepath():
            return
        path = bpy.path.abspath(self.filepath)
        try:
            img = bpy.data.images.get(path)
            if img is None:
                img = bpy.data.images.load(path)
            w, h = img.size[0], img.size[1]
            self.img_w, self.img_h = w, h
            self.k1_w, self.k1_h = w, h
            self.k2_w, self.k2_h = w, h
            self.k4_w, self.k4_h = w, h
        except:
            self.img_w, self.img_h = 0, 0

    def calc_gap_size(self, context):
        if not self.check_filepath():
            self.report({"WARNING"}, "No strip inspected")
            return
        w, h = self.img_w, self.img_h
        sw, sh = get_screen_size(context)
        aw = min(sw - self.gap * 2, w)
        ah = min(sh - self.gap * 2, h)

        if w <= aw and h <= ah:
            return (w, h)
        r1 = aw / ah
        r2 = w / h
        return (int(ah / h * w), ah) if r1 > r2 else (aw, int(aw / w * h))

    def calc_cover_size(self, context):
        sw, sh = get_screen_size(context)
        w, h = self.img_w, self.img_h
        r1 = sw / sh
        r2 = w / h
        return (int(sh / h * w), sh) if r1 >= r2 else (sw, int(sw / w * h))

    def calc_contain_size(self, context):
        sw, sh = get_screen_size(context)
        w, h = self.img_w, self.img_h
        r1 = sw / sh
        r2 = w / h
        return (int(sh / h * w), sh) if r1 <= r2 else (sw, int(sw / w * h))


# --------------------------
# Operator
# --------------------------
class JF_OT_quick_set(bpy.types.Operator):
    bl_idname = "jf.image_quick_set"
    bl_label = "Quick Set by Animation Type"

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
                props = context.scene.jf_image_props
                props.filepath = filepath
                props.update_image_size()
                props.k1_w, props.k1_h = props.img_w, props.img_h
                props.k2_w, props.k2_h = props.img_w, props.img_h
                props.k3_w, props.k3_h = props.img_w, props.img_h
                props.k4_w, props.k4_h = props.img_w, props.img_h
                fps = get_fps()
                duration = strip.frame_final_duration / fps
                if duration >= IN_TIME * 2:
                    props.k12_t = IN_TIME
                    props.k23_t = duration - IN_TIME * 2
                    props.k34_t = IN_TIME
                else:
                    self.report(
                        {"WARNING"},
                        f"strip duration too short, less than {IN_TIME * 2}s",
                    )
            else:
                self.report({"WARNING"}, "Invalid image strip")
                return {"CANCELLED"}

        props = context.scene.jf_image_props
        if not props.check_filepath():
            return {"CANCELLED"}

        type = props.anim_type
        size_type = props.size_type
        sw, sh = get_screen_size(context)

        if size_type == "ORIGIN":
            w, h = props.img_w, props.img_h
        elif size_type == "COVER":
            w, h = props.calc_cover_size(context)
        elif size_type == "CONTAIN":
            w, h = props.calc_contain_size(context)
        elif size_type == "1/2w":
            w = sw * 1 / 2
            h = w / props.img_w * props.img_h
        elif size_type == "1/4w":
            w = sw * 1 / 4
            h = w / props.img_w * props.img_h
        elif size_type == "1/6w":
            w = sw * 1 / 6
            h = w / props.img_w * props.img_h
        elif size_type == "1/8w":
            w = sw * 1 / 8
            h = w / props.img_w * props.img_h
        elif size_type == "1/2h":
            h = sh * 1 / 2
            w = h / props.img_h * props.img_w
        elif size_type == "1/4h":
            h = sh * 1 / 4
            w = h / props.img_h * props.img_w
        elif size_type == "1/6h":
            h = sh * 1 / 6
            w = h / props.img_h * props.img_w
        elif size_type == "1/8h":
            h = sh * 1 / 8
            w = h / props.img_h * props.img_w
        else:
            self.report({"ERROR"}, "Unknown size type")
            return {"CANCELLED"}
        w, h = int(w), int(h)

        origin_type = props.origin_type
        if origin_type == "UL":
            ox, oy = (w - sw) / 2, (sh - h) / 2
        elif origin_type == "U":
            ox, oy = 0, (sh - h) / 2
        elif origin_type == "UR":
            ox, oy = (sw - w) / 2, (sh - h) / 2
        elif origin_type == "L":
            ox, oy = (w - sw) / 2, 0
        elif origin_type == "C":
            ox, oy = 0, 0
        elif origin_type == "R":
            ox, oy = sw / 4, 0
        elif origin_type == "DL":
            ox, oy = (w - sw) / 2, (h - sh) / 2
        elif origin_type == "D":
            ox, oy = 0, (h - sh) / 2
        elif origin_type == "DR":
            ox, oy = (sw - w) / 2, (h - sh) / 2
        else:
            self.report({"ERROR"}, "Unknown origin type")
            return {"CANCELLED"}
        ox, oy = int(ox), int(oy)

        props.k1_w, props.k1_h = w, h
        props.k1_x, props.k1_y = ox, oy
        props.k1_a = 0
        props.k1_enable_rotation = False

        props.k2_w, props.k2_h = w, h
        props.k2_x, props.k2_y = ox, oy
        props.k2_a = 1
        props.k2_enable_rotation = False

        props.k3_w, props.k3_h = w, h
        props.k3_x, props.k3_y = ox, oy
        props.k3_a = 1
        props.k3_enable_rotation = False

        props.k4_w, props.k4_h = w, h
        props.k4_x, props.k4_y = ox, oy
        props.k4_a = 0
        props.k4_enable_rotation = False

        mov_scale = 1.2
        if type.startswith("MOV"):
            props.k4_w = int(w * mov_scale)
            props.k4_h = int(h * mov_scale)
            props.k2_enable_pos = False
            props.k2_enable_size = False
            props.k3_enable_pos = False
            props.k3_enable_size = False
        else:
            props.k2_enable_pos = True
            props.k2_enable_size = True
            props.k3_enable_pos = True
            props.k3_enable_size = True

        slide_x = int(sw * 0.05)
        slide_y = int(sh * 0.05)
        zoom_ratio = 0.4

        if type == "MOV_LEFT":
            props.k4_x = ox - slide_x
            props.k4_y = oy
        elif type == "MOV_RIGHT":
            props.k4_x = ox + slide_x
            props.k4_y = oy
        elif type == "MOV_UP":
            props.k4_x = ox
            props.k4_y = oy + slide_y
        elif type == "MOV_DOWN":
            props.k4_x = ox
            props.k4_y = oy - slide_y
        elif type == "FADE":
            pass
        elif type == "UD":
            props.k1_x = ox
            props.k1_y = oy + slide_y
            props.k4_x = ox
            props.k4_y = oy - slide_y
        elif type == "DU":
            props.k1_x = ox
            props.k1_y = oy - slide_y
            props.k4_x = ox
            props.k4_y = oy + slide_y
        elif type == "LR":
            props.k1_x = ox - slide_x
            props.k1_y = oy
            props.k4_x = ox + slide_x
            props.k4_y = oy
        elif type == "RL":
            props.k1_x = ox + slide_x
            props.k1_y = oy
            props.k4_x = ox - slide_x
            props.k4_y = oy
        elif type == "ZOOM+":
            props.k1_w = int(w * zoom_ratio)
            props.k1_h = int(h * zoom_ratio)
            props.k4_w = int(w * (1 + zoom_ratio))
            props.k4_h = int(h * (1 + zoom_ratio))
        elif type == "ZOOM-":
            props.k1_w = int(w * (1 + zoom_ratio))
            props.k1_h = int(h * (1 + zoom_ratio))
            props.k4_w = int(w * zoom_ratio)
            props.k4_h = int(h * zoom_ratio)
        else:
            self.report({"ERROR"}, "Unknown animation type")
        return {"FINISHED"}


class JF_OT_k1_size_origin(bpy.types.Operator):
    bl_idname = "jf.image_k1_size_origin"
    bl_label = "Reset In Size"

    def execute(self, context):
        props = context.scene.jf_image_props
        props.k1_w, props.k1_h = props.img_w, props.img_h
        return {"FINISHED"}


class JF_OT_k1_size_cover(bpy.types.Operator):
    bl_idname = "jf.image_k1_size_cover"
    bl_label = "In Size Cover Screen"

    def execute(self, context):
        props = context.scene.jf_image_props
        props.k1_w, props.k1_h = props.calc_cover_size(context)
        return {"FINISHED"}


class JF_OT_k1_size_contain(bpy.types.Operator):
    bl_idname = "jf.image_k1_size_contain"
    bl_label = "In Size Contain Screen"

    def execute(self, context):
        props = context.scene.jf_image_props
        props.k1_w, props.k1_h = props.calc_contain_size(context)
        return {"FINISHED"}


class JF_OT_k1_size_gap(bpy.types.Operator):
    bl_idname = "jf.image_k1_size_gap"
    bl_label = "Reset In Size By Gap"

    def execute(self, context):
        props = context.scene.jf_image_props
        props.k1_w, props.k1_h = props.calc_gap_size(context)
        return {"FINISHED"}


class JF_OT_k2_size_cover(bpy.types.Operator):
    bl_idname = "jf.image_k2_size_cover"
    bl_label = "Keep Size Cover Screen"

    def execute(self, context):
        props = context.scene.jf_image_props
        props.k2_w, props.k2_h = props.calc_cover_size(context)
        return {"FINISHED"}


class JF_OT_k2_size_contain(bpy.types.Operator):
    bl_idname = "jf.image_k2_size_contain"
    bl_label = "Keep Size Contain Screen"

    def execute(self, context):
        props = context.scene.jf_image_props
        props.k2_w, props.k2_h = props.calc_contain_size(context)
        return {"FINISHED"}


class JF_OT_k2_size_origin(bpy.types.Operator):
    bl_idname = "jf.image_k2_size_origin"
    bl_label = "Reset Keep Size"

    def execute(self, context):
        props = context.scene.jf_image_props
        props.k2_w, props.k2_h = props.img_w, props.img_h
        return {"FINISHED"}


class JF_OT_k2_size_gap(bpy.types.Operator):
    bl_idname = "jf.image_k2_size_gap"
    bl_label = "Reset Keep Size By Gap"

    def execute(self, context):
        props = context.scene.jf_image_props
        props.k2_w, props.k2_h = props.calc_gap_size(context)
        return {"FINISHED"}


class JF_OT_k3_size_cover(bpy.types.Operator):
    bl_idname = "jf.image_k3_size_cover"
    bl_label = "Keep Size Cover Screen"

    def execute(self, context):
        props = context.scene.jf_image_props
        props.k3_w, props.k3_h = props.calc_cover_size(context)
        return {"FINISHED"}


class JF_OT_k3_size_contain(bpy.types.Operator):
    bl_idname = "jf.image_k3_size_contain"
    bl_label = "Keep Size Contain Screen"

    def execute(self, context):
        props = context.scene.jf_image_props
        props.k3_w, props.k3_h = props.calc_contain_size(context)
        return {"FINISHED"}


class JF_OT_k3_size_origin(bpy.types.Operator):
    bl_idname = "jf.image_k3_size_origin"
    bl_label = "Reset Keep Size"

    def execute(self, context):
        props = context.scene.jf_image_props
        props.k3_w, props.k3_h = props.img_w, props.img_h
        return {"FINISHED"}


class JF_OT_k3_size_gap(bpy.types.Operator):
    bl_idname = "jf.image_k3_size_gap"
    bl_label = "Reset Keep Size By Gap"

    def execute(self, context):
        props = context.scene.jf_image_props
        props.k3_w, props.k3_h = props.calc_gap_size(context)
        return {"FINISHED"}


class JF_OT_k4_size_origin(bpy.types.Operator):
    bl_idname = "jf.image_k4_size_origin"
    bl_label = "Reset Out Size"

    def execute(self, context):
        props = context.scene.jf_image_props
        props.k4_w, props.k4_h = props.img_w, props.img_h
        return {"FINISHED"}


class JF_OT_k4_size_cover(bpy.types.Operator):
    bl_idname = "jf.image_k4_size_cover"
    bl_label = "Out Size Cover Screen"

    def execute(self, context):
        props = context.scene.jf_image_props
        props.k4_w, props.k4_h = props.calc_cover_size(context)
        return {"FINISHED"}


class JF_OT_k4_size_contain(bpy.types.Operator):
    bl_idname = "jf.image_k4_size_contain"
    bl_label = "Out Size Contain Screen"

    def execute(self, context):
        props = context.scene.jf_image_props
        props.k4_w, props.k4_h = props.calc_contain_size()
        return {"FINISHED"}


class JF_OT_k4_size_gap(bpy.types.Operator):
    bl_idname = "jf.image_k4_size_gap"
    bl_label = "Reset Out Size By Gap"

    def execute(self, context):
        props = context.scene.jf_image_props
        props.k4_w, props.k4_h = props.calc_gap_size(context)
        return {"FINISHED"}


class JF_OT_add_animation(bpy.types.Operator):
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

    def execute(self, context):
        props = context.scene.jf_image_props
        filepath = bpy.path.abspath(props.filepath)

        seq = context.scene.sequence_editor
        if not seq:
            seq = context.scene.sequence_editor_create()

        fps = get_fps()
        in_frames = int(props.k12_t * fps)
        keep_frames = int(props.k23_t * fps)
        out_frames = int(props.k34_t * fps)

        selected_strips = bpy.context.selected_sequences
        if not selected_strips:
            self.report({"WARNING"}, "No strip selected")
            return {"CANCELLED"}
        elif len(selected_strips) > 1:
            self.report({"WARNING"}, "Only one image strip is allowed")
            return {"CANCELLED"}
        else:
            strip = selected_strips[0]
            start_frame = strip.frame_final_start
            channel = strip.channel
            seq_editor = bpy.context.scene.sequence_editor
            seq_editor.sequences.remove(strip)

        img_strip = seq.sequences.new_image(
            name=filepath.split("/")[-1],
            filepath=filepath,
            channel=channel,
            frame_start=start_frame,
        )
        img_strip.frame_final_duration = in_frames + keep_frames + out_frames

        insert_keyframe(
            img_strip,
            frame=start_frame,
            alpha=props.k1_a,
            offset_x=props.k1_x,
            offset_y=props.k1_y,
            scale_x=props.k1_w / props.img_w,
            scale_y=props.k1_h / props.img_h,
            rotation=props.k1_rotation if props.k1_enable_rotation else None,
        )

        start_frame += in_frames
        insert_keyframe(
            img_strip,
            frame=start_frame,
            alpha=props.k2_a if props.k2_enable_alpha else None,
            offset_x=props.k2_x if props.k2_enable_pos else None,
            offset_y=props.k2_y if props.k2_enable_pos else None,
            scale_x=props.k2_w / props.img_w if props.k2_enable_size else None,
            scale_y=props.k2_h / props.img_h if props.k2_enable_size else None,
            rotation=props.k2_rotation if props.k2_enable_rotation else None,
        )

        start_frame += keep_frames
        insert_keyframe(
            img_strip,
            frame=start_frame,
            alpha=props.k3_a if props.k3_enable_alpha else None,
            offset_x=props.k3_x if props.k3_enable_pos else None,
            offset_y=props.k3_y if props.k3_enable_pos else None,
            scale_x=props.k3_w / props.img_w if props.k3_enable_size else None,
            scale_y=props.k3_h / props.img_h if props.k3_enable_size else None,
            rotation=props.k3_rotation if props.k3_enable_rotation else None,
        )

        start_frame += out_frames
        insert_keyframe(
            img_strip,
            frame=start_frame,
            alpha=props.k4_a,
            offset_x=props.k4_x,
            offset_y=props.k4_y,
            scale_x=props.k4_w / props.img_w,
            scale_y=props.k4_h / props.img_h,
            rotation=props.k4_rotation if props.k4_enable_rotation else None,
        )

        self.report({"INFO"}, f"Inserted {filepath.split('/')[-1]}")
        return {"FINISHED"}


# --------------------------
# UI Panel
# --------------------------
class JF_PT_image_panel(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Jellyfish"
    bl_label = "Image"

    def draw(self, context):
        layout = self.layout
        props = context.scene.jf_image_props

        ow, oh = props.img_w, props.img_h

        col = layout.column(align=True)
        col.prop(props, "origin_type", text="")
        col.prop(props, "size_type", text="")
        col.prop(props, "anim_type", text="")
        row = col.row(align=True)
        row.operator("jf.image_quick_set", text="Generate", icon="MODIFIER")
        row.operator("jf.image_add_image_anim", text="Insert", icon="OUTLINER_OB_IMAGE")

        k1_box = layout.box()
        k1_box.label(text="k1")
        size_col = k1_box.column(align=True)
        row = size_col.row(align=True)
        row.prop(props, "k1_w", text="W")
        row.prop(props, "k1_h", text="H")
        size_row1 = size_col.row(align=True)
        size_row1.operator("jf.image_k1_size_origin", text="Origin", icon="LOOP_BACK")
        size_row1.operator("jf.image_k1_size_gap", text="Gap", icon="FULLSCREEN_EXIT")
        size_row2 = size_col.row(align=True)
        size_row2.operator("jf.image_k1_size_cover", text="Cover", icon="CLIPUV_DEHLT")
        size_row2.operator(
            "jf.image_k1_size_contain", text="Contain", icon="CLIPUV_HLT"
        )
        w, h = props.k1_w, props.k1_h
        if w > ow or h > oh:
            k1_box.label(text="Out of origin size", icon="ERROR")
        pos_row = k1_box.row(align=True)
        pos_row.prop(props, "k1_x", text="X")
        pos_row.prop(props, "k1_y", text="Y")
        k1_box.prop(props, "k1_a")
        row = k1_box.row(align=True)
        row.prop(
            props,
            "k1_enable_rotation",
            text="" if props.k1_enable_rotation else "Enable Rotation",
        )
        if props.k1_enable_rotation:
            row.prop(props, "k1_r")

        layout.prop(props, "k12_t")

        k2_box = layout.box()
        k2_box.label(text="k2")
        size_row = k2_box.row(align=True)
        size_row.prop(
            props, "k2_enable_size", text="" if props.k2_enable_size else "Enable Size"
        )
        if props.k2_enable_size:
            size_col = size_row.column(align=True)
            row = size_col.row(align=True)
            row.prop(props, "k2_w", text="W")
            row.prop(props, "k2_h", text="H")
            size_row1 = size_col.row(align=True)
            size_row1.operator(
                "jf.image_k2_size_origin", text="Origin", icon="LOOP_BACK"
            )
            size_row1.operator(
                "jf.image_k2_size_gap", text="Gap", icon="FULLSCREEN_EXIT"
            )
            size_row2 = size_col.row(align=True)
            size_row2.operator(
                "jf.image_k2_size_cover", text="Cover", icon="CLIPUV_DEHLT"
            )
            size_row2.operator(
                "jf.image_k2_size_contain", text="Contain", icon="CLIPUV_HLT"
            )
            w, h = props.k2_w, props.k2_h
            if w > ow or h > oh:
                k2_box.label(text="Out of origin size", icon="ERROR")
        pos_row = k2_box.row(align=True)
        pos_row.prop(
            props,
            "k2_enable_pos",
            text="" if props.k2_enable_pos else "Enable Position",
        )
        if props.k2_enable_pos:
            pos_row.prop(props, "k2_x", text="X")
            pos_row.prop(props, "k2_y", text="Y")
        row = k2_box.row(align=True)
        row.prop(
            props,
            "k2_enable_alpha",
            text="" if props.k2_enable_alpha else "Enable Alpha",
        )
        if props.k2_enable_alpha:
            row.prop(props, "k2_a")
        row = k2_box.row(align=True)
        row.prop(
            props,
            "k2_enable_rotation",
            text="" if props.k2_enable_rotation else "Enable Rotation",
        )
        if props.k2_enable_rotation:
            row.prop(props, "k2_r")

        layout.prop(props, "k23_t")

        k3_box = layout.box()
        k3_box.label(text="k3")
        size_row = k3_box.row(align=True)
        size_row.prop(
            props, "k3_enable_size", text="" if props.k3_enable_size else "Enable Size"
        )
        if props.k3_enable_size:
            size_col = size_row.column(align=True)
            row = size_col.row(align=True)
            row.prop(props, "k3_w", text="W")
            row.prop(props, "k3_h", text="H")
            size_row1 = size_col.row(align=True)
            size_row1.operator(
                "jf.image_k3_size_origin", text="Origin", icon="LOOP_BACK"
            )
            size_row1.operator(
                "jf.image_k3_size_gap", text="Gap", icon="FULLSCREEN_EXIT"
            )
            size_row2 = size_col.row(align=True)
            size_row2.operator(
                "jf.image_k3_size_cover", text="Cover", icon="CLIPUV_DEHLT"
            )
            size_row2.operator(
                "jf.image_k3_size_contain", text="Contain", icon="CLIPUV_HLT"
            )
            w, h = props.k3_w, props.k3_h
            if w > ow or h > oh:
                k3_box.label(text="Out of origin size", icon="ERROR")
        pos_row = k3_box.row(align=True)
        pos_row.prop(
            props,
            "k3_enable_pos",
            text="" if props.k3_enable_pos else "Enable Position",
        )
        if props.k3_enable_pos:
            pos_row.prop(props, "k3_x", text="X")
            pos_row.prop(props, "k3_y", text="Y")
        row = k3_box.row(align=True)
        row.prop(
            props,
            "k3_enable_alpha",
            text="" if props.k3_enable_alpha else "Enable Alpha",
        )
        if props.k3_enable_alpha:
            row.prop(props, "k3_a")
        row = k3_box.row(align=True)
        row.prop(
            props,
            "k3_enable_rotation",
            text="" if props.k3_enable_rotation else "Enable Rotation",
        )
        if props.k3_enable_rotation:
            row.prop(props, "k3_r")

        layout.prop(props, "k34_t")

        k4_box = layout.box()
        k4_box.label(text="k4")
        size_col = k4_box.column(align=True)
        row = size_col.row(align=True)
        row.prop(props, "k4_w", text="W")
        row.prop(props, "k4_h", text="H")
        size_row1 = size_col.row(align=True)
        size_row1.operator("jf.image_k4_size_origin", text="Origin", icon="LOOP_BACK")
        size_row1.operator("jf.image_k4_size_gap", text="Gap", icon="FULLSCREEN_EXIT")
        size_row2 = size_col.row(align=True)
        size_row2.operator("jf.image_k4_size_cover", text="Cover", icon="CLIPUV_DEHLT")
        size_row2.operator(
            "jf.image_k4_size_contain", text="Contain", icon="CLIPUV_HLT"
        )
        w, h = props.k4_w, props.k4_h
        if w > ow or h > oh:
            k4_box.label(text="Out of origin size", icon="ERROR")
        pos_row = k4_box.row(align=True)
        pos_row.prop(props, "k4_x", text="X")
        pos_row.prop(props, "k4_y", text="Y")
        k4_box.prop(props, "k4_a")
        row = k4_box.row(align=True)
        row.prop(
            props,
            "k4_enable_rotation",
            text="" if props.k4_enable_rotation else "Enable Rotation",
        )
        if props.k4_enable_rotation:
            row.prop(props, "k4_r")


# --------------------------
# Register
# --------------------------
classes = [
    JFImageProps,
    JF_OT_quick_set,
    JF_OT_add_animation,
    JF_OT_k1_size_origin,
    JF_OT_k1_size_cover,
    JF_OT_k1_size_contain,
    JF_OT_k1_size_gap,
    JF_OT_k2_size_origin,
    JF_OT_k2_size_cover,
    JF_OT_k2_size_contain,
    JF_OT_k2_size_gap,
    JF_OT_k3_size_origin,
    JF_OT_k3_size_cover,
    JF_OT_k3_size_contain,
    JF_OT_k3_size_gap,
    JF_OT_k4_size_origin,
    JF_OT_k4_size_cover,
    JF_OT_k4_size_contain,
    JF_OT_k4_size_gap,
    JF_PT_image_panel,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.jf_image_props = bpy.props.PointerProperty(type=JFImageProps)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.jf_image_props


if __name__ == "__main__":
    register()
