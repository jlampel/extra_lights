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
from bpy.props import IntProperty, BoolProperty, FloatVectorProperty
from bpy.types import Operator, PropertyGroup
from bpy.utils import register_class, unregister_class
import os
from pathlib import Path

# Append Lumens Converters if they're not already in the file

if os.path.dirname(os.path.abspath(__file__)) == 'C:\\':
    nodes_directory = "C:/Users/jonat/Documents/GitHub/extra-lights" + "/real_lights.blend\\NodeTree\\"
else: 
    nodes_directory = os.path.dirname(os.path.abspath(__file__)) + "/real_lights.blend\\NodeTree\\"

if (bpy.data.node_groups.find("Lumens Converter") == -1):
    bpy.ops.wm.append(
        filename = "Lumens Converter", 
        directory = nodes_directory
    )
if (bpy.data.node_groups.find("Spot Lumens Converter") == -1):
    bpy.ops.wm.append(
        filename = "Spot Lumens Converter", 
        directory = nodes_directory
    )
if (bpy.data.node_groups.find("Area Lumens Converter") == -1):
    bpy.ops.wm.append(
        filename = "Area Lumens Converter", 
        directory = nodes_directory
    )

# set light properties 

class Light:
    def __init__(self, name, id, lightType, radius, temp, strength):
        self.name = name
        self.id = id
        self.lightType = lightType
        self.radius = radius
        self.temp = temp
        self.strength = strength

nat_01 = Light("Candle", "candle", "POINT", 0.015, 1800, 12)
nat_02 = Light("Fireplace", "fireplace", "POINT", 0.228, 2000, 500)
nat_03 = Light("Sunset", "sunset", "SUN", 0.75, 3000, 500)
nat_04 = Light("Overcast Sun", "overcast", "SUN", 50, 7000, 250)
nat_05 = Light("Direct Sun", "directsun", "SUN", 0.526, 5250, 1000)
natural_lights = [nat_01, nat_02, nat_03, nat_04, nat_05]

inc_01 = Light("70 lm C7 Candelabra Appliance Light", "70c7", "POINT", 0.015, 2700, 70)
inc_02 = Light("250 lm Vintage Tungsten Decorative Light", "vintage", "POINT", 0.025, 2700, 250)
inc_03 = Light("200 lm A15 Appliance Light", "200a15", "POINT", 0.0216, 2700, 200)
inc_04 = Light("400 lm A15 Appliance Light", "400a15", "POINT", 0.0216, 2700, 400)
inc_05 = Light("1000 lm A19 Lamp Light", "1000a19", "POINT", 0.03, 2700, 1000)
inc_06 = Light("2700 lm A21 Ceiling Light", "2700a21", "AREA", ["Disk", 0.033], 2700, 2700)
inc_07 = Light("3000 lm Halogen Car Headlight", "3000headlight", "SPOT", [125, 0.02], 4100, 3000)
inc_08 = Light("3800 lm A21 Ceiling Light", "3800a21", "AREA", ["DISK", 0.033], 2700, 3800)
inc_09 = Light("5800 lm PS30 Barn Light", "5800ps30", "AREA", ["DISK", 0.038], 2700, 5800)
incandescent_lights = [inc_01, inc_02, inc_03, inc_04, inc_05, inc_06, inc_07, inc_08, inc_09]

