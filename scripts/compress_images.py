import os
from pickletools import optimize
from PIL import Image
from settings import PARPATH

def compress_images():
    srcpath = os.path.join(PARPATH, 'images')
    for file in os.listdir(srcpath):
        with Image.open(os.path.join(srcpath, file)) as image:
            image = image.resize((180, 180))
            image.save(os.path.join(srcpath, 'thumbnails', file), optimize=True, quality=85)

if __name__ == '__main__':
    compress_images()