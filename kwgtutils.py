import tkinter as tk
from PIL import ImageTk, Image
import io
from dataclasses import dataclass
from typing import TypedDict, Any
import zipfile
import json
from typeddicts import KWGTPresetInfo, KWGTPreset


def get_preset_info(preset_data: KWGTPreset):
    authorinfo: KWGTPresetInfo = preset_data['preset_info']
    return authorinfo

class ImageViewer:
    def __init__(self, rb_image, max_height = 400):
        self.root = tk.Tk()
        image = Image.open(io.BytesIO(rb_image))
        # create image label using pillow to parse image data
        height = min([image.height, max_height])
        width = image.width * (height/image.height)
        
        print(f"{height=}, {width=}")
        
        self.image = ImageTk.PhotoImage(image.resize((int(width), int(height))))
        self.root.geometry(f"{int(width)}x{int(height)}")
        # create label0, 0, width, height)))
        self.label = tk.Label(self.root, image=self.image, background='green')
        # add label to root window
        self.label.grid()
        
    def run(self):
        self.root.mainloop()
def show_image(image, max_height = 400):
    ImageViewer(image, max_height).run()



def get_preset(arch: zipfile.ZipFile, file: str) -> KWGTPreset:
    with arch.open(file, 'r') as f:
        preset_data: KWGTPreset = json.loads(f.read())
        
    return preset_data