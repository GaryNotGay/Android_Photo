# -*- coding: utf-8 -*-

# @Author  :  lijishi
# @Contact :  lijishi@emails.bjut.edu.cn
# @Software:  Pycharm & Python 3.7
# @EditTime:  Jan 8, 2020
# @Version :  1.0
# @describe:  GUI of Control MIUI Photoed
# @LICENSE :  GNU GENERAL PUBLIC LICENSE Version 3

# References
# https://blog.csdn.net/fancy10255/article/details/88965926

import base64
import time
import re
import os
import subprocess
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk
from tkinter import *
from picture import Icon
from picture import Gif

num = -1
def Photo():
    num_limit = int(photo_num.get())
    time_gap = int(photo_time.get())
    path = str(adb_path.get())
    global num
    num += 1
    have_num.set(num)
    last_num.set(num_limit-num)
    last_time.set((num_limit-num) * time_gap)

    start_camera = path + r'\adb shell am start -a android.media.action.STILL_IMAGE_CAMERA'
    #os.system(start_camera)
    subprocess.run(start_camera, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    Shutter(path)
    if num == num_limit:
        have_num.set(num)
        last_num.set(num_limit - num)
        last_time.set((num_limit - num) * time_gap)
        num = -1
        Finish(path)
    else:
        main_window.after(time_gap * 1000, Photo)

def Shutter(path):
    #os.system(adb_path + r" devices")
    #start_camera = path + r'\adb shell am start -a android.media.action.STILL_IMAGE_CAMERA'
    shutter_command = path + r'\adb shell input keyevent 27'
    #os.system(start_camera)
    #os.system(shutter_command)

    subprocess.run(shutter_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def SelectADBPath():
    path_ = tkinter.filedialog.askopenfilename()
#    path_ = path_.replace("/", "\\\\")
    adb_path.set(path_[:-7])
    shutter_path = path_[:-7]

def About():
    # window centered
    about_window = Toplevel()
    screen_width = about_window.winfo_screenwidth()
    screen_heigh = about_window.winfo_screenheight()
    about_window_width = 455
    about_window_heigh = 295
    x = (screen_width - about_window_width) / 2
    y = (screen_heigh - about_window_heigh) / 2
    about_window.geometry("%dx%d+%d+%d" % (about_window_width, about_window_heigh, x, y))

    # window layout
    global cha_gif
    about_window.title('About')
    with open('tmp.ico', 'wb') as tmp:
        tmp.write(base64.b64decode(Icon().img))
    about_window.iconbitmap('tmp.ico')
    os.remove('tmp.ico')
#    about_window.iconbitmap(".\\cha.ico")
    with open('tmp.gif', 'wb') as tmp:
        tmp.write(base64.b64decode(Gif().img))
#    about_window.iconbitmap('temp.gif')
    cha_gif = tk.PhotoImage(file="tmp.gif")

#    os.remove('temp.gif')
#    cha_gif = tk.PhotoImage(file=".\\cha.gif")
    software_frame = ttk.LabelFrame(about_window, text='Software Info')
    software_frame.grid(row=0, column=0, rowspan=5, columnspan=4, padx=50, pady=5)
    ttk.Label(software_frame, image=cha_gif, compound='left').grid(row=0, rowspan=3, column=0)
    os.remove('tmp.gif')
    ttk.Label(software_frame, text="Android Photo Version 1.0").grid(row=0, column=1, sticky = W)
    ttk.Label(software_frame, text="@Author    :   lijishi").grid(row=1, column=1, sticky = W)
    ttk.Label(software_frame, text="@EditTime  :   Jan 8,2020").grid(row=2, column=1, sticky = W)

    copyright_frame = ttk.LabelFrame(about_window, text='LICENSE Info')
    copyright_frame.grid(row=5, column=0, rowspan=3, columnspan=4, padx=50, pady=5)
    ttk.Label(copyright_frame, text = "Github @ Android_Photo").grid(row=5, column=0)
    ttk.Label(copyright_frame, text="GNU GENERAL PUBLIC LICENSE Version 3").grid(row=6, column=0)

def Finish(path):
    back_command = path + r'\adb shell input keyevent 4'
    #os.system(back_command)
    subprocess.run(back_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    tk.messagebox.showinfo("Finish", "拍照完成！")

def Tips():
    tk.messagebox.showinfo("Tips", "确保手机开启USB调试\nadb工具包请自行下载\n间隔时间仅支持整数\n确保初始位置为手机桌面")

def Error():
    tk.messagebox.showerror("Error", "错误")

# window centered
main_window=tk.Tk()
screen_width = main_window.winfo_screenwidth()
screen_heigh = main_window.winfo_screenheight()
main_window_width = 440
main_window_heigh = 200
x = (screen_width-main_window_width) / 2
y = (screen_heigh-main_window_heigh) / 2
main_window.geometry("%dx%d+%d+%d" %(main_window_width,main_window_heigh,x,y))

# window layout
main_window.title("Android Photo V1.0")
with open('tmp.ico', 'wb') as tmp:
    tmp.write(base64.b64decode(Icon().img))
main_window.iconbitmap('tmp.ico')
os.remove('tmp.ico')
#main_window.iconbitmap(".\\cha.ico")
adb_path = tk.StringVar()
photo_num = tk.IntVar()
photo_time = tk.IntVar()
last_time = tk.IntVar()
last_num = tk.IntVar()
have_num = tk.IntVar()
output = tk.IntVar()
adb_path.set("请选择/键入adb.exe文件位置")
last_time.set('0')
last_num.set('0')
have_num.set('0')
path_frame = ttk.LabelFrame(main_window, text='路径选择')
path_frame.grid(row=0, column=0, rowspan=1, columnspan=6, padx=10, pady=5)
ttk.Label(path_frame, text = "ADB工具包：").grid(row = 0, column = 0, padx=10)
ttk.Entry(path_frame, width = 30, textvariable = adb_path).grid(row = 0, column = 1, columnspan = 2, padx=5)
ttk.Button(path_frame, width = 10, text = "选择", command = SelectADBPath).grid(row = 0, column = 4, padx=10, pady=5)
photo_frame = ttk.LabelFrame(main_window, text='拍摄参数')
photo_frame.grid(row=2, column=2, rowspan=2, columnspan=3, padx=10, pady=5, sticky = W)
ttk.Label(photo_frame, text = "拍照张数：").grid(row = 2, column = 2, padx=10)
ttk.Entry(photo_frame, width = 10, textvariable = photo_num).grid(row = 2, column = 3, padx=5, pady=5)
ttk.Label(photo_frame, text = "间隔时间：").grid(row = 3, column = 2, padx=10)
ttk.Entry(photo_frame, width = 10, textvariable = photo_time).grid(row = 3, column = 3, padx=5, pady=5)
display_frame = ttk.LabelFrame(main_window, text='拍摄信息')
display_frame.grid(row=2, column=0, rowspan=3, columnspan=2, padx=10, pady=5, sticky = W)
ttk.Label(display_frame, text = "剩余时间：").grid(row = 2, column = 0, padx=5, pady=5)
last_time_label = ttk.Label(display_frame, textvariable = last_time).grid(row = 2, column = 1, padx=5)
ttk.Label(display_frame, text = "已拍张数：").grid(row = 3, column = 0, padx=5, pady=5)
have_num_label = ttk.Label(display_frame, textvariable = have_num).grid(row = 3, column = 1, padx=5)
ttk.Label(display_frame, text = "剩余张数：").grid(row = 4, column = 0, padx=5, pady=5)
last_num_label = ttk.Label(display_frame, textvariable = last_num).grid(row = 4, column = 1, padx=5)
ttk.Button(main_window, text = "拍照", command = lambda: Photo()).grid(row = 2, column = 5, sticky = S)
ttk.Button(main_window, text = "提示", command = Tips).grid(row = 3, column = 5)
ttk.Button(main_window, text = "关于", command = About).grid(row = 4, column = 5)

main_window.mainloop()