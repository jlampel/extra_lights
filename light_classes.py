import bpy
import os
from pathlib import Path
from bpy.types import Operator, PropertyGroup
from bpy.props import IntProperty, BoolProperty, FloatVectorProperty

from . import conversions

if os.path.dirname(os.path.abspath(__file__)) == 'C:\\':
    nodes_directory = "C:/Users/jonat/Documents/GitHub/extra-lights" + "/real_lights.blend\\NodeTree\\"
else: 
    nodes_directory = os.path.dirname(os.path.abspath(__file__)) + "/real_lights.blend\\NodeTree\\"

class props:
    def colType(self):
        return bpy.props.EnumProperty(
            items = [
                ("kelvin", "Kelvin Temperature", "Set the light color according to Kelvin values"),
                ("rgb", "RGB Color", "Set the light color to a specific RGB value")
            ],
            name = "Set Color With",
            description = "Set the light's color with either Kelvin or RGB values",
            default = "kelvin",
        )
    def irradiance(self, x):
        return bpy.props.IntProperty(
            name = "Irradiance",
            default = x,
            min = 50,
            max = 2000,
            description = "Amound of light that hits a direct surface as measured in watts per square meter",
        )
    def lumens(self, x):
        return bpy.props.IntProperty(
            name = "Lumens",
            default = x,
            min = 5,
            max = 20000,
            description = "Amound of percieved light emitted as measured in lumens",
        )
    def setExposure(self):
        return bpy.props.BoolProperty(
            name = "Set Exposure",
            default = False,
            description = "Set the scene exposure to approximately match the added light. Exposusure heavily depends on context, so it's recommended that you adjust it further before your final render."
        )
    def spotAngle(self, x):
        return bpy.props.IntProperty(
            name = "Spot Angle",
            default = x,
            min = 1,
            max = 180,
            description = "Setting the spot angle here will keep the total amount of light generated the same regardless of the spot size",
        )
    def temp(self, x):
        return bpy.props.IntProperty(
            name = "Color Temperature",
            default = x,
            min = 1500,
            max = 12000,
            description = "Color of the light according to the Kelvin temperature scale",
        )
    def tint(self):
        return bpy.props.FloatVectorProperty(
            subtype = 'COLOR',
            name = "Color Tint",
            default = (1.0, 1.0, 1.0),
            description = "Sets the RGB color of the light"
        )
    def useNodes(self):
        return bpy.props.BoolProperty(
            name = "Use Nodes (Cycles only)",
            default = False,
            description = "Create light with nodes so that lumens and color temperature can be changed at any time. Currently only works with Cycles."
        )    
    def useSky(self):
        return bpy.props.BoolProperty(
            name = "Create Linked Sky (Cylces only)",
            default = False,
            description = "Create a new World with a Sky texture linked to the rotation of the sun lamp. Currently the Sky texture only renderes correctly in Cycles."
        )

class setup:
    def nodeColor(self, lumensNode, colType, col, temp):
        if colType == "rgb":
            lumensNode.inputs[1].default_value = 6000
            lumensNode.inputs[2].default_value = col
        else:
            lumensNode.inputs[1].default_value = self.temp
    def nodeless(self, data, colType, tint, temp, lumens):
        if colType == "rgb":
            data.color = self.tint
        else: 
            data.color = conversions.kelvin(self.temp)
        data.energy = conversions.lumens(self.lumens, data.color)

class PointLight:
    def __init__(self, name, tag, radius, temp, lumens, exposure):
        self.name = name
        self.tag = tag
        self.radius = radius
        self.temp = temp
        self.lumens = lumens
        self.exposure = exposure

    def create_light(self):
        class OBJECT_OT_add_light(Operator):
            bl_idname = "light.add_" + self.tag
            bl_label = "Add a " + self.name
            bl_description = "Creates a physically based light"
            bl_options = {'REGISTER', 'UNDO'}

            name = self.name
            lightType = 'POINT'

            lumens: props.lumens(self, self.lumens)
            colType: props.colType(self)
            temp: props.temp(self, self.temp)
            tint: props.tint(self)
            useNodes: props.useNodes(self)
            setExposure: props.setExposure(self)

            def draw(self, context):
                layout = self.layout
                layout.use_property_split = True
                layout.use_property_decorate = False

                layout.prop(self, "lumens")
                layout.prop(self, "colType")
                if self.colType == "kelvin":
                    layout.prop(self, "temp")
                else:
                    layout.prop(self, "tint")
                layout.prop(self, "useNodes")
                layout.prop(self, "setExposure")

            def execute(self, context):
                bpy.ops.object.light_add(type='POINT')
                bpy.context.active_object.name = self.name
                ob = bpy.context.active_object
                data = ob.data

                data.shadow_soft_size = self.radius
                data.use_custom_distance = True

                if self.useNodes:
                    if bpy.data.node_groups.find("Lumens Converter") == -1:
                        bpy.ops.wm.append(filename = "Lumens Converter", directory = nodes_directory)

                    data.energy = 1
                    col = [self.tint[0], self.tint[1], self.tint[2], 1.0]
                    data.use_nodes = True
                    nodes = data.node_tree.nodes

                    lumensNode = nodes.new("ShaderNodeGroup")
                    lumensNode.node_tree = bpy.data.node_groups["Lumens Converter"]
                    data.node_tree.links.new(lumensNode.outputs[0], nodes["Light Output"].inputs[0])
                    lumensNode.inputs[0].default_value = self.lumens
                    setup.nodeColor(self, lumensNode, self.colType, col, self.temp)

                else:
                    setup.nodeless(self, data, self.colType, self.tint, self.temp, self.lumens)

                if self.setExposure:
                    bpy.context.scene.view_settings.exposure = self.exposure

                return {'FINISHED'}
        return OBJECT_OT_add_light