led_01 = Light("400 lm Flashlight", "400flashlight", "SPOT", [65, 0.0075], 2700, 400)
led_02 = Light("800 lm A19 Lamp LED", "800a19", "POINT", 0.034, 3000, 800)
led_03 = Light("1400 lm Flashlight", "1400flashlight", "SPOT", [65, 0.0075], 4000, 1400)
led_04 = Light("1500 lm PAR38 Outdoor Floodlight", "1400par38", "AREA", ["DISK", 0.06], 3000, 1500)
led_05 = Light("1600 lm A21 Ceiling LED", "1600a21", "AREA", ["DISK", 0.034], 5000, 1600)
led_06 = Light("2500 lm Photography LED Bar", "2500bar", "AREA", ["RECTANGLE", 0.03, 0.4], 5500, 2500)
led_07 = Light("2600 lm PAR38 Outdoor Floodlight", "2600par38", "AREA", ["DISK", 0.06], 3000, 2600)
led_08 = Light("3350 lm Photography LED Pack", "3350pack", "AREA", ["RECTANGLE", 0.23, 0.178], 5600, 3350)
led_09 = Light("5000 lm LED Car Headlight", "headlightled", "SPOT", [125, 0.02], 6500, 5000)
led_10 = Light("9100 lm Industrial LED Wall Pack", "9100flood", "AREA", ["RECTANGLE", 0.23, 0.178], 5000, 9100)
led_lights = [led_01, led_02, led_03, led_04, led_05, led_06, led_07, led_08, led_09, led_10] 

fl_01 = Light("1500 lm Photography Umbrella", "1500ubmrella", "AREA", ["DISK", 0.838], 5000, 1500)
fl_02 = Light("2000 lm Photography Softbox", "2000softbox", "AREA", ["SQUARE", 0.61], 5000, 2000)
fl_03 = Light("2250 lm Photography CFL", "2250cfl", "POINT", 0.03, 5500, 2250)
fl_04 = Light("2500 lm Fluorescent Tube", "2500tube", "AREA", ["RECTANGLE", 0.05, 1.22], 5000, 2500)
fl_05 = Light("4500 lm Daylight CFL", "4500cfl", "POINT", 0.03, 6500, 4500)
fluorescent_lights = [fl_01, fl_02, fl_03, fl_04, fl_05]

all_lights = natural_lights + incandescent_lights + led_lights + fluorescent_lights

