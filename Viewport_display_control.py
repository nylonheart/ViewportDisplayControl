bl_info = {
    "name": "Viewport display control",
    "author": "Yonemaru",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "location": "3D View > Tool panel",
    "description": "This script toggles visibility of modifiers, armatures, and mesh wireframes, and switches between pose and rest modes in Blender's viewport.",
    "category": "3D View" # カテゴリー
}

import bpy

class HID_PT_UI(bpy.types.Panel):
    bl_label = "ViewportDisplayControl"
    bl_category = "Nylonheart"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    bpy.types.Scene.HID_OnOffModName = bpy.props.StringProperty(name='Partial')
    
    def draw(self,context):
        
        layout = self.layout
        row = layout.row(align=False)
        box = row.box()
        box.label(text =  'Modifier switch')
        box.prop(context.scene, "HID_OnOffModName")
        brow = box.row(align=True)
        brow.alignment = 'EXPAND'
        brow.operator("hid.subsonoff", text='ON', icon='MOD_SUBSURF').subs = True
        brow.operator("hid.subsonoff", text='OFF',icon='MESH_ICOSPHERE').subs = False
        
        row = layout.row(align=False)
        box = row.box()
        box.label(text =  'Armature switch')
        brow = box.row(align=True)
        brow.operator("hid.poseonoff", text='Pose', icon='ARMATURE_DATA').subs = 'POSE'
        brow.operator("hid.poseonoff", text='Rest', icon='POSE_HLT').subs = 'REST'
        crow = box.row(align=True)
        crow.operator("hid.armaturevisonoff", text='Show', icon='HIDE_OFF').subs = False
        crow.operator("hid.armaturevisonoff", text='Hide', icon='HIDE_ON').subs = True
        
        row = layout.row(align=False)
        box = row.box()
        box.label(text =  'Wire switch')
        brow = box.row(align=True)
        brow.operator("hid.wireonoff", text='+WIRE', icon='SHADING_WIRE').subs = True
        brow.operator("hid.wireonoff", text='Base', icon='SHADING_SOLID').subs = False
       
        
class HID_OT_SubSurf(bpy.types.Operator):
    bl_idname = "hid.subsonoff"
    bl_label = "Button"
    subs : bpy.props.BoolProperty()

    def execute(self, context):
        modname = bpy.context.scene["HID_OnOffModName"]
        print(modname)
        if bpy.context.selected_objects == []:
            for obj in bpy.data.objects:
                for mod in obj.modifiers:
                    if modname in mod.name:
                        mod.show_viewport = self.subs
        else:
            for obj in bpy.context.selected_objects:
                for mod in obj.modifiers:
                    if modname in mod.name:
                        mod.show_viewport = self.subs
        return{'FINISHED'}

class HID_OT_ArmaturePose(bpy.types.Operator):
    bl_idname = "hid.poseonoff"
    bl_label = "Button"
    subs : bpy.props.StringProperty()
    
    def execute(self, context):
        if bpy.context.selected_objects == []:
            for dat in bpy.data.objects:
                try:
                    dat.data.pose_position = self.subs
                except:
                    pass
        else:
            for dat in bpy.context.selected_objects:
                try:
                    dat.data.pose_position = self.subs
                except:
                    pass

        return{'FINISHED'}
    
class HID_OT_ArmatureVisibility(bpy.types.Operator):
    bl_idname = "hid.armaturevisonoff"
    bl_label = "Button"
    subs : bpy.props.BoolProperty()
    
    def execute(self, context):
        for obj in bpy.context.scene.objects:
            # オブジェクトがArmatureタイプの場合
            if obj.type == 'ARMATURE':
                # Viewportでの可視性を非表示に設定
                obj.hide_viewport = self.subs
                # 選択可能性を非表示（選択不可）に設定
                obj.hide_select = self.subs

        return{'FINISHED'}

class HID_OT_Wire(bpy.types.Operator):
    bl_idname = "hid.wireonoff"
    bl_label = "Button"
    subs : bpy.props.BoolProperty()
    
    def execute(self, context):
        if self.subs:
            if bpy.context.selected_objects == []:
                for dat in bpy.data.objects:
                    try:
                        dat.show_wire = not dat.show_wire
                    except:
                        pass
            else:
                for dat in bpy.context.selected_objects:
                    try:
                        dat.show_wire = not dat.show_wire
                    except:
                        pass
        else:
            if bpy.context.selected_objects == []:
                for dat in bpy.data.objects:
                    try:
                        if dat.display_type == 'WIRE':
                            dat.display_type = 'TEXTURED'
                        else:
                            dat.display_type = 'WIRE'
                    except:
                        pass
            else:
                for dat in bpy.context.selected_objects:
                    try:
                        if dat.display_type == 'WIRE':
                            dat.display_type = 'TEXTURED'
                        else:
                            dat.display_type = 'WIRE'
                    except:
                        pass
            
        return{'FINISHED'}

classes = (
    HID_PT_UI,
    HID_OT_SubSurf,
    HID_OT_ArmaturePose,
    HID_OT_ArmatureVisibility,
    HID_OT_Wire
)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()