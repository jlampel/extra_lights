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
from bpy.utils import register_class, unregister_class
from bpy_extras.object_utils import AddObjectHelper, object_data_add

# set light properties 

class Light:
    def __init__(self, name, lightType, radius, temp, lumens):
        self.name = name
        self.lightType = lightType
        self.radius = radius
        self.temp = temp
        self.lumens = lumens

nat_01 = Light("Candle", "POINT", 0.015, 1800, 12.57)
nat_02 = Light("Fireplace", "POINT", 0.228, 2000, 500)

inc_01 = Light("10w C7 Candelabra", "POINT", 0.015, 2700, 70)
inc_02 = Light("25w A15", "POINT", 0.0216, 2700, 210)

led_01 = Light("400 Lumen Flashlight", "SPOT", 0.0075, 2700, 400)
led_02 = Light("1400 Lumen Flashlight", "SPOT", 0.0075, 4000, 1400)
led_03 = Light("60w A19 White", "POINT", 0.034, 3000, 800)
led_04 = Light("100w A21 Daylight", "POINT", 0.034, 5000, 1600)
led_05 = Light("150w PAR38 White", "POINT", 0.06, 3000, 1400)
led_06 = Light("250w PAR38 White", "POINT", 0.06, 3000, 2600)

fl_01 = Light("45w Daylight CFL", "POINT", 0.03, 5500, 2250)
fl_02 = Light("60w Halogen Headlight", "SPOT", 0.02, 4100, 3000)

# Append Lumens Converter if it's not already in the file

if (bpy.data.node_groups.find("Lumens Converter") == -1):

    blendfile = "C:/Users/jonat/Documents/GitHub/extra-lights/lights/real_lights.blend"
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

# Create operators

# Natural lights
class OBJECT_OT_add_nat01(Operator, AddObjectHelper):
    bl_idname = "light.add_nat01"
    bl_label = "Add Natural Light"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
            create_light(self, context, nat_01)
            return {'FINISHED'}
            
class OBJECT_OT_add_nat02(Operator, AddObjectHelper):
    bl_idname = "light.add_nat02"
    bl_label = "Add Natural Light"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
            create_light(self, context, nat_02)
            return {'FINISHED'}

# Incandescent lights
class OBJECT_OT_add_inc01(Operator, AddObjectHelper):
    bl_idname = "light.add_inc_01"
    bl_label = "Add Incandescent Light"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
            create_light(self, context, inc_01)
            return {'FINISHED'}

class OBJECT_OT_add_inc02(Operator, AddObjectHelper):
    bl_idname = "light.add_inc_02"
    bl_label = "Add Incandescent Light"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
            create_light(self, context, inc_02)
            return {'FINISHED'}

# LED lights
class OBJECT_OT_add_led01(Operator, AddObjectHelper):
    bl_idname = "light.add_led_01"
    bl_label = "Add LED Light"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
            create_light(self, context, led_01)
            return {'FINISHED'}

class OBJECT_OT_add_led02(Operator, AddObjectHelper):
    bl_idname = "light.add_led_02"
    bl_label = "Add LED Light"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
            create_light(self, context, led_02)
            return {'FINISHED'}

class OBJECT_OT_add_led03(Operator, AddObjectHelper):
    bl_idname = "light.add_led_03"
    bl_label = "Add LED Light"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
            create_light(self, context, led_03)
            return {'FINISHED'}

class OBJECT_OT_add_led04(Operator, AddObjectHelper):
    bl_idname = "light.add_led_04"
    bl_label = "Add LED Light"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
            create_light(self, context, led_04)
            return {'FINISHED'}

class OBJECT_OT_add_led05(Operator, AddObjectHelper):
    bl_idname = "light.add_led_05"
    bl_label = "Add LED Light"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
            create_light(self, context, led_05)
            return {'FINISHED'}

class OBJECT_OT_add_led06(Operator, AddObjectHelper):
    bl_idname = "light.add_led_06"
    bl_label = "Add LED Light"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
            create_light(self, context, led_06)
            return {'FINISHED'}

# Flourescent lights
class OBJECT_OT_add_fl01(Operator, AddObjectHelper):
    bl_idname = "light.add_fl_01"
    bl_label = "Add Flourescent Light"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
            create_light(self, context, fl_01)
            return {'FINISHED'}

class OBJECT_OT_add_fl02(Operator, AddObjectHelper):
    bl_idname = "light.add_fl_02"
    bl_label = "Add Flourescent Light"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
            create_light(self, context, fl_02)
            return {'FINISHED'}

# Create menu items

class NaturalsMenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_naturals_menu"
    bl_label = "Natural"

    def draw(self, context):
        layout = self.layout
        self.layout.operator(
            OBJECT_OT_add_nat01.bl_idname,
            text=nat_01.name,
            icon='LIGHT_'+nat_01.lightType)
        self.layout.operator(
            OBJECT_OT_add_nat02.bl_idname,
            text=nat_02.name,
            icon='LIGHT_'+nat_02.lightType)

class IncandescentsMenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_incandescents_menu"
    bl_label = "Incandescent"

    def draw(self, context):
        layout = self.layout
        self.layout.operator(
            OBJECT_OT_add_inc01.bl_idname,
            text=inc_01.name,
            icon='LIGHT_'+inc_01.lightType)
        self.layout.operator(
            OBJECT_OT_add_inc02.bl_idname,
            text=inc_02.name,
            icon='LIGHT_'+inc_02.lightType)

class LEDsMenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_leds_menu"
    bl_label = "LED"

    def draw(self, context):
        layout = self.layout
        self.layout.operator(
            OBJECT_OT_add_led01.bl_idname,
            text=led_01.name,
            icon='LIGHT_'+led_01.lightType)
        self.layout.operator(
            OBJECT_OT_add_led02.bl_idname,
            text=led_02.name,
            icon='LIGHT_'+led_02.lightType)
        self.layout.operator(
            OBJECT_OT_add_led03.bl_idname,
            text=led_03.name,
            icon='LIGHT_'+led_03.lightType)
        self.layout.operator(
            OBJECT_OT_add_led04.bl_idname,
            text=led_04.name,
            icon='LIGHT_'+led_04.lightType)
        self.layout.operator(
            OBJECT_OT_add_led05.bl_idname,
            text=led_05.name,
            icon='LIGHT_'+led_05.lightType)
        self.layout.operator(
            OBJECT_OT_add_led06.bl_idname,
            text=led_06.name,
            icon='LIGHT_'+led_06.lightType)

class FlourescentsMenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_flourescents_menu"
    bl_label = "Flourescent"

    def draw(self, context):
        layout = self.layout
        self.layout.operator(
            OBJECT_OT_add_fl01.bl_idname,
            text=fl_01.name,
            icon='LIGHT_'+fl_01.lightType)
        self.layout.operator(
            OBJECT_OT_add_fl02.bl_idname,
            text=fl_02.name,
            icon='LIGHT_'+fl_02.lightType)

def draw_NaturalsMenu(self, context):
    self.layout.menu(NaturalsMenu.bl_idname, icon='LIGHT')

def draw_IncandescentsMenu(self, context):
    self.layout.menu(IncandescentsMenu.bl_idname, icon='LIGHT')

def draw_LEDsMenu(self, context):
    self.layout.menu(LEDsMenu.bl_idname, icon='LIGHT')

def draw_FlourescentsMenu(self, context):
    self.layout.menu(FlourescentsMenu.bl_idname, icon='LIGHT')

# Registration 

classes = (
    NaturalsMenu,
    IncandescentsMenu,
    LEDsMenu,
    FlourescentsMenu,

    OBJECT_OT_add_nat01,
    OBJECT_OT_add_nat02,

    OBJECT_OT_add_inc01,
    OBJECT_OT_add_inc02,

    OBJECT_OT_add_led01,
    OBJECT_OT_add_led02,
    OBJECT_OT_add_led03,
    OBJECT_OT_add_led04,
    OBJECT_OT_add_led05,
    OBJECT_OT_add_led06,
    
    OBJECT_OT_add_fl01,
    OBJECT_OT_add_fl02,
)
        
def register():
    for cls in classes:
        register_class(cls)

    bpy.types.VIEW3D_MT_light_add.append(draw_NaturalsMenu)
    bpy.types.VIEW3D_MT_light_add.append(draw_IncandescentsMenu)
    bpy.types.VIEW3D_MT_light_add.append(draw_LEDsMenu)
    bpy.types.VIEW3D_MT_light_add.append(draw_FlourescentsMenu)
    
def unregister():
    for cls in reversed(classes):
        unregister_class(cls)

    bpy.types.VIEW3D_MT_mesh_add.remove(draw_NaturalsMenu)
    bpy.types.VIEW3D_MT_mesh_add.remove(draw_IncandescentsMenu)
    bpy.types.VIEW3D_MT_light_add.remove(draw_LEDsMenu)
    bpy.types.VIEW3D_MT_light_add.remove(draw_FlourescentsMenu)

if __name__ == "__main__":
    register()