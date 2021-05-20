import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog
import os


def showPhoto():
    root = tk.Toplevel()
    root.title('违章车辆检测')
    root.geometry('500x500')

    canvas = tk.Canvas(root, height=400, width=400)
    canvas.pack()

    path = tk.StringVar()

    def resize(image):
        w, h = image.size
        mlength = max(w, h)  # 找出最大的边
        mul = 400 / mlength  # 缩放倍数
        w1 = int(w * mul)  # 重新获得高和宽
        h1 = int(h * mul)
        return image.resize((w1, h1))

    def show_image(path):
        global img  # 要申明全局变量我猜测是调用了canvas
        image = Image.open(path)  # 打开图片
        re_image = resize(image)  # 调用函数
        img = ImageTk.PhotoImage(re_image)  # PhotoImage类是用来在label和canvas展示图片用的
        canvas.create_image(200, 200, anchor='center', image=img)

    def openpicture():
        # 打开一张图片并显示
        global fileindex, fatherpath, files, file_num

        fatherpath = "output"
        files = os.listdir(fatherpath)  # 该路径下的所有文件并生成列表
        file_num = len(files)
        fileindex = 0  # 获取当前文件的索引值
        filepath1 = os.path.join(fatherpath, files[fileindex])
        show_image(filepath1)

    def previous():
        global fileindex, fatherpath, files, file_num
        fileindex -= 1
        if fileindex == -1:
            fileindex = file_num - 1
        filepath1 = os.path.join(fatherpath, files[fileindex])
        show_image(filepath1)

    def back():
        global fileindex, fatherpath, files, file_num
        fileindex += 1
        if fileindex == file_num:
            fileindex = 0
        filepath2 = os.path.join(fatherpath, files[fileindex])
        show_image(filepath2)

    tk.Button(root, text='显示违章车辆', command=openpicture).pack()
    tk.Button(root, text='上一张', command=previous).pack(side='left')
    tk.Button(root, text='下一张', command=back).pack(side='right')


if __name__ == '__main__':
    showPhoto()
