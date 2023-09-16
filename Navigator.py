#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from Navigator_ConvertFormat import ChangeFileFormat
from Navigator_OutPut import UploadPage
from main import Main_App

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # 设置窗口大小
        winWidth = 1000
        winHeight = 700
        # 获取屏幕分辨率
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()
        # 中间位置坐标
        x = int((screenWidth - winWidth) / 2)
        y = int((screenHeight - winHeight) / 2)
        # 设置窗口初始位置在屏幕居中
        self.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
        self.resizable(False, False)                # 窗口不能更改大小
        self.title('主页')
        # self.overrideredirect(True)    # 取消窗口边框


class mainFrameA(tk.Frame):
    """这是一个 tk.Frame 对象，可以比如 KPSFrame(self).pack() 这么来显示"""
    def __init__(self, master):
        super().__init__(master)

        global img1, img2 ,img3 ,img4
        container = tk.Frame(self, width=1366, height=768)
        container.pack()


        def switchToConfig():
            ChangeFileFormat()

        def switchToOutput():
            UploadPage()

        def switchToFrameB():
            apppppp = tk.Toplevel()
            Main_App(apppppp).pack()

            # 假如使用打开exe的方式的话
            # import subprocess
            # subprocess.Popen(r"D:\Python_Projects\My_GUIs\Software_FollowUp\Main\main.exe")




        def QuitAll():
            self.quit()


        img1 = tk.PhotoImage(file = r'img/ico_transfor_128.png')
        img2 = tk.PhotoImage(file='img/ico_start_128.png')
        img3 = tk.PhotoImage(file='img/ico_quit_128.png')
        img4 = tk.PhotoImage(file='img/ico_2cloud_128.png')

        tk.Label(container, text='随访管理与记录系统', font=('黑体', 55)).place(relx=.5, rely=.15, anchor="center")
        tk.Label(container, text='尤组专用   版本号 v2.0.0-beta   更新日期：2022/12/5', font=('黑体', 20)).place(
            relx=.5, rely=.25,
            anchor="center")

        Button_box_line1 = tk.Frame(container)
        Button_box_line1.place(relx=.5, rely=.45, anchor="center")

        # 设置按钮2
        Button2 = tk.Label(Button_box_line1, image=img2,relief=tk.GROOVE,bd=2,width=200,height=160)
        Button2.grid(row=0, column=0, sticky='nw', padx=30, pady=0, ipadx=0, ipady=0)
        Button2.bind('<Button-1>', lambda e: switchToFrameB())  # 左键切换为橙色界面
        tk.Label(Button_box_line1, text='开始', font=('黑体', 25)).grid(row=1, column=0, sticky='n')

        Button_box = tk.Frame(container)
        Button_box.place(relx=.5, rely=.75, anchor="center")

        # 设置按钮1
        Button1 = tk.Label(Button_box, image=img1,relief=tk.GROOVE,bd=2,width=200,height=160)
        Button1.grid(row=0, column=0, sticky='nw', padx=30, pady=0, ipadx=0, ipady=0)
        Button1.bind('<Button-1>', lambda e: switchToConfig())  # 左键切换为橙色界面
        tk.Label(Button_box, text='csv转读取格式', font=('黑体', 25)).grid(row=1, column=0, sticky='n')

        # 设置按钮1
        Button_upload = tk.Label(Button_box, image=img4,relief=tk.GROOVE,bd=2,width=200,height=160)
        Button_upload.grid(row=0, column=1, sticky='nw', padx=30, pady=0, ipadx=0, ipady=0)
        Button_upload.bind('<Button-1>', lambda e: switchToOutput())  # 左键切换为橙色界面
        tk.Label(Button_box, text='导出csv', font=('黑体', 25)).grid(row=1, column=1, sticky='n')

        # 设置按钮3
        Button3 = tk.Label(Button_box, image=img3,relief=tk.GROOVE,bd=2,width=200,height=160)
        Button3.grid(row=0, column=3, sticky='nw', padx=30, pady=0, ipadx=0, ipady=0)
        Button3.bind('<Button-1>', lambda e: QuitAll())  # 左键切换为橙色界面
        tk.Label(Button_box, text='关闭', font=('黑体', 25)).grid(row=1, column=3, sticky='n')


if __name__ == "__main__":
    app = App()

    mainFrame_ = mainFrameA(app)
    mainFrame_.pack(fill=tk.BOTH, expand=True)
    app.mainloop()

