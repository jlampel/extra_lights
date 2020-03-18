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
from bpy.props import IntProperty
from bpy.types import Operator, PropertyGroup
from bpy.utils import register_class, unregister_class
from bpy_extras.object_utils import AddObjectHelper, object_data_add

# set light properties 

class Light:
    def __init__(self, name, id, lightType, radius, temp, lumens):
        self.name = name
        self.id = id
        self.lightType = lightType
        self.radius = radius
        self.temp = temp
        self.lumens = lumens

nat_01 = Light("Candle", "candle", "POINT", 0.015, 1800, 12)
nat_02 = Light("Fireplace", "fireplace", "POINT", 0.228, 2000, 500)
natural_lights = [nat_01, nat_02]

inc_01 = Light("10w C7 Candelabra", "10wc7", "POINT", 0.015, 2700, 70)
inc_02 = Light("Vintage Tungsten", "vintage", "POINT", 0.025, 2700, 245)
inc_03 = Light("25w A15", "25wa15", "POINT", 0.0216, 2700, 210)
inc_04 = Light("40w A15", "40wa15", "POINT", 0.0216, 2700, 400)
inc_05 = Light("75w A19", "75wa19", "POINT", 0.03, 2775, 1050)
inc_06 = Light("150w A21", "150wa21", "POINT", 0.033, 2700, 1050)
inc_07 = Light("200w A21", "200wa21", "POINT", 0.033, 2700, 3880)
inc_08 = Light("Halogen Car Headlight", "headlighth", "SPOT", 0.02, 4100, 3000)
inc_09 = Light("300w PS30", "300wps30", "POINT", 0.038, 2700, 5870)
incandescent_lights = [inc_01, inc_02, inc_03, inc_04, inc_05, inc_06, inc_07, inc_08, inc_09]

led_01 = Light("400 Lumen Flashlight", "400flashlight", "SPOT", 0.0075, 2700, 400)
led_02 = Light("1400 Lumen Flashlight", "1400flashlight", "SPOT", 0.0075, 4000, 1400)
led_03 = Light("60w A19 White LED", "60wa19", "POINT", 0.034, 3000, 800)
led_04 = Light("100w A21 Daylight LED", "100wa21", "POINT", 0.034, 5000, 1600)
led_05 = Light("150w PAR38 White LED", "150wpar38", "POINT", 0.06, 3000, 1400)
led_06 = Light("250w PAR38 White LED", "250wpar38", "POINT", 0.06, 3000, 2600)
led_07 = Light("LED Car Headlight", "headlightled", "SPOT", 0.02, 6500, 5000)
led_08 = Light("350w Outdoor Flood", "350wflood", "AREA", 0.178, 5000, 9100)
led_lights = [led_01, led_02, led_03, led_04, led_05, led_06, led_07, led_08]

fl_01 = Light("45w Daylight CFL", "45wcfl", "POINT", 0.03, 5500, 2250)
fl_02 = Light("85w Daylight CFL", "45wcfl", "POINT", 0.03, 6500, 4500)
flourescent_lights = [fl_01, fl_02]

all_lights = natural_lights + incandescent_lights + led_lights + flourescent_lights

# Add new light
def create_light(self, context, light, strength, temp):
    light_data = bpy.data.lights.new(name=light.name, type=light.lightType)
    light_object = bpy.data.objects.new(name=light.name, object_data=light_data)
    bpy.context.collection.objects.link(light_object)
    bpy.ops.object.select_all(action='DESELECT')
    light_object.select_set(state = True)
    context.view_layer.objects.active = light_object

    # Append Lumens Converter if it's not already in the file
    if (bpy.data.node_groups.find("Lumens Converter") == -1):
        bpy.ops.wm.append(
            filename = "Lumens Converter", 
            directory = "C:/Users/jonat/Documents/GitHub/extra-lights/lights/real_lights.blend\\NodeTree\\"
        )
    
    # Create nodes
    def setup_lumens(): 
        light_data.energy = 1
        light_data.use_nodes = True
        nodes = light_data.node_tree.nodes
        links = light_data.node_tree.links

        lumens_node = nodes.new("ShaderNodeGroup")
        lumens_node.node_tree = bpy.data.node_groups["Lumens Converter"]
        links.new(lumens_node.outputs[0], nodes["Light Output"].inputs[0])

        lumens_node.inputs[0].default_value = strength
        lumens_node.inputs[1].default_value = temp
    
    # Set properties 
    if light.lightType == "SPOT" or "POINT":
        setup_lumens()
        light_data.shadow_soft_size = light.radius
    elif light.lightType == "AREA":
        setup_lumens()
        light_data.size = light.radius
    elif light.lightType == "SUN":
        light_data.energy = strength
        light_data.angle = light.radius
    
    # Set location and rotation
    light_object.location = bpy.context.scene.cursor.location
    if light.lightType == "SPOT":
        light_object.rotation_euler[0] = 1.5708
    elif light.lightType == "SUN":
        light_object.rotation_euler[0] = 0.785398
        light_object.rotation_euler[1] = 0.785398
    
