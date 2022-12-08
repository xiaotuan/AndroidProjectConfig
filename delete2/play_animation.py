import os
from time import sleep
import tkinter as tk
from threading import Timer
from PIL import Image, ImageTk

def playAnimation(dir, rate):
    """
    播放帧动画
    dir: 动画图片目录
    rate: 一秒钟播放的图片数量
    """
    if os.path.isdir(dir) and os.path.exists(dir):
        pictures = os.listdir(dir)
        if len(pictures) > 0:
            top = tk.Tk()
            pic = dir + "/" + pictures[len(pictures) - 1]
            print("picture path: " + pic)
            maxWidth = 480.0
            img = Image.open(pic)
            width = img.width
            height = img.height
            if width > int(maxWidth) or height > int(maxWidth):
                wscale = maxWidth / width
                hscale = maxWidth / height
                scale = min(wscale, hscale)
                width = int(width * scale)
                height = int(height * scale)

            print("width: " + str(width) + ", height: " + str(height))
            image = ImageTk.PhotoImage(image=Image.open(pic).resize(size=(width, height)))
            print(dir + "/anim_019.png")
            top.geometry("%dx%d" % (width, height))
            #label = tk.Label(top, width=width, height=height, anchor=tk.CENTER, text="正在加载中...")
            label = tk.Label(top, width=width, height=height, image=image)
            label.pack(side=tk.LEFT)
            #t = Timer(interval=1, function=showPicture, args=[dir, label, rate, image, width, height])
            #t.start()
            #label.configure(image=image)
            top.mainloop()
        else:
            print("There are no pictures in the {dir} directory.")
    else:
        print("{dir} isn't a direcotry or exists.")


def showPicture(dir, label, rate, image, width, height):
    """
    显示图片
    """
    images = []
    for p in os.listdir(dir):
        images.append(tk.PhotoImage(file=dir + "\\" + p))
        #images.append(ImageTk.PhotoImage(image=Image.open(dir + "/" + p).resize(size=(width, height))))
    
    label.configure(text="")

    interval = 1.0 / rate
    for img in images:
        label.configure(image=img)
        sleep(interval)

    label.configure(image=image)