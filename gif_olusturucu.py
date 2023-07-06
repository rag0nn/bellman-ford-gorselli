# -*- coding: utf-8 -*-
"""
#ALFABE SIRASINA GÖRE GİF YAPAN KOD
"""

import glob
import os
from PIL import Image

def make_gif(frame_folder):
    frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*.JPG")]
    frame_one = frames[0]
    frame_one.save("my_awesome.gif", format="GIF", append_images=frames,
               save_all=True, duration=400, loop=0)
    
make_gif("./ims")
    