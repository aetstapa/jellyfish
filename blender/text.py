# pyright: reportMissingModuleSource=false
# pyright: reportInvalidTypeForm=false

bl_info = {
    "name": "Text",
    "author": "Jiaju",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "VSE > Sidebar",
    "description": "Insert text strips in VSE with enter/exit animations",
    "category": "Sequencer",
}

import bpy, os, sys
from bpy.props import (
    StringProperty,
    EnumProperty,
    FloatProperty,
    FloatVectorProperty,
    IntProperty,
)
from utils import *

ANIM_TIME = 0.5
GAP = 0.05


def get_default_font_dir():
    if sys.platform.startswith("win"):
        return os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")
    elif sys.platform.startswith("darwin"):
        return "/System/Library/Fonts"
    elif sys.platform.startswith("linux"):
        user_fonts = os.path.expanduser("~/.fonts")
        system_fonts = "/usr/share/fonts"
        return user_fonts if os.path.exists(user_fonts) else system_fonts
    else:
        return os.path.expanduser("~")


class VSETextProperties(bpy.types.PropertyGroup):
    source: EnumProperty(
        name="Source",
        description="Image source",
        items=[
            ("NEW", "New", ""),
            ("STRIP", "Strip", ""),
        ],
        default="NEW",
    )
    text: StringProperty(
        name="Text", description="Text to insert", default="Hello World"
    )
    font_path: StringProperty(name="Font", description="Path to TTF font", default="")
    size: FloatProperty(name="Size", description="Font size", default=52.0)
    color: FloatVectorProperty(
        name="Color",
        description="Text color",
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(1.0, 1.0, 1.0, 1.0),
    )
    placement: EnumProperty(
        name="Placement",
        description="Place text method",
        items=[
            ("POS", "Point", ""),
            ("SCREEN", "Screen", ""),
        ],
        default="POS",
    )
    x: FloatProperty(name="X", description="X position", default=0.5)
    y: FloatProperty(name="Y", description="Y position", default=0.5)
    rel_pos: EnumProperty(
        name="Relative Position",
        description="Relative to screen",
        items=[
            ("TL", "Top Left", ""),
            ("TC", "Top", ""),
            ("TR", "Top Right", ""),
            ("LC", "Left", ""),
            ("C", "Center", ""),
            ("RC", "Right", ""),
            ("BL", "Bottom Left", ""),
            ("BC", "Bottom", ""),
            ("BR", "Bottom Right", ""),
        ],
        default="C",
    )
    channel: IntProperty(
        name="Channel", description="Channel to insert", default=1, min=1
    )
    duration: FloatProperty(
        name="Duration",
        description="Text strip duration",
        min=2 * ANIM_TIME,
        default=2 * ANIM_TIME + 2,
    )


class VSE_OT_ReadText(bpy.types.Operator):
    bl_idname = "jf.text_read_text"
    bl_label = "Read Text Strip"
    bl_description = "Read text strip info, such as text, size, location..."

    def execute(self, context):
        props = context.scene.jf_text_props
        selected_strips = bpy.context.selected_sequences
        if not selected_strips:
            self.report({"WARNING"}, "No strip selected")
        elif len(selected_strips) > 1:
            self.report({"WARNING"}, "Only one image strip is allowed")
        else:
            strip = selected_strips[0]
            if strip.type == "TEXT":
                font = strip.font
                if font:
                    props.font_path = font.filepath
                props.text = strip.text
                props.size = strip.font_size
                props.x, props.y = strip.location
                props.color = strip.color
                props.channel = strip.channel
                fps = get_fps()
                props.duration = strip.frame_final_duration / fps
            else:
                self.report({"WARNING"}, "Invalid image strip")
        return {"FINISHED"}


class VSE_OT_SelectFontPath(bpy.types.Operator):
    bl_idname = "jf.text_select_font_path"
    bl_label = "Select Font"
    bl_description = "Select a TTF font file"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def invoke(self, context, event):
        default_dir = get_default_font_dir()
        self.filepath = default_dir
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        context.scene.jf_text_props.font_path = self.filepath
        self.report({"INFO"}, f"Font selected: {self.filepath}")
        return {"FINISHED"}


class VSE_OT_SmallFontSize(bpy.types.Operator):
    bl_idname = "jf.text_small_font_size"
    bl_label = "Small Font Size"
    bl_description = "Set small font size"

    def execute(self, context):
        props = context.scene.jf_text_props
        props.size = 100
        return {"FINISHED"}


class VSE_OT_MediumFontSize(bpy.types.Operator):
    bl_idname = "jf.text_medium_font_size"
    bl_label = "Medium Font Size"
    bl_description = "Set medium font size"

    def execute(self, context):
        props = context.scene.jf_text_props
        props.size = 150
        return {"FINISHED"}


class VSE_OT_LargeFontSize(bpy.types.Operator):
    bl_idname = "jf.text_large_font_size"
    bl_label = "Large Font Size"
    bl_description = "Set large font size"

    def execute(self, context):
        props = context.scene.jf_text_props
        props.size = 200
        return {"FINISHED"}


