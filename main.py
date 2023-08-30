from PIL import Image, ImageDraw
import os
import numpy
from moviepy.editor import VideoFileClip, ImageSequenceClip, VideoClip, concatenate_videoclips, ImageClip,TextClip


class MainProcess:
    """主程序"""

    def __init__(self):
        """初始化应用设置"""
        self.proportion = 1080 / 2060
        self.gap = 200
        self.duration = 5
        self.ending_time = 10
        self.codec = "libx264"
        self.fps = 60

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

        self.width = sum([image.size[0] for image in images]) + (len(image_files) - 1) * self.gap
        self.height = max([image.size[1] for image in images])
        self.canvas: Image.Image = Image.new("RGB", (self.width, self.height),
                                             color=(255, 255, 255))

        x_axis = 0
        for image in images:
            self.canvas.paste(image, (x_axis, 0))
            x_axis += image.size[0] + 200

        output_img = "stitched_img.jpg"
        self.canvas.save(output_img)

    def tovideo(self):
        """转换为视频"""
        # self.canvas.crop((0,0,self.width,self.height)).show()

        pixel_speed = int((self.width - self.height * self.proportion) / self.duration)  # 每秒前进的像素数

        def make_frame(t):
            """生成对应t的帧"""
            left = t * pixel_speed
            box = [left, 0, int(self.height * self.proportion) + left, self.height]
            return numpy.array(self.canvas.crop(box))

        video_clip0 = VideoClip(make_frame, duration=self.duration)
        video_clip1 = ImageClip(
            numpy.array(self.canvas.crop((self.width - self.height * self.proportion, 0, self.width, self.height))),
            duration=self.ending_time)
        video = concatenate_videoclips([video_clip0, video_clip1])
        output_file = "video.mp4"
        video.write_videofile(output_file, codec=self.codec, fps=self.fps)

    def add_text(self):
        """为视频底部添加文字"""
        text = Image.new("RGB",(self.width,self.height))
        text2 = TextClip("Hello TextClip")




if __name__ == "__main__":
    a = MainProcess()

    import tkinter
    from tkinter import ttk

    root = tkinter.Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    ttk.Button(frm, text="拼接", command=a.stitch).grid(column=1, row=0)
    ttk.Button(frm, text="视频", command=a.tovideo).grid(column=2, row=0)
    root.mainloop()
