import bpy
import bmesh
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

scene = bpy.context.scene
cam = bpy.context.scene.camera
objs = bpy.context.selected_objects

mod=None
if(bpy.context.object.mode!='EDIT'):
    mod=bpy.context.object.mode
    bpy.ops.object.mode_set(mode = 'EDIT')

for obj in objs:   
    if obj.type=='MESH':    
        
            mw = obj.matrix_world
            me = obj.data
            bm = bmesh.from_edit_mesh(me)            
            for v in bm.verts:
                co_ndc = world_to_camera_view(scene, cam, mw @ v.co) 
                if (0.0 < co_ndc.x < 1.0 and 0.0 < co_ndc.y < 1.0):
                    v.select = True
                else:
                    v.select = False
            bmesh.update_edit_mesh(me, False, False)
if mod:   
    bpy.ops.object.mode_set(mode=(mod))            


