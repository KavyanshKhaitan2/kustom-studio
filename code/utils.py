import tkinter as tk
from PIL import ImageTk, Image
import io
from dataclasses import dataclass
from typing import TypedDict, Any
import zipfile
import json
import tkextrafont # type: ignore
from typeddicts import KWGTPresetInfo, KWGTPreset
import uuid
import tempfile
import windows_metadata # type: ignore
import os
from tkinter import font

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

def try_get_item(dict: dict, item:str, defaultValue = 0) -> Any | None:
    try:
        return dict[item]
    except KeyError:
        return defaultValue

def getfile(archname: str, filepath:str):
    starter = 'kfile://org.kustom.provider/'
    new_filepath = filepath.removeprefix(starter)
    with zipfile.ZipFile(archname, 'r') as arch:
        return arch.read(new_filepath)

def get_preset(arch: zipfile.ZipFile, file='preset.json') -> KWGTPreset:
    with arch.open(file, 'r') as f:
        preset_data: KWGTPreset = json.loads(f.read())
        
    return preset_data

def get_temp_file(archname:str, filepath:str):
    
    starter = 'kfile://org.kustom.provider/'
    new_filepath = filepath.removeprefix(starter)

    with zipfile.ZipFile(archname, 'r') as arch:
        file_data = arch.read(new_filepath)

        file_extension = new_filepath.split('.')[-1]
        
        temp_file_path= f"{tempfile.gettempdir()}/kustom-studio/{uuid.uuid4()}.{file_extension}"

        try: os.mkdir(f'{tempfile.gettempdir()}/kustom-studio')
        except: pass
        

        if not temp_file_path:
            return ""

        with open(temp_file_path, "xb") as f:
            f.write(file_data)
    return temp_file_path

def get_font_family(fontPath):
    props = windows_metadata.WindowsAttributes(fontPath)
    return props['Title']

def render_text_helper(filepath:str, x:float, y:float, text:str, font_size:int, font_path:str):
    font_size = int(font_size // 1.5)
    if font_path:
        font_path = get_temp_file(filepath, font_path)
        family_name = get_font_family(font_path)
        _font = tkextrafont.Font(file=font_path, size=int(font_size), family=family_name)
    else:
        _font = font.Font(size = int(font_size))
    
    args = {
        "text": text,
        "font": _font
    }
    return args