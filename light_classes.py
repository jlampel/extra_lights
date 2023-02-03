'''
Copyright (C) 2020-2023 Orange Turbine
https://orangeturbine.com
orangeturbine@cgcookie.com

This file is part of Extra Lights, created by Jonathan Lampel. 

All code distributed with this add-on is open source as described below. 

Extra Lights is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <https://www.gnu.org/licenses/>.
'''

import bpy
import os
from pathlib import Path
from bpy.types import Operator, PropertyGroup
from bpy.props import IntProperty, BoolProperty, FloatVectorProperty

from . import conversions

nodes_directory = bpy.path.native_pathsep(os.path.dirname(os.path.abspath(__file__)) + "/real_lights.blend\\NodeTree\\")
texts_directory = bpy.path.native_pathsep(os.path.dirname(os.path.abspath(__file__)) + "/real_lights.blend\\Text\\")

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
    def iesNodes(self):
        return bpy.props.BoolProperty(
            name = "Use Nodes (Cycles only)",
            default = True,
            description = "IES Textures only work with Cycles at the moment. Turning this off will just make it a regular light",
        )   
    def irradiance(self, x):
        return bpy.props.FloatProperty(
            name = "Irradiance",
            default = x,
            min = 0.0001,
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
            description = "Set the scene exposure to approximately match the added light. Exposusure heavily depends on context, so it's recommended that you adjust it further before your final render"
        )
    def spotAngle(self, x):
        return bpy.props.IntProperty(
            name = "Spot Angle",
            default = x,
            min = 1,
            max = 180,
            description = "Setting the spot angle here will keep the total amount of light generated the same regardless of the angle.",
        )
    def spreadAngle(self):
        return bpy.props.IntProperty(
            name = "Spread Angle",
            default = 180,
            min = 5,
            max = 180,
            description = "Lower values direct more light streight forward",
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
            description = "Sets the RGB color of the light",
        )
    def useNodes(self):
        return bpy.props.BoolProperty(
            name = "Use Nodes (Cycles only)",
            default = False,
            description = "Create light with nodes so that lumens and color temperature can be changed at any time. Currently only works with Cycles.",
        )    
    def useSky(self):
        return bpy.props.BoolProperty(
            name = "Create Linked Sky",
            default = False,
            description = "Create a new World with a Sky texture linked to the rotation of the sun lamp.",
        )

