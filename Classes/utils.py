from pygame.image import load as img_load
from pygame.transform import scale
from glob import glob
from os import walk, getcwd

# Importa tutte le animazioni dato un determinato percorso
# scalando le immagini seguendo x e y come risoluzione
def import_animations(path, x, y):
    
    #Trova il percorso completo
    full_path = f"{getcwd()}/{path}".replace("\\", "/")
    folders = [folder for folder in  walk(full_path)][0][1]
    animations = {}
    for folder in folders:
        image_list = glob(f"{full_path}/{folder}/*.png")
        animations[folder] = [
            scale(img_load(image), (x, y)) 
            for image in image_list
            ]
    return animations

def import_bullets(path, x, y):
    
    full_path = f"{getcwd()}/{path}".replace("\\", "/")
    bullets = {
        i.replace("\\", "/").split("/")[-1].split(".png")[0] : scale(img_load(i), (x,y) if "shuriken" in i else (x/2, y))
        for i in glob(f"{full_path}/*.png")
        }
    return bullets
