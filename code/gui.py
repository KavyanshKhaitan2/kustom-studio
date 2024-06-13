import tkinter as tk
from tkinter import ttk
from tkinter import font
import utils
from utils import try_get_item
import zipfile
import typeddicts
from typeddicts import KWGTPreset
import formula_parse
import tkextrafont # type: ignore



class App():
    def __init__(self, filepath) -> None:
        self.filepath = filepath

        self.root = tk.Tk()
        self.root.title("Kustom Widget - Kustom Studio")
        self.root.geometry('200x200')
        
        self.window2 = tk.Toplevel()
        self.window2.title("Widget View")
        self.window2.protocol("WM_DELETE_WINDOW", self.root.quit)
        
        with zipfile.ZipFile(filepath, 'r') as arch:
            self.preset: KWGTPreset = utils.get_preset(arch)
        
        canvas_width = self.preset["preset_info"]['width']
        canvas_width = 1000
        canvas_height = self.preset['preset_info']['height']
        
        self.canvas_startx = canvas_width//2
        self.canvas_starty = canvas_height//2
        
        ttk.Label(self.root, text=f"{self.canvas_startx=}\n{self.canvas_starty=}").grid()
        
        self.canvas = tk.Canvas(self.window2, width=canvas_width, height=canvas_height)
        self.canvas.grid()
        
        self.render_canvas()
    
    def render_canvas(self):
        for item in self.preset['preset_root']['viewgroup_items']:
            x_offset: float = try_get_item(item, 'position_offset_x') # type: ignore
            y_offset: float = try_get_item(item, 'position_offset_y') # type: ignore

            if item['internal_type'] == 'StackLayerModule':
                _stack = typeddicts._KWGTPresetRoot(item)
                _stack_x_offset = x_offset
                _stack_y_offset = y_offset
                for stack_item in _stack['viewgroup_items']:
                    x_offset: float = _stack_x_offset + try_get_item(stack_item, 'position_offset_x') # type: ignore
                    y_offset: float = _stack_y_offset + try_get_item(stack_item, 'position_offset_y') # type: ignore
                    if stack_item['internal_type'] == 'TextModule':
                        text: str = try_get_item(stack_item, 'text_expression', 'Blank text') # type: ignore
                        text = formula_parse.parse(text)

                        x = self.canvas_startx + x_offset
                        y = self.canvas_starty + y_offset
                        text_size = int(utils.try_get_item(stack_item, 'text_size'))
                        font_path: str = utils.try_get_item(stack_item, 'text_family') # type: ignore
                        args = utils.render_text_helper(self.filepath, x, y, text, text_size, font_path)
                        print(args)
                        self.canvas.create_text(x, y, **args)
            
            if item['internal_type'] == 'TextModule':
                text: str = try_get_item(item, 'text_expression', 'Blank text') # type: ignore
                text = formula_parse.parse(text)

                x = self.canvas_startx + x_offset
                y = self.canvas_starty + y_offset
                text_size = int(utils.try_get_item(item, 'text_size'))
                font_path: str = utils.try_get_item(item, 'text_family') # type: ignore
                args = utils.render_text_helper(self.filepath, x, y, text, text_size, font_path)
                self.canvas.create_text(x, y, **args)
    
    def run(self) -> None:
        self.root.mainloop()
    

def main():
    app = App('./sample1.zip')
    app.run()

if __name__ == "__main__":  
    main()