class SpotLight:
    def __init__(self, name, tag, radius, angle, temp, lumens, exposure):
        self.name = name
        self.tag = tag
        self.radius = radius
        self.angle = angle
        self.temp = temp
        self.lumens = lumens
        self.exposure = exposure

    def create_light(self):
        class OBJECT_OT_add_light(Operator):
            bl_idname = "light.add_" + self.tag
            bl_label = "Add a " + self.name
            bl_description = "Creates a physically based light"
            bl_options = {'REGISTER', 'UNDO'}

            name = self.name
            lightType = 'SPOT'

            lumens: props.lumens(self, self.lumens)
            spotAngle: props.spotAngle(self, self.angle)
            colType: props.colType(self)
            temp: props.temp(self, self.temp)
            tint: props.tint(self)
            useNodes: props.useNodes(self)
            setExposure: props.setExposure(self)

            def draw(self, context):
                layout = self.layout
                layout.use_property_split = True
                layout.use_property_decorate = False

                layout.prop(self, "lumens")
                layout.prop(self, "spotAngle")
                layout.prop(self, "colType")
                if self.colType == "kelvin":
                    layout.prop(self, "temp")
                else:
                    layout.prop(self, "tint")
                layout.prop(self, "useNodes")
                layout.prop(self, "setExposure")

            def execute(self, context):
                bpy.ops.object.light_add(type='SPOT')
                bpy.context.active_object.name = self.name
                ob = bpy.context.active_object
                data = ob.data

                ob.rotation_euler[0] = 1.5708
                data.shadow_soft_size = self.radius
                data.spot_size = self.spotAngle / 57.2957795 
                data.use_custom_distance = True

                if self.useNodes:
                    if (bpy.data.node_groups.find("Spot Lumens Converter") == -1):
                        bpy.ops.wm.append(filename = "Spot Lumens Converter", directory = nodes_directory)

                    data.energy = 1
                    col = [self.tint[0], self.tint[1], self.tint[2], 1.0]
                    data.use_nodes = True
                    nodes = data.node_tree.nodes
                    lumensNode = nodes.new("ShaderNodeGroup")
                    lumensNode.node_tree = bpy.data.node_groups["Spot Lumens Converter"]
                    data.node_tree.links.new(lumensNode.outputs[0], nodes["Light Output"].inputs[0])
                    lumensNode.inputs[0].default_value = self.lumens
                    setup.nodeColor(self, lumensNode, self.colType, col, self.temp)

                else:
                    setup.nodeless(self, data, self.colType, self.tint, self.temp, self.lumens)

                if self.setExposure:
                    bpy.context.scene.view_settings.exposure = self.exposure

                return {'FINISHED'}
        return OBJECT_OT_add_light

