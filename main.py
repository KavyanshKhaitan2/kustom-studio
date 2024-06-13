import zipfile
import pprint
import json
import kwgtutils
import tkinter as tk
from PIL import ImageTk, Image
import io


with zipfile.ZipFile('./sample1.zip', 'r') as arch:
    preset = kwgtutils.get_preset(arch, 'preset.json')

