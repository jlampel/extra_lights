import bpy, os, json
from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class


path = os.path.dirname(os.path.abspath(__file__))

class EXTRALIGHTS_OT_export_presets(Operator):
    bl_label = 'Export Extra Lights Presets'
    bl_idname = 'extralights.export_presets'
    bl_description = "Export light data for the chosen collection for the Extra Lights addon to read"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        # Check if the collection exists 
        if 'Light Presets' in bpy.data.collections:

            # Create file to store object info 
            filename = bpy.path.basename(bpy.context.blend_data.filepath)[:-6]
            file = open(path + '/presets/' + filename + '_data.py', 'w')

            light_presets = { filename : {} }

            # Create dictionary of objects 
            presets_collection = bpy.data.collections['Light Presets']

            for category in presets_collection.children:
                light_presets[filename][category.name] = {}

                def save_objects(object):
                    light_presets[filename][category.name][object.name] = {
                        # save attributes here
                    }

                for object in category.objects:
                    save_objects(object)
                for c in category.children:
                    object = bpy.data.objects[c.name]
                    save_objects(object)

            self.report({'INFO'}, 'Export complete!')
            file.write(json.dumps(light_presets))

        else:
            bpy.ops.extralights.export_error('INVOKE_DEFAULT')
        return {'FINISHED'}  
    
class EXTRALIGHTS_PT_Panel(bpy.types.Panel):
    bl_idname = 'EXTRALIGHTS_PT_Panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lighting'
    bl_label = 'Extra Lights'
    
    def draw(self, context):
        self.layout.operator('extralights.export_presets', text='Export Light Presets')

class EXTRALIGHTS_OT_export_error(bpy.types.Operator):
    bl_idname = 'extralights.export_error'
    bl_label = 'Export Error'

    def execute(self, context):
        self.report({'INFO'}, "Nothing was exported")
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.label(text=' ')
        col.label(text='Please create a collection called Light Presets.')
        col.label(text=' ')
        col.label(text='Each collection inside of it will be a category, ')
        col.label(text='and each light inside the categories ')
        col.label(text='will be exported as a preset.')        
        col.label(text=' ')
        col.label(text='See the documentation for more detailed instructions')
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class EXTRALIGHTS_OT_mesh_material_error(bpy.types.Operator):
    bl_idname = 'extralights.mesh_material_error'
    bl_label = 'Export Error'

    def execute(self, context):
        self.report({'INFO'}, "Export Cancelled")
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.label(text='Please use a Lumens Converter node ')
        col.label(text='in the first material slot ')
        col.label(text='when exporting a mesh light')
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

classes = (
    EXTRALIGHTS_OT_export_presets,
    EXTRALIGHTS_PT_Panel,
    EXTRALIGHTS_OT_export_error,
    EXTRALIGHTS_OT_mesh_material_error,
)
    
def register():
    for cls in classes:
        register_class(cls)

def unregister():
    for cls in classes:
        unregister_class(cls)