# Add new light
def create_light(self, context, light, colType, temp, tint, useNodes, useSky, spotSize):
    bpy.ops.object.light_add(type=light.lightType)
    bpy.context.active_object.name = light.name
    light_object = bpy.context.active_object
    light_data = light_object.data

    def setup_nodes(): 
        light_data.energy = 1
        col = [tint[0], tint[1], tint[2], 1.0]
        light_data.use_nodes = True
        nodes = light_data.node_tree.nodes

        if light.lightType == "SUN":
            nodes["Emission"].inputs[1].default_value = light.strength
            k = nodes.new("ShaderNodeBlackbody")
            k.inputs[0].default_value = temp
            light_data.node_tree.links.new(k.outputs[0], nodes["Emission"].inputs[0])
        else:
            lumens_node = nodes.new("ShaderNodeGroup")
            if light.lightType == "SPOT":
                lumens_node.node_tree = bpy.data.node_groups["Spot Lumens Converter"]
                lumens_node.inputs[3].default_value = spotSize
            elif light.lightType == "AREA":
                lumens_node.node_tree = bpy.data.node_groups["Area Lumens Converter"]
            else:
                lumens_node.node_tree = bpy.data.node_groups["Lumens Converter"]
            light_data.node_tree.links.new(lumens_node.outputs[0], nodes["Light Output"].inputs[0])
            lumens_node.inputs[0].default_value = light.strength
            if colType == "rgb":
                lumens_node.inputs[1].default_value = 6000
                lumens_node.inputs[2].default_value = col
            else:
                lumens_node.inputs[1].default_value = temp
    
    def setup_color():
        if colType == "rgb":
            light_data.color = tint
        else: 
            light_data.color = convert_kelvin(light.temp)

    def setup_sky():
        bpy.ops.world.new()
        world = bpy.data.worlds["World"]
        world.name = light.name + " World"
        bpy.context.scene.world = world
        nodes = world.node_tree.nodes

        sky_texture = nodes.new("ShaderNodeTexSky")
        world.node_tree.links.new(sky_texture.outputs[0], nodes["Background"].inputs[0])
        dr = sky_texture.driver_add("sun_direction")
        for i in range(3):
            dr[i].driver.expression = "var"
            var = dr[i].driver.variables.new()
            var.targets[0].id = light_object
            var.targets[0].data_path = "matrix_world[2]["+str(i)+"]"

        if light.id == "sunset":
            sky_texture.turbidity = 3
            nodes["Background"].inputs[1].default_value = 250
        elif light.id == "overcast":
            sky_texture.turbidity = 8
            nodes["Background"].inputs[1].default_value = 100
        else:
            nodes["Background"].inputs[1].default_value = 750
        
    def to_linear(i):
        if i <= 0.04045 :
            x = i * (1.0 / 12.92)
        else:
            x = pow( (i + 0.055) * (1.0 / (1 + 0.055)), 2.4)
        return x
    
    def convert_kelvin(kelvin):
        kelvin_table = {
            # Thanks to Andreas Siess: https://andi-siess.de/rgb-to-color-temperature/
            1000: [255, 56, 0], 1100: [255, 71, 0], 1200: [255, 83, 0], 1300: [255, 93, 0], 1400: [255, 101, 0], 1500: [255, 109, 0], 1600: [255, 115, 0], 1700: [255, 121, 0], 1800: [255, 126, 0], 1900: [255, 131, 0],
            2000: [255, 138, 18], 2100: [255, 142, 33], 2200: [255, 147, 44], 2300: [255, 152, 54], 2400: [255, 157, 63], 2500: [255, 161, 72], 2600: [255, 165, 79], 2700: [255, 169, 87], 2800: [255, 173, 94], 2900: [255, 177, 101],
            3000: [255, 180, 107], 3100: [255, 184, 114], 3200: [255, 187, 120], 3300: [255, 190, 126], 3400: [255, 193, 132], 3500: [255, 196, 137], 3600: [255, 199, 143], 3700: [255, 201, 148], 3800: [255, 204, 153], 3900: [255, 206, 159], 
            4000: [255, 209, 163], 4100: [255, 211, 168], 4200: [255, 213, 173], 4300: [255, 215, 177], 4400: [255, 217, 182], 4500: [255, 219, 186], 4600: [255, 221, 190], 4700: [255, 223, 194], 4800: [255, 225, 198], 4900: [255, 227, 202],
            5000: [255, 228, 206], 5100: [255, 230, 210], 5200: [255, 232, 213], 5300: [255, 233, 217], 5400: [255, 235, 220], 5500: [255, 236, 224], 5600: [255, 238, 227], 5700: [255, 239, 230], 5800: [255, 240, 233], 5900: [255, 242, 236],            
            6000: [255, 243, 239], 6100: [255, 244, 242], 6200: [255, 245, 245], 6300: [255, 246, 247], 6400: [255, 248, 251], 6500: [255, 249, 253], 6600: [254, 249, 255], 6700: [252, 247, 255], 6800: [249, 246, 255], 6900: [247, 245, 255],
            7000: [245, 243, 255], 7100: [243, 242, 255], 7200: [240, 241, 255], 7300: [239, 240, 255], 7400: [237, 239, 255], 7500: [235, 238, 255], 7600: [233, 237, 255], 7700: [231, 236, 255], 7800: [230, 235, 255], 7900: [228, 234, 255],
            8000: [227, 233, 255], 8100: [225, 232, 255], 8200: [224, 231, 255], 8300: [222, 230, 255], 8400: [221, 230, 255], 8500: [220, 229, 255], 8600: [218, 229, 255], 8700: [217, 227, 255], 8800: [216, 227, 255], 8900: [215, 226, 255], 
            9000: [214, 225, 255], 9100: [212, 225, 255], 9200: [211, 224, 255], 9300: [210, 223, 255], 9400: [209, 223, 255], 9500: [208, 222, 255], 9600: [207, 221, 255], 9700: [207, 221, 255], 9800: [206, 220, 255], 9900: [205, 220, 255],
            10000: [207, 218, 255], 10100: [207, 218, 255], 10200: [206, 217, 255], 10300: [205, 217, 255], 10400: [204, 216, 255], 10500: [204, 216, 255], 10600: [203, 215, 255], 10700: [202, 215, 255], 10800: [202, 214, 255], 10900: [201, 214, 255],
            11000: [200, 213, 255], 11100: [200, 213, 255], 11200: [199, 212, 255], 11300: [198, 212, 255], 11400: [198, 212, 255], 11500: [197, 211, 255], 11600: [197, 211, 255], 11700: [197, 210, 255], 11800: [196, 210, 255], 11900: [195, 210, 255],
            12000: [195, 209, 255]
        }
        rgb = kelvin_table[round(kelvin, -2)]

        color = [to_linear(rgb[0]/255), to_linear(rgb[1]/255), to_linear(rgb[2]/255)]
        return color

    def convert_lumens(lumens, rgb):
        power = lumens / ( (rgb[0] * 145.256) + (rgb[1] * 488.449) + (rgb[2] * 49.2955) )
        return power
    
    # Set light properties 
    if light.lightType == "POINT":
        light_data.shadow_soft_size = light.radius
        if useNodes == True:
            setup_nodes()
        else:
            setup_color()
            light_data.energy = convert_lumens(light.strength, light_data.color)
            light_data.use_custom_distance = True
            
    elif light.lightType == "SPOT":
        light_object.rotation_euler[0] = 1.5708
        light_data.shadow_soft_size = light.radius[1]
        light_data.spot_size = spotSize / 57.2957795 

        if useNodes == True:
            setup_nodes()
        else:
            setup_color()
            light_data.energy = convert_lumens(light.strength, light_data.color) * (360 / spotSize)
            light_data.use_custom_distance = True
            
    elif light.lightType == "AREA":
        light_data.shape = light.radius[0]
        if light_data.shape == "SQUARE" or "DISK":
            light_data.size = light.radius[1]
        elif light_data.shape == "RECTANGLE" or "ELLIPSE":
            light_data.size = light.radius[1]
            light_data.size_y = light.radius[2]

        if useNodes == True:
            setup_nodes()
        else:
            setup_color()
            light_data.energy = convert_lumens(light.strength, light_data.color) * 1.95
            light_data.use_custom_distance = True
            
    elif light.lightType == "SUN":
        light_data.angle = light.radius
        if light.id == "sunset":
            light_object.rotation_euler[0] = 1.4835
            light_object.rotation_euler[1] = 0.785398
        else:
            light_object.rotation_euler[0] = 0.785398
            light_object.rotation_euler[1] = 0.785398

        # Set the sun slightly above the camera
        if bpy.context.scene.camera != None:
            z = (125/100) * bpy.context.scene.camera.location[2]
            light_object.location[2] = z

        if useNodes == True:
            setup_nodes()
        else: 
            light_data.energy = light.strength
            light_data.color = convert_kelvin(light.temp)
            
        if useSky:
            setup_sky()
        
    
