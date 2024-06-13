import zipfile
import pprint
import json
import utils
import tkinter as tk
from PIL import ImageTk, Image
import io


with zipfile.ZipFile('./sample1.zip', 'r') as arch:
    preset = utils.get_preset(arch, 'preset.json')

pprint.pp(preset['preset_root'])