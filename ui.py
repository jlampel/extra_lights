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


import bpy, os
from pathlib import Path
from bpy.utils import register_class, unregister_class

from . import light_presets

natural_operators = [ light.create_light() for light in light_presets.lights['natural'] ]
incandescent_operators = [ light.create_light() for light in light_presets.lights['incandescent'] ]
led_operators = [ light.create_light() for light in light_presets.lights['led'] ]
fluorescent_operators = [ light.create_light() for light in light_presets.lights['fluorescent'] ]

try:
    from . import light_presets_bonus
    bonus = True
except:
    bonus = False

def sortOrder(op):
    return op.order

if bonus:
    for light in light_presets_bonus.lights['natural']:
        op = light.create_light()
        natural_operators.append(op)
    natural_operators.sort(key=sortOrder)
    for light in light_presets_bonus.lights['fluorescent']:
        op = light.create_light()
        fluorescent_operators.append(op)
    fluorescent_operators.sort(key=sortOrder)
    for light in light_presets_bonus.lights['incandescent']:
        op = light.create_light()
        incandescent_operators.append(op)
    incandescent_operators.sort(key=sortOrder)
    for light in light_presets_bonus.lights['led']:
        op = light.create_light()
        led_operators.append(op)
    led_operators.sort(key=sortOrder)   

class NaturalsMenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_naturals_menu"
    bl_label = "Natural"
    def draw(self, context):
        for op in natural_operators:
            self.layout.operator(
                op.bl_idname,
                text=op.name,
                icon='LIGHT_'+op.lightType
            )
class IncandescentsMenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_incandescents_menu"
    bl_label = "Incandescent"
    def draw(self, context):
        for op in incandescent_operators:
            self.layout.operator(
                op.bl_idname,
                text=op.name,
                icon='LIGHT_'+op.lightType
            )
class LEDsMenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_leds_menu"
    bl_label = "LED"
    def draw(self, context):
        for op in led_operators:
            self.layout.operator(
                op.bl_idname,
                text=op.name,
                icon='LIGHT_'+op.lightType
            )
class FluorescentsMenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_fluorescents_menu"
    bl_label = "Fluorescent"
    def draw(self, context):
        for op in fluorescent_operators:
            self.layout.operator(
                op.bl_idname,
                text=op.name,
                icon='LIGHT_'+op.lightType
            )

def draw_naturals(self, context):
    self.layout.menu(NaturalsMenu.bl_idname, icon='LIGHT')
def draw_incandescents(self, context):
    self.layout.menu(IncandescentsMenu.bl_idname, icon='LIGHT')
def draw_leds(self, context):
    self.layout.menu(LEDsMenu.bl_idname, icon='LIGHT')
def draw_fluorescents(self, context):
    self.layout.menu(FluorescentsMenu.bl_idname, icon='LIGHT')

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
    bpy.types.VIEW3D_MT_light_add.append(draw_naturals)
    bpy.types.VIEW3D_MT_light_add.append(draw_incandescents)
    bpy.types.VIEW3D_MT_light_add.append(draw_leds)
    bpy.types.VIEW3D_MT_light_add.append(draw_fluorescents)

def unregister():
    for cls in classes:
        unregister_class(cls)
    bpy.types.VIEW3D_MT_mesh_add.remove(draw_naturals)
    bpy.types.VIEW3D_MT_mesh_add.remove(draw_incandescents)
    bpy.types.VIEW3D_MT_light_add.remove(draw_leds)
    bpy.types.VIEW3D_MT_light_add.remove(draw_fluorescents)
