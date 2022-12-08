# from time import sleep
# from playsound import playsound

# path = "C:\\Users\\xiaotuan\\Desktop\\曾经的你.mp3"
# path = path.replace(" ", "%20")
# playsound(path)

# import time
# import pygame

# path = "C:\\Users\\xiaotuan\\Desktop\\曾经的你.mp3"
# pygame.mixer.init()
# trace = pygame.mixer.music.load(path)
# pygame.mixer.music.play()
# time.sleep(10)
# pygame.mixer.music.stop()


# import os

# path = "C:\\Users\\xiaotuan\\Desktop\\曾经的你.mp3"
# os.system(path)

# import pyaudio

# import wave

# CHUNK = 1024

# FILENAME = "C:\\Users\\xiaotuan\\Desktop\\曾经的你.mp3"

# def play(filename = FILENAME):
#     wf = wave.open(filename, 'rb')
#     p = pyaudio.PyAudio()
#     stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#     channels=wf.getnchannels(),
#     rate=wf.getframerate(),
#     output=True)
#     data = wf.readframes(CHUNK)

#     while data != b'':
#         stream.write(data)
#         data = wf.readframes(CHUNK)

#     stream.stop_stream()
#     stream.close()
#     p.terminate()

# play()

import os
from time import sleep
import tkinter as tk
from threading import Timer
from PIL import Image, ImageTk

def playAnimation(dir, rate):
    """
    播放帧动画
    """
    if os.path.isdir(dir) and os.path.exists(dir):
        pictures = os.listdir(dir)
        if len(pictures) > 0:
            top = tk.Tk()
            pic = dir + "\\" + pictures[len(pictures) - 1]
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

            image = ImageTk.PhotoImage(image=Image.open(pic).resize(size=(width, height)))
            top.geometry("%dx%d" % (width, height))
            label = tk.Label(top, width=width, height=height, anchor=tk.CENTER, text="正在加载中...")
            label.pack(side=tk.LEFT)
            t = Timer(interval=1, function=showPicture, args=[dir, label, rate, image, width, height])
            t.start()
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
        # images.append(tk.PhotoImage(file=dir + "\\" + p))
        images.append(ImageTk.PhotoImage(image=Image.open(dir + "\\" + p).resize(size=(width, height))))
    
    label.configure(text="")

    interval = 1.0 / rate
    for img in images:
        label.configure(image=img)
        sleep(interval)

    label.configure(image=image)

path = "C:\\WorkSpace\\GitSpace\\Xiaotuan\\AndroidProjectConfig\\temp\\Animation"
playAnimation(path, 23)
