import bpy
from bpy.utils import register_class, unregister_class
from . import import_presets, light_classes

class ExtraLightsMenu:
    def __init__(self, category):
        self.category = category

    def create_category(self):
        class EXTRALIGHTS_MT_menu(bpy.types.Menu):
            # Why am I not useing self.category? 
            bl_idname = 'OBJECT_MT_' + category + '_menu'
            bl_label = category

            def draw(self, context):
                self.layout.operator(
                    self.bl_idname,
                    text = self.bl_label,
                    icon = 'LIGHT',
                )

            def draw_category(self, context):
                self.layout.menu(EXTRALIGHTS_MT_menu.bl_idname, icon='LIGHT')

        return EXTRALIGHTS_MT_menu

    #when do I use the draw method
        
light_presets = import_presets.load()
filenames = light_presets.keys()

category_classes = []
cateogry_menus = []
light_operators = []

for f in filenames:
    categories = list( light_presets[f].keys() )
    for category in categories:
        if category not in category_classes:
            c = ExtraLightsMenu.create_category(category)
            category_classes.append(c)
            cateogry_menus.append(c.draw_category)
        presets = list(light_presets[f][category].keys() )
        for preset in presets:
            light_operators.append( light_classes.Light.create_light( light_presets[f][category][preset] ) )

classes = category_classes + light_operators

def register():
    for cls in classes:
        register_class(cls)
    for menu in category_menus:
        bpy.types.VIEW3D_MT_light_add.append(menu)

def unregister():
    for cls in classes:
        unregister_class(cls)
    for menu in category_menus:
        bpy.types.VIEW3D_MT_light_add.remove(menu)
