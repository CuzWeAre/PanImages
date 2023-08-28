import tkinter
from PIL import Image, ImageDraw
import os


class MainProcess:
    """主程序"""

    def __init__(self):
        """初始化应用设置"""
        pass

    def stitch(self):
        """用于拼接图片的函数"""
        # 获取当前目录
        current_directory = os.getcwd()
        work_dir = current_directory+"\\images\\"
        # 获取当前目录下的所有文件
        all_files = os.listdir(work_dir)
        # 使用列表推导式过滤出图片文件
        image_files = sorted([file for file in all_files if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp'))])

        images = [Image.open(work_dir+image) for
                image in image_files]

        canvas_width = sum([image.size[0] for image in images])
        canvas_height = max([image.size[1] for image in images])
        self.canvas:Image.Image = Image.new("RGB",(canvas_width,canvas_height),color=(255,255,255))
        # canvas_draw = ImageDraw.ImageDraw(canvas)
        x_axis = 0
        for image in images:
            self.canvas.paste(image, (x_axis, 0))
            x_axis += image.size[0]
        self.canvas.show()
        
        
        
if __name__ == "__main__":
    
    a = MainProcess()
    
    from tkinter import ttk
    root = tkinter.Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    ttk.Button(frm, text="拼接", command=a.stitch).grid(column=1, row=0)
    root.mainloop()