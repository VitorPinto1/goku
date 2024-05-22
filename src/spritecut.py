import os
from PIL import Image

# Cargar la imagen
img_path = 'assets/sprites/gokugoku.png'
img = Image.open(img_path)

# Dimensiones de cada sprite (ajustar según sea necesario)
sprite_width = 38
sprite_height = 60

# Crear una carpeta para guardar los sprites cortados
output_folder = 'assets/sprites/cut'
os.makedirs(output_folder, exist_ok=True)

# Obtener las dimensiones de la imagen
img_width, img_height = img.size

# Cortar los sprites y guardarlos
sprite_count = 0
for y in range(0, img_height, sprite_height):
    for x in range(0, img_width, sprite_width):
        box = (x, y, x + sprite_width, y + sprite_height)
        sprite = img.crop(box)
        sprite.save(os.path.join(output_folder, f'sprite_{sprite_count}.png'))
        sprite_count += 1

# Mostrar un mensaje con la cantidad de sprites guardados
print(f'Se han guardado {sprite_count} sprites en la carpeta {output_folder}.')