# Create operators
def create_light_operator(light):
    class OBJECT_OT_add_light(Operator):
        bl_idname = "light.add_" + light.id
        bl_label = "Add a " + light.name + " light"
        bl_description = "Creates a physically based light"
        bl_options = {'REGISTER', 'UNDO'}
        name = light.name
        lightType = light.lightType
        
        if light.lightType == "SUN":
            strength: bpy.props.IntProperty(
                name = "Irradiance",
                default = light.strength,
                min = 50,
                max = 2000,
                description = "Amound of light that hits a direct surface as measured in watts per square meter",
            )
        else:
            strength: bpy.props.IntProperty(
                name = "Lumens",
                default = light.strength,
                min = 5,
                max = 20000,
                description = "Amound of percieved light emitted as measured in lumens",
            )
        if light.lightType == "SPOT":
            spotSize: bpy.props.IntProperty(
                name = "Spot Angle",
                default = light.radius[0],
                min = 1,
                max = 180,
                description = "Setting the spot angle here will keep the total amount of light generated the same regardless of the spot size",
            )
        else: 
            spotSize: bpy.props.IntProperty(
                name = "Spot Angle",
                default = 65,
                min = 1,
                max = 180,
                description = "This prop should never appear. It just avoids a float object being unsubscriptable error",
            )
        useNodes: bpy.props.BoolProperty(
            name = "Use Nodes (Cycles only)",
            default = False,
            description = "Create light with nodes so that lumens and color temperature can be changed at any time. Currently only works with Cycles."
        )
        colType: bpy.props.EnumProperty(
            items = [
                ("kelvin", "Kelvin Temperature", "Set the light color according to Kelvin values"),
                ("rgb", "RGB Color", "Set the light color to a specific RGB value")
            ],
            name = "Set Color With",
            description = "Set the light's color with either Kelvin or RGB values",
            default = "kelvin",
        )
        temp: bpy.props.IntProperty(
            name = "Color Temperature",
            default = light.temp,
            min = 1500,
            max = 12000,
            description = "Color of the light according to the Kelvin temperature scale",
        )
        tint: bpy.props.FloatVectorProperty(
            subtype = 'COLOR',
            name = "Color Tint",
            default = (1.0, 1.0, 1.0),
            description = "Sets the RGB color of the light"
        )
        useSky: bpy.props.BoolProperty(
            name = "Create Linked Sky (Cylces only)",
            default = False,
            description = "Create a new World with a Sky texture linked to the rotation of the sun lamp. Currently the Sky texture only renderes correctly in Cycles."
        )

        def draw(self, context):
            layout = self.layout
            layout.use_property_split = True
            layout.use_property_decorate = False

            layout.prop(self, "strength")
            layout.prop(self, "colType")

            if light.lightType == "SUN":
                layout.prop(self, "temp")
            else:
                if self.colType == "kelvin":
                    layout.prop(self, "temp")
                else:
                    layout.prop(self, "tint")
                
            layout.prop(self, "useNodes")

            if light.lightType == "SUN":
                layout.prop(self, "useSky")
            elif light.lightType == "SPOT":
                layout.prop(self, "spotSize")


        def execute(self, context):
                create_light(self, context, light, self.colType, self.temp, self.tint, self.useNodes, self.useSky, self.spotSize)
                return {'FINISHED'}
    return OBJECT_OT_add_light

