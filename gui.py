import tkinter as tk
import _thread
import deal
from PIL import Image, ImageTk

path = 'image/example.jpg'
img = Image.open(path)

if __name__ == '__main__':
    master = tk.Tk()

    canDraw = tk.IntVar(value=0)
    beginX = tk.IntVar(value=0)
    beginY = tk.IntVar(value=0)
    endX = tk.IntVar(value=0)
    endY = tk.IntVar(value=0)

    photo = ImageTk.PhotoImage(img)
    canvas = tk.Canvas(master, bg='white', width=800, height=600)
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)
    canvas.grid(row=0, columnspan=3)


    def onLeftButtonDown(event):
        canDraw.set(1)
        beginX.set(event.x)
        beginY.set(event.y)


    def onLeftButtonMove(event):
        global lastDraw
        if canDraw.get() == 0:
            return

        # 先删除矩形，再画一个矩形，没什么用，只是看着舒服点
        try:
            canvas.delete(lastDraw)
        except Exception as e:
            pass
        lastDraw = canvas.create_rectangle(beginX.get(), beginY.get(), event.x, event.y)


    def onLeftButtonUp(event):
        canvas.create_rectangle(beginX.get(), beginY.get(), event.x, event.y)
        endX.set(event.x)
        endY.set(event.y)
        canDraw.set(0)


    canvas.bind('<Button-1>', onLeftButtonDown)
    canvas.bind('<B1-Motion>', onLeftButtonMove)
    canvas.bind('<ButtonRelease-1>', onLeftButtonUp)

    tk.Label(master, text="停留时间：").grid(row=2)
    e2 = tk.Entry(master)
    e2.grid(row=2, column=1, padx=5, pady=5)


    def threadFun():
        deal.deal(beginX.get(), beginY.get(), endX.get(), endY.get(), e2.get())


    def show():
        print("output：%s" % e2.get())
        print(beginX.get())
        print(beginY.get())
        print(endX.get())
        print(endY.get())
        # 抛线程处理，不然ui会卡死
        _thread.start_new_thread(threadFun, ())

    tk.Button(master, text="开始检测", width=10, command=show).grid(row=2, column=2, sticky="w", padx=10, pady=5)

    master.mainloop()
