from graphics import Graphics
import glm
import moderngl
import math
from raytracer import RayTracer

class Scene:
    def __init__(self, ctx, camera, shader_program=None):
        self.ctx = ctx
        self.objects = []
        self.graphics = {}
        self.camera = camera
        self.shader = shader_program  # <- guardo el shader si me lo pasan
        self.time = 0.0
        self.view = None         
        self.projection = None 

    def add_object(self, model, material):
        self.objects.append(model)
        self.graphics[model.name] = Graphics(self.ctx, model, material)

    def update(self, dt):
        # Animación sencilla: girar todos los objetos en Y (60° por segundo)
        for obj in self.objects:
            if obj.name.startswith("Cube"):  # Solo cubos rotan
                obj.rotation.y += 60.0 * dt
    
    def start(self):
        print("Start!")

    def render(self):
        self.time += 0.01
        for obj in self.objects:
            if(obj.name != "Sprite"):
                pass
                # obj.rotation += glm.vec3(0.8, 0.6, 0.4)
                # obj.position.x += math.sin(self.time) * 0.01
            model = obj.get_model_matrix()
            mvp = self.projection * self.view * model
            self.graphics[obj.name].render({'Mvp': mvp})
    
    def on_mouse_click(self, u, v):
        ray = self.camera.raycast(u, v)

        for obj in self.objects:
            if obj.check_hit(ray.origin, ray.direction):
                print(f"¡Golpeaste al objeto {obj.name}!")

    def on_resize(self, width, height):
        self.ctx.viewport = (0, 0, width, height)
        # actualizar aspect en la cámara
        self.camera.aspect = width / float(max(1, height))

class RayScene(Scene):
    def __init__(self, ctx, camera, width, height):
        super().__init__(ctx, camera)
        self.raytracer = RayTracer(camera, width, height)
    
    def start(self):
        self.raytracer.render_frame(self.objects)
        if "Sprite" in self.graphics:
            self.graphics["Sprite"].update_texture("u_texture", self.raytracer.get_texture())

    def render(self):
        super().render()
    
    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.raytracer = RayTracer(self.camera, width, height)
        self.start()