class VSE_OT_InsertText(bpy.types.Operator):
    bl_idname = "jf.text_insert_text"
    bl_label = "Insert Text Strip"
    bl_description = "Insert text strip at current frame"

    def execute(self, context):
        scene = context.scene
        props = scene.jf_text_props
        seq = scene.sequence_editor

        if props.font_path == "":
            self.report({"WARNING"}, "Invalid font path")
            return {"FINISHED"}

        if seq is None:
            scene.sequence_editor_create()

        fps = get_fps()
        if props.source == "NEW":
            frame_start = scene.frame_current
        else:
            selected_strips = bpy.context.selected_sequences
            if not selected_strips:
                self.report({"WARNING"}, "No strip selected")
                return {"FINISHED"}
            elif len(selected_strips) > 1:
                self.report({"WARNING"}, "Only one text strip is allowed")
                return {"FINISHED"}
            else:
                strip = selected_strips[0]
                if strip.type == "TEXT":
                    frame_start = strip.frame_final_start
                    seq_editor = bpy.context.scene.sequence_editor
                    seq_editor.sequences.remove(strip)
                else:
                    self.report({"WARNING"}, "Invalid image strip")
                    return {"FINISHED"}
        frame_end = frame_start + int(props.duration * fps)
        print(frame_start, frame_end)

        text_strip = seq.sequences.new_effect(
            name=props.text,
            type="TEXT",
            channel=props.channel,
            frame_start=frame_start,
            frame_end=frame_end,
        )

        text_strip.text = props.text
        font_path = props.font_path
        font_name = os.path.basename(font_path)
        if font_name in bpy.data.fonts:
            text_strip.font = bpy.data.fonts[font_name]
        else:
            text_strip.font = bpy.data.fonts.load(font_path)

        text_strip.font_size = props.size
        text_strip.color = props.color

        x, y = props.x, props.y
        rel_pos = props.rel_pos
        is_screen = props.placement == "SCREEN"
        if rel_pos == "TL":
            location = (GAP, 1 - GAP) if is_screen else (x, y)
            anchor = ("LEFT", "TOP") if is_screen else ("RIGHT", "BOTTOM")
        elif rel_pos == "TC":
            location = (0.5, 1 - GAP) if is_screen else (x, y)
            anchor = ("CENTER", "TOP") if is_screen else ("CENTER", "BOTTOM")
        elif rel_pos == "TR":
            location = (1 - GAP, 1 - GAP) if is_screen else (x, y)
            anchor = ("RIGHT", "TOP") if is_screen else ("LEFT", "BOTTOM")
        elif rel_pos == "LC":
            location = (GAP, 0.5) if is_screen else (x, y)
            anchor = ("LEFT", "CENTER") if is_screen else ("RIGHT", "CENTER")
        elif rel_pos == "C":
            location = (0.5, 0.5) if is_screen else (x, y)
            anchor = ("CENTER", "CENTER")
        elif rel_pos == "RC":
            location = (1 - GAP, 0.5) if is_screen else (x, y)
            anchor = ("RIGHT", "CENTER") if is_screen else ("LEFT", "CENTER")
        elif rel_pos == "BL":
            location = (GAP, GAP) if is_screen else (x, y)
            anchor = ("LEFT", "BOTTOM") if is_screen else ("RIGHT", "TOP")
        elif rel_pos == "BC":
            location = (0.5, GAP) if is_screen else (x, y)
            anchor = ("CENTER", "BOTTOM") if is_screen else ("CENTER", "TOP")
        elif rel_pos == "BR":
            location = (1 - GAP, GAP) if is_screen else (x, y)
            anchor = ("RIGHT", "BOTTOM") if is_screen else ("LEFT", "TOP")
        else:
            raise ValueError(f"Invalid relative position: {rel_pos}")

        text_strip.location = location
        text_strip.align_x, text_strip.align_y = anchor

        sw, sh = get_screen_size(context)
        px_x, px_y = x * sw, y * sh
        offset = 30
        insert_keyframe(
            text_strip,
            frame=(frame_start, frame_start + int(ANIM_TIME * fps)),
            alpha=(0, 1),
            pos=((0, offset), (0, 0)),
        )
        frame_start = text_strip.frame_final_end - int(ANIM_TIME * fps)
        insert_keyframe(
            text_strip,
            frame=(frame_start, text_strip.frame_final_end),
            alpha=(1, 0),
            pos=((0, 0), (0, -offset)),
        )

        self.report({"INFO"}, f"Inserted text strip: {props.text}")
        return {"FINISHED"}


class VSE_PT_TextPanel(bpy.types.Panel):
    bl_label = "Text"
    bl_idname = "VSE_PT_text_panel"
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Jellyfish"

    def draw(self, context):
        layout = self.layout
        props = context.scene.jf_text_props

        row = layout.row(align=True)
        row.prop(props, "source", text="")
        if props.source == "STRIP":
            row.operator("jf.text_read_text", icon="INFO")
        layout.prop(props, "text", text="")
        row = layout.row(align=True)
        row.prop(props, "font_path", text="")
        row.operator("jf.text_select_font_path", icon="FILE_FONT", text="")
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(props, "size")
        row.prop(props, "color", text="")
        row = col.row(align=True)
        row.operator("jf.text_small_font_size", text="S")
        row.operator("jf.text_medium_font_size", text="M")
        row.operator("jf.text_large_font_size", text="L")
        col = layout.column(align=True)
        col.prop(props, "placement", text="")
        row = col.row(align=True)
        row.prop(props, "rel_pos", text="")
        row.prop(props, "x")
        row.prop(props, "y")
        layout.prop(props, "duration")
        layout.prop(props, "channel")
        text = "Insert" if props.source == "NEW" else "Modify"
        layout.operator("jf.text_insert_text", text=text)


classes = (
    VSETextProperties,
    VSE_OT_ReadText,
    VSE_OT_SelectFontPath,
    VSE_OT_SmallFontSize,
    VSE_OT_MediumFontSize,
    VSE_OT_LargeFontSize,
    VSE_OT_InsertText,
    VSE_PT_TextPanel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.jf_text_props = bpy.props.PointerProperty(type=VSETextProperties)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.jf_text_props


if __name__ == "__main__":
    register()