class AreaLight:
    def __init__(self, name, tag, shape, size, temp, lumens, exposure):
        self.name = name
        self.tag = tag
        self.shape = shape
        self.size = size
        self.temp = temp
        self.lumens = lumens
        self.exposure = exposure

    def create_light(self):
        class OBJECT_OT_add_light(Operator):
            bl_idname = "light.add_" + self.tag
            bl_label = "Add a " + self.name
            bl_description = "Creates a physically based light"
            bl_options = {'REGISTER', 'UNDO'}

            name = self.name
            lightType = 'AREA'

            lumens: props.lumens(self, self.lumens)
            colType: props.colType(self)
            temp: props.temp(self, self.temp)
            tint: props.tint(self)
            useNodes: props.useNodes(self)
            setExposure: props.setExposure(self)

            def draw(self, context):
                layout = self.layout
                layout.use_property_split = True
                layout.use_property_decorate = False

                layout.prop(self, "lumens")
                layout.prop(self, "colType")
                if self.colType == "kelvin":
                    layout.prop(self, "temp")
                else:
                    layout.prop(self, "tint")
                layout.prop(self, "useNodes")
                layout.prop(self, "setExposure")

            def execute(self, context):
                bpy.ops.object.light_add(type='AREA')
                bpy.context.active_object.name = self.name
                ob = bpy.context.active_object
                data = ob.data

                data.shadow_soft_size = self.radius
                data.shape = self.shape
                data.size = self.size[0]
                data.size_y = self.size[1]
                data.use_custom_distance = True

                if self.useNodes:
                    if (bpy.data.node_groups.find("Area Lumens Converter") == -1):
                        bpy.ops.wm.append(filename = "Area Lumens Converter", directory = nodes_directory)

                    data.energy = 1
                    col = [self.tint[0], self.tint[1], self.tint[2], 1.0]
                    data.use_nodes = True
                    nodes = data.node_tree.nodes

                    lumensNode = nodes.new("ShaderNodeGroup")
                    lumensNode.node_tree = bpy.data.node_groups["Area Lumens Converter"]
                    data.node_tree.links.new(lumensNode.outputs[0], nodes["Light Output"].inputs[0])
                    lumensNode.inputs[0].default_value = self.lumens
                    setup.nodeColor(self, lumensNode, self.colType, col, self.temp)

                else:
                    setup.nodeless(self, data, self.colType, self.tint, self.temp, self.lumens)

                if self.setExposure:
                    bpy.context.scene.view_settings.exposure = self.exposure

                return {'FINISHED'}
        return OBJECT_OT_add_light

class SunLight:
    def __init__(self, name, tag, angle, temp, irradiance, exposure, rotation, skyStrength, skyTurbidity):
        self.name = name
        self.tag = tag
        self.angle = angle
        self.temp = temp
        self.irradiance = irradiance
        self.rotation = rotation
        self.exposure = exposure
        self.skyStrength = skyStrength
        self.skyTurbidity = skyTurbidity

    def create_light(self):
        class OBJECT_OT_add_light(Operator):
            bl_idname = "light.add_" + self.tag
            bl_label = "Add a " + self.name
            bl_description = "Creates a physically based light"
            bl_options = {'REGISTER', 'UNDO'}
            
            name = self.name
            lightType = 'SUN'

            irradiance: props.irradiance(self, self.irradiance)
            temp: props.temp(self, self.temp)
            useNodes: props.useNodes(self)
            useSky: props.useSky(self) 
            setExposure: props.setExposure(self)

            def draw(self, context):
                layout = self.layout
                layout.use_property_split = True
                layout.use_property_decorate = False

                layout.prop(self, "irradiance")
                layout.prop(self, "temp")
                layout.prop(self, "useNodes")
                layout.prop(self, "useSky")
                layout.prop(self, "setExposure")

            def execute(self, context):
                bpy.ops.object.light_add(type='SUN')
                bpy.context.active_object.name = self.name
                ob = bpy.context.active_object
                data = ob.data

                ob.rotation_euler = self.rotation
                if bpy.context.scene.camera != None:
                    z = (125/100) * bpy.context.scene.camera.location[2]
                    ob.location[2] = z

                if self.useNodes:
                    if (bpy.data.node_groups.find("Lumens Converter") == -1):
                        bpy.ops.wm.append(filename = "Lumens Converter", directory = nodes_directory)

                    data.energy = 1
                    data.use_nodes = True
                    nodes = data.node_tree.nodes

                    nodes["Emission"].inputs[1].default_value = self.strength
                    k = nodes.new("ShaderNodeBlackbody")
                    k.inputs[0].default_value = self.temp
                    data.node_tree.links.new(k.outputs[0], nodes["Emission"].inputs[0])
                else:
                    data.energy = self.strength
                    data.color = conversions.kelvin(self.temp)

                if self.useSky:
                    world = bpy.context.scene.world
                    nodes = world.node_tree.nodes
                    sky_texture = nodes.new("ShaderNodeTexSky")
                    sky_texture.turbidity = self.skyTurbidity
                    nodes["Background"].inputs[1].default_value = skyStrength
                    world.node_tree.links.new(sky_texture.outputs[0], nodes["Background"].inputs[0])
                    
                    dr = sky_texture.driver_add("sun_direction")
                    for i in range(3):
                        dr[i].driver.expression = "var"
                        var = dr[i].driver.variables.new()
                        var.targets[0].tag = ob
                        var.targets[0].data_path = "matrix_world[2]["+str(i)+"]"

                if self.setExposure:
                    bpy.context.scene.view_settings.exposure = self.exposure

                return {'FINISHED'}
        return OBJECT_OT_add_light

class IesLight:
    def __init__(self, name, tag, file, size, temp, strength, lumens, exposure):
        self.name = name
        self.tag = tag
        self.file = file
        self.size = size
        self.temp = temp
        self.strength = strength
        self.lumens = lumens
        self.exposure = exposure

    def SetProperties(self):
       pass

