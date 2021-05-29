import tkinter as tk
import _thread
import deal
from PIL import Image, ImageTk

path = 'image/example.jpg'
img = Image.open(path)

if __name__ == '__main__':
    master = tk.Tk()

    drawType = tk.IntVar(value=0)
    canDraw = tk.IntVar(value=0)
    beginX = tk.IntVar(value=0)
    beginY = tk.IntVar(value=0)
    drawX = tk.IntVar(value=0)
    drawY = tk.IntVar(value=0)
    endX = tk.IntVar(value=0)
    endY = tk.IntVar(value=0)
    lastDraw = 0

    photo = ImageTk.PhotoImage(img)
    canvas = tk.Canvas(master, bg='white', width=800, height=600)
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)
    canvas.grid(row=0, rowspan=3)


    def onLeftButtonDown(event):
        canDraw.set(1)
        beginX.set(event.x)
        beginY.set(event.y)
        drawX.set(event.x)
        drawY.set(event.y)


    def onLeftButtonMove(event):
        global lastDraw
        if canDraw.get() == 0:
            return
        if drawType.get() == 1:
            canvas.create_line(drawX.get(), drawY.get(), event.x, event.y)
            drawX.set(event.x)
            drawY.set(event.y)
        elif drawType.get() == 2:
            # 先删除矩形，再画一个矩形，没什么用，只是看着舒服点
            try:
                canvas.delete(lastDraw)
            except Exception as e:
                pass
            lastDraw = canvas.create_rectangle(beginX.get(), beginY.get(), event.x, event.y)


    def onLeftButtonUp(event):
        if drawType.get() == 1:
            canvas.create_line(beginX.get(), beginY.get(), event.x, event.y)
        if drawType.get() == 2:
            canvas.create_rectangle(beginX.get(), beginY.get(), event.x, event.y)
        endX.set(event.x)
        endY.set(event.y)
        canDraw.set(0)

    def onRightButtonUp(event):
        menu.post(event.x_root, event.y_root)

    menu = tk.Menu(master, tearoff=0)
    menu.add_command(label='Curve', command=lambda: drawType.set(1))
    menu.add_command(label='Rectangle', command=lambda: drawType.set(2))

    canvas.bind('<Button-1>', onLeftButtonDown)
    canvas.bind('<B1-Motion>', onLeftButtonMove)
    canvas.bind('<ButtonRelease-1>', onLeftButtonUp)


    def threadFun():
        try:
            time = int(e2.get())
        except Exception as e:
            time = 1
            pass
        finally:
            e2.delete(0, "end")

        deal.deal(beginX.get(), beginY.get(), endX.get(), endY.get(), time, text)


    def show():
        print("output：%s" % e2.get())
        print(beginX.get())
        print(beginY.get())
        print(endX.get())
        print(endY.get())
        # 抛线程处理，不然ui会卡死
        _thread.start_new_thread(threadFun, ())


    inputBar = tk.Frame()
    inputBar.grid(row=1, column=1)
    tk.Label(inputBar, text="停留时间：").grid(row=2, sticky=tk.W)
    e2 = tk.Entry(inputBar)
    e2.insert("end", "请输入检测时间阈值")
    e2.grid(row=2, column=1)
    tk.Button(inputBar, text="开始检测", command=show).grid(row=2, column=2, sticky=tk.W, padx=10, pady=10)

    outputBar = tk.Frame()
    text = tk.Text(outputBar, height=30, width=50)
    text.grid(sticky=tk.N)
    outputBar.grid(row=0, column=1)

    canvas.bind('<ButtonRelease-3>', onRightButtonUp)
    master.mainloop()
