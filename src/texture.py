import numpy as np

class ImageData: # contenedor de los pixeles de la imagen
    def __init__(self, height, width, channels, color = (0, 0, 0)): # es una matriz con tres dimensiones
        self.data = np.full((height, width, channels), color, dtype=np.uint8)

    def set_pixel(self, x, y, color): # nos permite pintar pixel por pixel
        self.data[y,x] = color

    def tobytes(self): # convertimos la matriz a bytes para enviarla a la GPU
        return self.data.tobytes() 

class Texture: # encargada de administrar los datos de la textura en CPU y nos da metodos para manipularlos
    def __init__(self, name = "u_texture", width = 1, height = 1, channels_amount = 3, image_data: ImageData = None, color = (0,0,0), repeat_x = False, repeat_y = False, build_mipmaps = False):
        self.name = name
        self.size = (width, height)
        self.channels_amount = channels_amount
        self.repeat_x = repeat_x
        self.repeat_y = repeat_y
        self.build_mipmaps = build_mipmaps

        self.width = width
        self.height = height

        if image_data is not None: 
            self._image_data = image_data # si se le pasa una imagen, la usa
        else:
            self._image_data = ImageData(height, width, channels_amount, color) # si no, crea una nueva imagen con el color por defecto
    
    @property
    def image_data(self): 
        return self._image_data
    
    def update_data(self, new_data: ImageData): # actualiza la imagen completa
        self._image_data = new_data
    
    def set_pixel(self, x, y, color): # modifica un pixel especifico
        self._image_data.set_pixel(x, y, color)

    def get_bytes(self): # obtiene los bytes listos para enviarlos a la GPU
        return self._image_data.tobytes()