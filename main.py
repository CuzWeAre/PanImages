import tkinter
from PIL import Image, ImageDraw
import os
import numpy
from moviepy.editor import VideoFileClip, ImageSequenceClip, VideoClip, concatenate_videoclips, ImageClip


class MainProcess:
    """主程序"""

    def __init__(self):
        """初始化应用设置"""
        self.proportion = 16 / 9
        self.gap = 200
        self.duration = 5
        self.ending_time = 10

    def stitch(self):
        """用于拼接图片的函数"""
        # 获取当前目录
        current_directory = os.getcwd()
        work_dir = current_directory + "\\images\\"
        # 获取当前目录下的所有文件
        all_files = os.listdir(work_dir)
        # 使用列表推导式过滤出图片文件
        image_files = sorted(
            [file for file in all_files if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp'))])

        images = [Image.open(work_dir + image) for
                  image in image_files]

        self.width = sum([image.size[0] for image in images])
        self.height = max([image.size[1] for image in images])
        self.canvas: Image.Image = Image.new("RGB", (self.width + (len(image_files) - 1) * self.gap, self.height),
                                             color=(255, 255, 255))

        x_axis = 0
        for image in images:
            self.canvas.paste(image, (x_axis, 0))
            x_axis += image.size[0] + 200
        # self.canvas.show()

    def tovideo(self):
        """转换为视频"""

        pixel_speed = int((self.width - self.height * self.proportion) / self.duration)  # 每秒前进的像素数

        def make_frame(t):
            """生成对应t的帧"""
            left = t * pixel_speed
            box = [left, 0, int(self.height * self.proportion) + left, self.height]
            return numpy.array(self.canvas.crop(box))

        video_clip0 = VideoClip(make_frame, duration=self.duration)
        # self.canvas.crop((self.width-self.height*self.proportion,0,self.width,self.height)).show()
        video_clip1 = ImageClip(
            numpy.array(self.canvas.crop((self.width - self.height * self.proportion, 0, self.width, self.height))),
            duration=self.ending_time)
        video = concatenate_videoclips([video_clip0, video_clip1])
        output_file = "custom_video.mp4"
        video.write_videofile(output_file, codec='libx264', fps=60)


if __name__ == "__main__":
    a = MainProcess()

    from tkinter import ttk

    root = tkinter.Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    ttk.Button(frm, text="拼接", command=a.stitch).grid(column=1, row=0)
    ttk.Button(frm, text="视频", command=a.tovideo).grid(column=2, row=0)
    root.mainloop()