class setup:
    def nodeColor(self, lumensNode, colType, col, temp):
        if colType == "rgb":
            lumensNode.inputs[1].default_value = 6000
            lumensNode.inputs[2].default_value = col
        else:
            lumensNode.inputs[1].default_value = temp
    def nodeless(self, data, colType, tint, temp, lumens):
        if colType == "rgb":
            data.color = tint
        else: 
            data.color = conversions.kelvin(temp)
        data.energy = conversions.lumens(lumens, data.color)

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

            lightType = 'POINT'
            name = self.name
            lightName = name
            radius = self.radius
            exposure = self.exposure
            order = self.lumens

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
                bpy.context.active_object.name = self.lightName
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
                    lumensNode.location = (0,150)
                    lumensNode.node_tree = bpy.data.node_groups["Lumens Converter"]
                    data.node_tree.links.new(lumensNode.outputs[0], nodes["Light Output"].inputs[0])
                    lumensNode.inputs[0].default_value = self.lumens
                    setup.nodeColor(self, lumensNode, self.colType, col, self.temp)

                else:
                    setup.nodeless(self, data, self.colType, self.tint, self.temp, self.lumens)

                if self.setExposure:
                    bpy.context.scene.view_settings.exposure = self.exposure
                    if self.exposure > 0:
                        bpy.context.scene.cycles.light_sampling_threshold = 0.01 / (self.exposure * 10)


                ob.select_set(True)
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

            radius = self.radius
            exposure = self.exposure
            name = self.name
            lightName = name
            lightType = 'SPOT'
            order = self.lumens

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
                bpy.context.active_object.name = self.lightName
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
                    lumensNode.location = (0,150)
                    lumensNode.node_tree = bpy.data.node_groups["Spot Lumens Converter"]
                    data.node_tree.links.new(lumensNode.outputs[0], nodes["Light Output"].inputs[0])
                    lumensNode.inputs[0].default_value = self.lumens
                    setup.nodeColor(self, lumensNode, self.colType, col, self.temp)

                    dr = lumensNode.inputs[3].driver_add("default_value")
                    dr.driver.expression = "var * 57.2957795"
                    var = dr.driver.variables.new()
                    var.targets[0].id_type = 'LIGHT'
                    var.targets[0].id = data
                    var.targets[0].data_path = "spot_size"

                else:
                    setup.nodeless(self, data, self.colType, self.tint, self.temp, self.lumens)
                    data.energy = (360 / self.spotAngle) * conversions.lumens(self.lumens, data.color) 

                if self.setExposure:
                    bpy.context.scene.view_settings.exposure = self.exposure
                    if self.exposure > 0:
                        bpy.context.scene.cycles.light_sampling_threshold = 0.01 / (self.exposure * 10)

                ob.select_set(True)
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

            shape = self.shape
            exposure = self.exposure
            size = self.size
            name = self.name
            lightName = name
            lightType = 'AREA'
            order = self.lumens

            lumens: props.lumens(self, self.lumens)
            colType: props.colType(self)
            temp: props.temp(self, self.temp)
            tint: props.tint(self)
            useNodes: props.useNodes(self)
            setExposure: props.setExposure(self)
            spreadAngle: props.spreadAngle(self)

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
                spreadAngleRow = layout.row(align=True)
                spreadAngleRow.enabled = self.useNodes
                spreadAngleRow.prop(self, "spreadAngle")
                layout.prop(self, "setExposure")

            def execute(self, context):
                bpy.ops.object.light_add(type='AREA')
                bpy.context.active_object.name = self.lightName
                ob = bpy.context.active_object
                data = ob.data

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
                    lumensNode.location = (0,150)
                    lumensNode.node_tree = bpy.data.node_groups["Area Lumens Converter"]
                    data.node_tree.links.new(lumensNode.outputs[0], nodes["Light Output"].inputs[0])
                    lumensNode.inputs[0].default_value = self.lumens
                    lumensNode.inputs[3].default_value = self.spreadAngle
                    setup.nodeColor(self, lumensNode, self.colType, col, self.temp)

                else:
                    setup.nodeless(self, data, self.colType, self.tint, self.temp, self.lumens)

                if self.setExposure:
                    bpy.context.scene.view_settings.exposure = self.exposure
                    if self.exposure > 0:
                        bpy.context.scene.cycles.light_sampling_threshold = 0.01 / (self.exposure * 10)

                ob.select_set(True)
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
            
            rotation = self.rotation
            skyTurbidity = self.skyTurbidity
            skyStrength = self.skyStrength
            name = self.name
            lightName = name
            exposure = self.exposure
            angle = self.angle
            lightType = 'SUN'
            order = self.irradiance * 1000

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
                bpy.context.active_object.name = self.lightName
                ob = bpy.context.active_object
                data = ob.data

                data.angle = self.angle / 57.2957795 
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

                    nodes["Emission"].inputs[1].default_value = self.irradiance
                    k = nodes.new("ShaderNodeBlackbody")
                    k.inputs[0].default_value = self.temp
                    data.node_tree.links.new(k.outputs[0], nodes["Emission"].inputs[0])
                else:
                    data.energy = self.irradiance
                    data.color = conversions.kelvin(self.temp)

                if self.useSky:
                    if bpy.context.scene.world == None:
                        bpy.context.scene.world = bpy.data.worlds.new(name=self.name + " Sky")
                    world = bpy.context.scene.world
                    world.use_nodes = True
                    nodes = world.node_tree.nodes
                    if "World Output" not in nodes.keys():
                        nodes.new("ShaderNodeOutputWorld")
                    if "Background" not in nodes.keys():
                        background = nodes.new("ShaderNodeBackground")
                        world.node_tree.links.new(background.outputs[0], nodes["World Output"].inputs[0])
                    sky_texture = nodes.new("ShaderNodeTexSky")
                    sky_texture.sky_type = "HOSEK_WILKIE"
                    sky_texture.turbidity = self.skyTurbidity
                    nodes["Background"].inputs[1].default_value = self.skyStrength
                    world.node_tree.links.new(sky_texture.outputs[0], nodes["Background"].inputs[0])
                    
                    dr = sky_texture.driver_add("sun_direction")
                    for i in range(3):
                        dr[i].driver.expression = "var"
                        var = dr[i].driver.variables.new()
                        var.targets[0].id = ob
                        var.targets[0].data_path = "matrix_world[2]["+str(i)+"]"

                if self.setExposure:
                    bpy.context.scene.view_settings.exposure = self.exposure
                    if self.exposure > 0:
                        bpy.context.scene.cycles.light_sampling_threshold = 0.01 / (self.exposure * 10)

                ob.select_set(True)
                return {'FINISHED'}
        return OBJECT_OT_add_light

