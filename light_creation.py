import bpy, os
from bpy.types import Operator
from bpy.utils import register_class, unregister_class

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'presets')

def create_light_operator(preset):
    name = preset
    bl_id = ''.join(i for i in name if i.isalnum()).lower()

    class OBJECT_OT_add_light(Operator):
        bl_idname = "light.add_" + bl_id
        bl_label = name
        bl_description = "Creates an Extra Lights preset object"
        bl_options = {'REGISTER', 'UNDO'}

        def execute(self, context):
            bpy.ops.wm.append(directory = path + '', filename = name)

    return OBJECT_OT_add_light

def create_category_menu(category, operators):
    class EXTRALIGHTS_MT_menu(bpy.types.Menu):
        bl_idname = 'OBJECT_MT_' + category + '_menu'
        bl_label = category

        def draw(self, context):
            for op in operators:
                self.layout.operator(
                    op.bl_idname,
                    text = op.bl_label,
                    icon = 'LIGHT',
                )

        def draw_category(self, context):
            self.layout.menu(EXTRALIGHTS_MT_menu.bl_idname, icon='LIGHT')

    return EXTRALIGHTS_MT_menu