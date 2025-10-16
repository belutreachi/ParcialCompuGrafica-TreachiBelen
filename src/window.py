import moderngl
import pyglet

class Window(pyglet.window.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)
        self.ctx = moderngl.create_context()
        self.scene = None

    def set_scene(self, scene): # asigna la escena a la ventana y llama al metodo start de la escena
        self.scene = scene
        scene.start()
    
    def on_mouse_press(self, x, y, button, modifiers): # se ejecuta al hacer click con el mouse
        if self.scene is None:
            return
        
        # Convertir posición del mouse a u,v [0,1]
        u = x / self.width
        v = y / self.height

        self.scene.on_mouse_click(u, v)

    def on_draw(self):  # se ejecuta por cada frame, limpia y renderiza la escena en cada frame
        self.clear()
        self.ctx.clear()
        self.ctx.enable(moderngl.DEPTH_TEST)
        if self.scene:
            self.scene.render()

    def on_resize(self, width, height): # escala el contexto (se ejecuta) al escalar la ventana
        if self.scene:
            self.scene.on_resize(width, height)

    def run(self):  # ejecuta el loop principal de pyglet
        pyglet.app.run()
