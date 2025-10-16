from texture import Texture
from shader_program import ComputeShaderProgram
from bvh import BVH
import glm
import math

class RayTracer:
    def __init__(self, camera, width, height):
        self.camera = camera
        self.width = width
        self.height = height
        self.framebuffer = Texture(width=width, height=height, channels_amount=3) # crea una texture vacía

        self.camera.set_sky_colors(top=(16, 150, 222), bottom=(181, 224, 247)) # asigna un gradiente de cielo por defecto

    def trace_ray(self, ray, objects): # método para trazar los rayos
        for obj in objects: # recorre los objetos comprobando si el rayo los intersecta
            if obj.check_hit(ray.origin, ray.direction):
                return (255, 0, 0)  # si intersecta, devuelve rojo
        height = ray.direction.y # altura del rayo para el gradiente
        return self.camera.get_sky_gradient(height) # si no intersecta, devuelve el color del cielo
    
    def render_frame(self, objects): # se ejecuta para cada pixel de la textura
        for y in range(self.height): # recorre la imagen en sus dos dimensiones (horizontal y vertical)
            for x in range(self.width):
                u = x / (self.width - 1)
                v = y / (self.height - 1)
                ray = self.camera.raycast(u, v) # trza el rayo desde la cámara
                color = self.trace_ray(ray, objects) # pinta la textura asignando el color en la posición (x,y)
                self.framebuffer.set_pixel(x, y, color)
    
    def get_texture(self): # permite leer la información generada en el framebuffer y utilizarla en el renderizado del quad
        return self.framebuffer.image_data
    
class RayTracerGPU:
    def __init__(self, ctx, camera, width, height, output_graphics):
        self.ctx = ctx
        self.width, self.height = width, height
        self.camera = camera
        self.width = width
        self.height = height

        from pathlib import Path
        shader_dir_1 = Path(__file__).resolve().parents[1]/ "shaders"
        raytrace_comp_path = str(shader_dir_1 / "raytracing.comp")

        self.compute_shader = ComputeShaderProgram(self.ctx, raytrace_comp_path)
        self.output_graphics = output_graphics

        self.texture_unit = 0
        self.output_texture = Texture("u_texture", self.width, self.height, 4, None, (255, 255, 255, 255))
        self.output_graphics.update_texture("u_texture", self.output_texture.image_data)
        self.output_graphics.bind_to_image("u_texture", self.texture_unit, read=False, write=True)

        self.compute_shader.set_uniform('cameraPosition', self.camera.position)
        self.compute_shader.set_uniform('inverseViewMatrix', self.camera.get_inverse_view_matrix())
        self.compute_shader.set_uniform('fieldOfView', self.camera.fov)

    def resize(self, width, height): # recalcula el tamaño de la textura de salida cuando se redimensiona la ventana
        self.width, self.height = width, height
        self.output_texture = Texture("u_texture", width, height, 4, None, (255, 255, 255, 255))
        self.output_graphics.update_texture("u_texture", self.output_texture.image_data)
    
    def matrix_to_ssbo(self, matrix, binding = 0):
        buffer = self.ctx.buffer(matrix.tobytes())
        buffer.bind_to_storage_buffer(binding=binding) # tiene que ser igual al compute shader
    
    def primitives_to_ssbo(self, primitives, binding = 3):
        self.bvh_nodes = BVH(primitives)
        self.bvh_ssbo = self.bvh_nodes.pack_to_bytes()
        buf_bvh = self.ctx.buffer(self.bvh_ssbo)
        buf_bvh.bind_to_storage_buffer(binding=binding)
    
    def run(self):
        groups_x = (self.width + 15) // 16
        groups_y = (self.height + 15) // 16

        self.compute_shader.run(groups_x=groups_x, groups_y=groups_y, groups_z=1)
        self.ctx.clear(0.0, 0.0, 0.0, 1.0)
        self.output_graphics.render({"u_texture": self.texture_unit})
    
    def render(self):
        self.time += 0.01
        for obj in self.objects:
            if obj.animated:
                obj.rotation += glm.vec3(0.8, 0.6, 0.4)
                obj.position.x += math.sin(self.time) * 0.01
        
        if(self.raytracer is not None):
            self._update_matrix()
            self._matrix_to_ssbo()
            self.raytracer.run()