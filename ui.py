import bpy
from bpy.utils import register_class, unregister_class

from . import light_presets

natural_operators = [ light.create_light() for light in light_presets.lights['natural'] ]
incandescent_operators = [ light.create_light() for light in light_presets.lights['incandescent'] ]
led_operators = [ light.create_light() for light in light_presets.lights['led'] ]
fluorescent_operators = [ light.create_light() for light in light_presets.lights['fluorescent'] ]

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

def draw_naturals(self, context):
    self.layout.menu(NaturalsMenu.bl_idname, icon='LIGHT')
def draw_incandescents(self, context):
    self.layout.menu(IncandescentsMenu.bl_idname, icon='LIGHT')
def draw_leds(self, context):
    self.layout.menu(LEDsMenu.bl_idname, icon='LIGHT')
def draw_fluorescents(self, context):
    self.layout.menu(FluorescentsMenu.bl_idname, icon='LIGHT')

classes = []
for op in natural_operators:
    classes.append(op)
for op in incandescent_operators:
    classes.append(op)
for op in led_operators:
    classes.append(op)
for op in fluorescent_operators:
    classes.append(op)

def register():
    bpy.types.VIEW3D_MT_light_add.append(draw_naturals)
    bpy.types.VIEW3D_MT_light_add.append(draw_incandescents)
    bpy.types.VIEW3D_MT_light_add.append(draw_leds)
    bpy.types.VIEW3D_MT_light_add.append(draw_fluorescents)

def unregister():
    bpy.types.VIEW3D_MT_mesh_add.remove(draw_naturals)
    bpy.types.VIEW3D_MT_mesh_add.remove(draw_incandescents)
    bpy.types.VIEW3D_MT_light_add.remove(draw_leds)
    bpy.types.VIEW3D_MT_light_add.remove(draw_fluorescents)
