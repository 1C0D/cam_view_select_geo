import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

def main(context):
    # Get context elements: scene, camera and mesh
    scene = context.scene
    cam = context.scene.camera
    objs = context.selected_objects
    cao=context.active_object

    limit = 0.1

    # In world coordinates, get a bvh tree and vertices
    bpy.ops.object.mode_set(mode='OBJECT')
    for obj in objs:   
        if obj.type=='MESH':
            me = obj.data
            depsgraph = context.evaluated_depsgraph_get()
            obj_eval = obj.evaluated_get(depsgraph)
            for p in me.polygons:
                p.select = False
            for e in me.edges:
                e.select = False         
               
            for v in me.vertices:
                mw = obj_eval.matrix_world
                
                # Get the 2D projection of the vertex
                co2D = world_to_camera_view( scene, cam, mw @ v.co )

                cubeMesh=bpy.ops.mesh.primitive_cube_add(location=(mw @ v.co))
                bpy.ops.transform.resize(value=(0.01, 0.01, 0.01))
                cubeObject=context.object

                # If inside the camera view
                if 0.0 <= co2D.x <= 1.0 and 0.0 <= co2D.y <= 1.0 and co2D.z >0: 
                    # Try a ray cast, in order to test the vertex visibility from the camera
                    
                    location= scene.ray_cast(context.view_layer, cam.location, (mw @ v.co - cam.location).normalized() )
                    # If the ray hits something and if this hit is close to the vertex, we assume this is the vertex
                    print(location[0],location[1])
                    if location[0] and (mw @ v.co - location[1]).length < limit:
                        v.select = True
                        
                bpy.data.objects.remove(cubeObject,do_unlink= True)
    context.view_layer.objects.active =cao
    cao.select_set(True)


class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(SimpleOperator)


def unregister():
    bpy.utils.unregister_class(SimpleOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.simple_operator()