# Create operators
def create_light_operator(light):
    class OBJECT_OT_add_light(Operator, AddObjectHelper):
        bl_idname = "light.add_" + light.id
        bl_label = "Add a " + light.name + " light"
        bl_description = "Creates a physically based light"
        bl_options = {'REGISTER', 'UNDO'}
        name = light.name
        lightType = light.lightType

        strength: bpy.props.IntProperty(
            name = "Lumens",
            default = light.lumens,
            min = 5,
            max = 20000,
            description = "Amound of percieved light emitted as measured in lumens",
        )
        
        temp: bpy.props.IntProperty(
            name = "Color Temperature",
            default = light.temp,
            min = 1500,
            max = 8000,
            description = "Color of the light according to the Kelvin temperature scale",
        )

        def execute(self, context):
                create_light(self, context, light, self.strength, self.temp)
                return {'FINISHED'}
    return OBJECT_OT_add_light
natural_operators = [create_light_operator(light) for light in natural_lights]
incandescent_operators = [create_light_operator(light) for light in incandescent_lights]
led_operators = [create_light_operator(light) for light in led_lights]
flourescent_operators = [create_light_operator(light) for light in flourescent_lights]

# Create menu items
class NaturalsMenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_naturals_menu"
    bl_label = "Natural"
    def draw(self, context):
        layout = self.layout
        for op in natural_operators:
            self.layout.operator(
                op.bl_idname,
                text=op.name,
                icon='LIGHT_'+op.lightType)

class IncandescentsMenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_incandescents_menu"
    bl_label = "Incandescent"
    def draw(self, context):
        layout = self.layout
        for op in incandescent_operators:
            self.layout.operator(
                op.bl_idname,
                text=op.name,
                icon='LIGHT_'+op.lightType)

class LEDsMenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_leds_menu"
    bl_label = "LED"
    def draw(self, context):
        layout = self.layout
        for op in led_operators:
            self.layout.operator(
                op.bl_idname,
                text=op.name,
                icon='LIGHT_'+op.lightType)

class FlourescentsMenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_flourescents_menu"
    bl_label = "Flourescent"
    def draw(self, context):
        layout = self.layout
        for op in flourescent_operators:
            self.layout.operator(
                op.bl_idname,
                text=op.name,
                icon='LIGHT_'+op.lightType)

def draw_NaturalsMenu(self, context):
    self.layout.menu(NaturalsMenu.bl_idname, icon='LIGHT')
def draw_IncandescentsMenu(self, context):
    self.layout.menu(IncandescentsMenu.bl_idname, icon='LIGHT')
def draw_LEDsMenu(self, context):
    self.layout.menu(LEDsMenu.bl_idname, icon='LIGHT')
def draw_FlourescentsMenu(self, context):
    self.layout.menu(FlourescentsMenu.bl_idname, icon='LIGHT')

# Registration 
classes = [NaturalsMenu, IncandescentsMenu, LEDsMenu, FlourescentsMenu]
for op in natural_operators:
    classes.append(op)
for op in incandescent_operators:
    classes.append(op)
for op in led_operators:
    classes.append(op)
for op in flourescent_operators:
    classes.append(op)

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