natural_operators = [create_light_operator(light) for light in natural_lights]
incandescent_operators = [create_light_operator(light) for light in incandescent_lights]
led_operators = [create_light_operator(light) for light in led_lights]
fluorescent_operators = [create_light_operator(light) for light in fluorescent_lights]

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

class FluorescentsMenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_fluorescents_menu"
    bl_label = "Fluorescent"
    def draw(self, context):
        layout = self.layout
        for op in fluorescent_operators:
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
def draw_FluorescentsMenu(self, context):
    self.layout.menu(FluorescentsMenu.bl_idname, icon='LIGHT')

# Registration 
classes = [NaturalsMenu, IncandescentsMenu, LEDsMenu, FluorescentsMenu]
for op in natural_operators:
    classes.append(op)
for op in incandescent_operators:
    classes.append(op)
for op in led_operators:
    classes.append(op)
for op in fluorescent_operators:
    classes.append(op)

def register():
    for cls in classes:
        register_class(cls)
    bpy.types.VIEW3D_MT_light_add.append(draw_NaturalsMenu)
    bpy.types.VIEW3D_MT_light_add.append(draw_IncandescentsMenu)
    bpy.types.VIEW3D_MT_light_add.append(draw_LEDsMenu)
    bpy.types.VIEW3D_MT_light_add.append(draw_FluorescentsMenu)

def unregister():
    for cls in reversed(classes):
        unregister_class(cls)
    bpy.types.VIEW3D_MT_mesh_add.remove(draw_NaturalsMenu)
    bpy.types.VIEW3D_MT_mesh_add.remove(draw_IncandescentsMenu)
    bpy.types.VIEW3D_MT_light_add.remove(draw_LEDsMenu)
    bpy.types.VIEW3D_MT_light_add.remove(draw_FluorescentsMenu)

if __name__ == "__main__":
    register()