class IesLight:
    def __init__(self, name, tag, spotAngle, radius, temp, strength, lumens, exposure):
        self.name = name
        self.tag = tag
        self.spotAngle = spotAngle
        self.radius = radius
        self.temp = temp
        self.strength = strength
        self.lumens = lumens
        self.exposure = exposure

    def create_light(self):
        class OBJECT_OT_add_light(Operator):
            bl_idname = "light.add_" + self.tag
            bl_label = "Add a " + self.name
            bl_description = "Creates a physically based light"
            bl_options = {'REGISTER', 'UNDO'}

            name = self.name
            lightName = name
            spotAngle = self.spotAngle
            radius = self.radius
            strength = self.strength
            exposure = self.exposure
            if spotAngle:
                lightType = 'SPOT'
            else:
                lightType = 'POINT'
            order = self.lumens

            lumens: props.lumens(self, self.lumens)
            spotAngle: props.spotAngle(self, self.spotAngle)
            colType: props.colType(self)
            temp: props.temp(self, self.temp)
            tint: props.tint(self)
            useNodes: props.iesNodes(self)
            setExposure: props.setExposure(self)

            def draw(self, context):
                layout = self.layout
                layout.use_property_split = True
                layout.use_property_decorate = False

                layout.prop(self, "lumens")
                if self.lightType == 'SPOT':
                    layout.prop(self, "spotAngle")
                layout.prop(self, "colType")
                if self.colType == "kelvin":
                    layout.prop(self, "temp")
                else:
                    layout.prop(self, "tint")
                layout.prop(self, "useNodes")
                layout.prop(self, "setExposure")

            def execute(self, context):
                bpy.ops.object.light_add(type=self.lightType)
                bpy.context.active_object.name = self.lightName
                ob = bpy.context.active_object
                data = ob.data

                data.shadow_soft_size = self.radius
                if self.spotAngle:
                    data.spot_size = self.spotAngle / 57.2957795
                data.use_custom_distance = True

                if self.useNodes:
                    if bpy.data.node_groups.find("IES Lumens Converter") == -1:
                        bpy.ops.wm.append(filename = "IES Lumens Converter", directory = nodes_directory)
                    
                    if bpy.data.texts.find(self.lightName) == -1:
                        bpy.ops.wm.append(filename = self.lightName, directory = texts_directory)
                    
                    data.energy = 1
                    col = [self.tint[0], self.tint[1], self.tint[2], 1.0]
                    data.use_nodes = True
                    nodes = data.node_tree.nodes
                    lumensNode = nodes.new("ShaderNodeGroup")
                    lumensNode.location = (0,150)
                    lumensNode.node_tree = bpy.data.node_groups["IES Lumens Converter"]
                    data.node_tree.links.new(lumensNode.outputs[0], nodes["Light Output"].inputs[0])
                    lumensNode.inputs[0].default_value = self.lumens
                    setup.nodeColor(self, lumensNode, self.colType, col, self.temp)
                    
                    iesNode = nodes.new('ShaderNodeTexIES')
                    iesNode.location = (-200,150)
                    iesNode.ies = bpy.data.texts[self.lightName]
                    iesNode.inputs[1].default_value = self.strength
                    data.node_tree.links.new(iesNode.outputs[0], lumensNode.inputs[3])
                    
                else:
                    setup.nodeless(self, data, self.colType, self.tint, self.temp, self.lumens)

                if self.setExposure:
                    bpy.context.scene.view_settings.exposure = self.exposure
                    if self.exposure > 0:
                        bpy.context.scene.cycles.light_sampling_threshold = 0.01 / (self.exposure * 10)

                ob.select_set(True)
                return {'FINISHED'}
        return OBJECT_OT_add_light