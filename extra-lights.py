bl_info = {
    "name": "Extra Lights",
    "author": "Jonathan Lampel",
    "version": (1, 0),
    "blender": (2, 82, 0),
    "location": "View3D > Add > Light",
    "description": "Adds new preset light objects based on real world values",
    "warning": "",
    "doc_url": "",
    "category": "Add Light",
}

import bpy
import os
from bpy.types import Operator
from bpy_extras.object_utils import AddObjectHelper, object_data_add

# set light properties 

class Light:
    def __init__(self, name, lightType, radius, temp, lumens):
        self.name = name
        self.lightType = lightType
        self.radius = radius
        self.temp = temp
        self.lumens = lumens

natural_01 = Light("Candle", "POINT", 0.015, 1800, 12.57)
natural_02 = Light("Fireplace", "POINT", 0.228, 2000, 500)
naturals = [natural_01, natural_02]

incandescent_01 = Light("10w C7 Candelabra", "POINT", 0.015, 2700, 70)
incandescent_02 = Light("25w A15", "POINT", 0.0216, 2700, 210)
incandescents = [incandescent_01, incandescent_02]

# Append Lumens Converter if it's not already in the file

if (bpy.data.node_groups.find("Lumens Converter") == -1):

    blendfile = "C:/Users/jonat/Dropbox (CG Cookie Studio)/Education/learning-flows/intro-to-blender_2.8/fundamentals-of-lighting_2-8/scene/extra-lights/lights/real_lights.blend"
    section = "\\NodeTree\\"
    object = "Lumens Converter"

    bpy.ops.wm.append(
        filename = object,
        directory = blendfile + section
        )

# Add new light

def create_light(self, context, light):
    light_data = bpy.data.lights.new(name=light.name+"Data", type=light.lightType)
    light_data.shadow_soft_size = light.radius
    
    light_object = bpy.data.objects.new(name=light.name, object_data=light_data)
    
    bpy.context.collection.objects.link(light_object)
    bpy.ops.object.select_all(action='DESELECT')
    light_object.select_set(state = True)
    context.view_layer.objects.active = light_object

# Create operator

class OBJECT_OT_add_light(Operator, AddObjectHelper):
    bl_idname = "light.add_light"
    bl_label = "Add Light Object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for light in naturals: 
            create_light(self, context, light)
            return {'FINISHED'}
        
# Registration 

def add_light_buttons(self, context):
    # I need to do this for each light in list
    self.layout.operator(
        OBJECT_OT_add_light.bl_idname,
        text="Candle",
        icon='LIGHT_POINT')
        
def register():
    bpy.utils.register_class(OBJECT_OT_add_light)
    bpy.types.VIEW3D_MT_light_add.append(add_light_buttons)
    
def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_light)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_light_buttons)

if __name__ == "__main__":
    register()