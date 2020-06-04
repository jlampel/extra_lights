import bpy, os
from bpy.types import Operator
from bpy.utils import register_class, unregister_class

path = os.path.dirname(os.path.abspath(__file__)) + '/presets/'

class Light:
    def __init__(self, preset):
        self.preset = preset

    def create_light(self):
        class OBJECT_OT_add_light(Operator):
            name = list( self.preset.keys() )[0]

            bl_idname = "light.add_" + name.replace(' ', '').lower()
            bl_label = "Add a " + name
            bl_description = "Creates an Extra Lights preset object"
            bl_options = {'REGISTER', 'UNDO'}

            def execute(self, context):

                bpy.ops.wm.append(directory = path + '', filename = self.name)

        return OBJECT_OT_add_light


