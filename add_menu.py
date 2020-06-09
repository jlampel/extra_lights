import bpy
from bpy.utils import register_class, unregister_class
from . import import_presets, light_creation

light_presets = import_presets.load()

category_classes = []
category_menus = []
light_operators = []
light_menus = []

for preset_file in light_presets.keys():
    categories = list( light_presets[preset_file].keys() )
    for category in categories:
        if category not in category_classes:
            
            ops = []
            for preset in list(light_presets[preset_file][category].keys()):
                i = light_creation.create_light_operator(preset)
                ops.append( light_creation.create_light_operator(preset) )
                light_operators.append(i)

            c = light_creation.create_category_menu(category, ops)
            category_classes.append(c)
            category_menus.append(c.draw_category)


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
