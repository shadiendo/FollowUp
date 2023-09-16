#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import tkinter as tk
from Frame_InfoShow import InfoShow
from tools import AppSettings, ValueInDatabase_read, ValueInDatabase_write, pickle2csv, searchPat_from_nameAndHospID, \
    howManyToFinsh, restore_from_theLastUnfinishedWork
from tkinter import scrolledtext, ttk
from tkinter import END
import tkinter.messagebox
import pyautogui


global DIV_,cnt,Pro_Bar_


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        Main_App(self).pack()

class Main_App(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        global DIV_,cnt,Pro_Bar_


        # 设置窗口大小
        winWidth = 1190
        winHeight = 690
        # 获取屏幕分辨率
        screenWidth = self.master.winfo_screenwidth()
        screenHeight = self.master.winfo_screenheight()
        # 中间位置坐标
        x = int((screenWidth - winWidth) / 2)
        y = int((screenHeight - winHeight) / 2)
        # 设置窗口初始位置在屏幕居中
        self.master.title("KPS_frame")
        # self.attributes("-topmost", 1)
        self.master.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
        self.master.resizable(False, False)
        self.master.title("Follow-Up And Registration Tool v1.2.1")


        finished_color = "green"

        def finished():
            # 做强制判断，生死备注写了没
            isAlive_judgement = ''.join(scr_deadOrMainInfoRecord.get(1.0,'end').split())

            if isAlive_judgement == "":
                LorD_label.config(bg='red',fg='white')
                tkinter.messagebox.showinfo('提示', '先把生死备注写了，谢谢')
                return
            elif ("活" not in isAlive_judgement) and ("生" not in isAlive_judgement) and ("死" not in isAlive_judgement):
                LorD_label.config(bg='red',fg='white')
                tkinter.messagebox.showinfo('提示', '请围绕主题，至少写个 活 | 生 | 死 ，三个字中的一个，谢谢')
                return
            elif ("生" in isAlive_judgement) and (len(isAlive_judgement)<=2):
                LorD_label.config(bg='red',fg='white')
                tkinter.messagebox.showinfo('提示', '字数太少，加点对该患者活着的描述')
                return
            elif ("活" in isAlive_judgement) and (len(isAlive_judgement)<=2):
                LorD_label.config(bg='red',fg='white')
                tkinter.messagebox.showinfo('提示', '字数太少，加点对该患者活着的描述')
                return
            elif ("死" in isAlive_judgement) and (len(isAlive_judgement)<=2):
                LorD_label.config(bg='red', fg='white')
                tkinter.messagebox.showinfo('提示', '字数太少，加点死亡描述')
                return
            else:
                LorD_label.config(bg='#f0f0f0', fg='black')

                pickle2csv()
                # tkinter.messagebox.showinfo("提示", "【数据已保存到原excel文件~】\n注：每次点击其实都会先保存至pkl文件\n这一步点击完成是为了加快软件速度")
                if content["完成与否"][0]=="":
                    content["完成与否"][1].config(bg=finished_color, fg="#ffffff")
                    content["完成与否"][0]="True"
                    ValueInDatabase_write(cnt,"完成与否","True")

                content["生死备注"][0] = scr_deadOrMainInfoRecord.get("1.0", 'end')
                content["总备注"][0] = scr_note.get("1.0", 'end')
                ValueInDatabase_write(cnt, "生死备注", scr_deadOrMainInfoRecord.get("1.0", 'end'))
                ValueInDatabase_write(cnt, "总备注", scr_note.get("1.0", 'end'))

                # 截图并保存图片的位置和名称
                time_now = str(time.strftime('%Y%m%d-%H%M%S'))  # 当前时间
                patPath = 'data\\img_save\\'
                filename = ValueInDatabase_read(cnt,"姓名")+"★"+ValueInDatabase_read(cnt,"住院号")+"★"+time_now + '.jpg'
                finalFile = os.path.join(patPath, filename)
                if not os.path.exists(patPath):
                    os.mkdir(patPath)

                # 截图保存
                pyautogui.screenshot(finalFile)
                print('成功保存图片至%s' % str(finalFile))

        def searchPat():
            global DIV_
            global cnt
            if IsThisPatFinished():
                name4search = str(name_input.get().strip())     # 记得去掉头尾空格
                hosId4search = str(hosId_input.get().strip())

                goal_index = searchPat_from_nameAndHospID(name4search,hosId4search)
                if type(goal_index) != int:
                    tkinter.messagebox.showerror("提示", goal_index)
                else:
                    DIV_.destroy()

                    cnt = goal_index
                    DIV_ = DIV(frameCCC, cnt)
                    DIV_.pack()
                    scr_deadOrMainInfoRecord.delete(1.0, END)
                    scr_note.delete(1.0, END)
                    read_content()

                    tkinter.messagebox.showinfo("提示", f"找到该人了，序号为{goal_index}")
                    name_input.set("")
                    hosId_input.set("")
            else:
                tkinter.messagebox.showinfo('提示', '请先点击【完成】')

        def restorationTheWork():
            global DIV_
            global cnt
            if IsThisPatFinished():
                getIndex = restore_from_theLastUnfinishedWork()
                if type(getIndex) != int:
                    tkinter.messagebox.showerror("提示", getIndex)
                else:
                    DIV_.destroy()

                    cnt = getIndex
                    DIV_ = DIV(frameCCC, cnt)
                    DIV_.pack()
                    scr_deadOrMainInfoRecord.delete(1.0, END)
                    scr_note.delete(1.0, END)
                    read_content()

                    tkinter.messagebox.showinfo("提示", f"从该病人开始吧！序号为{getIndex}")
                    name_input.set("")
                    hosId_input.set("")
            else:
                tkinter.messagebox.showinfo('提示', '请先点击【完成】')

        def IsThisPatFinished():
            judge = ValueInDatabase_read(cnt,"完成与否")
            if judge=="":
                return False
            else:
                XiaYiWei.config(state=tk.ACTIVE)
                ShangYiWei.config(state=tk.ACTIVE)
                return True

        def switch(selection,btn):
            global DIV_
            global cnt,Pro_Bar_

            # 判断1: 如果按了接通，那么必须要判断有没有点击完成
            if ValueInDatabase_read(cnt, "接通状态_接通")!="":
                if not IsThisPatFinished():
                    return tkinter.messagebox.showinfo('提示', '请先点击【完成】')

            if cnt == 0 and selection == "Previous":
                ShangYiWei.config(state=tk.DISABLED)
                tkinter.messagebox.showinfo('提示','这是第一个')
                return
            elif cnt == (AppSettings.howManyPatients()-1) and selection == "Next":
                XiaYiWei.config(state=tk.DISABLED)
                tkinter.messagebox.showinfo('提示','这是最后一个')
                return
            else:
                btn.config(state=tk.ACTIVE)
                DIV_.destroy()
                Pro_Bar_.destroy()

                if selection == "Previous":
                    cnt = cnt-1
                    DIV_ = DIV(frameCCC, cnt)
                    DIV_.pack()
                    scr_deadOrMainInfoRecord.delete(1.0, END)
                    scr_note.delete(1.0, END)
                    read_content()

                    Pro_Bar_ = Pro_Bar_npnf(frameCCC)
                    Pro_Bar_.place(x=0, y=0, anchor="nw")

                elif selection == "Next":
                    cnt = cnt+1
                    DIV_ = DIV(frameCCC, cnt)
                    DIV_.pack()
                    scr_deadOrMainInfoRecord.delete(1.0, END)
                    scr_note.delete(1.0, END)
                    read_content()

                    Pro_Bar_ = Pro_Bar_npnf(frameCCC)
                    Pro_Bar_.place(x=0, y=0, anchor="nw")


        def showVersionInfo():
            info = tk.Toplevel()
            info.title('子窗口')

            # 设置窗口大小
            toplevel_winWidth = 450
            toplevel_winHeight = 340
            screenWidth = self.winfo_screenwidth()
            screenHeight = self.winfo_screenheight()
            # 中间位置坐标
            toplevel_x = int((screenWidth - toplevel_winWidth) / 2)
            toplevel_y = int((screenHeight - toplevel_winHeight) / 2)
            # 设置窗口初始位置在屏幕居中
            info.geometry("%sx%s+%s+%s" % (toplevel_winWidth, toplevel_winHeight, toplevel_x, toplevel_y))
            info.resizable(False, False)

            # 创建画布，此处一定一定要加长宽，因为默认大小是380*270左右
            CANVAS = tk.Canvas(master=info, width=toplevel_winWidth, height=toplevel_winHeight)
            # 创建滚动条
            scro = tk.Scrollbar(master=info, width=15)
            scro.pack(side='right', fill='y')
            scro.config(command=CANVAS.yview)
            # 创建画布上存放东西的框架，后续将该frame与画布绑定
            bigBox = tk.Frame(CANVAS, width=toplevel_winWidth, height=700)
            bigBox.pack(anchor=tk.N, side='right')
            bigBox.pack_propagate(0)
            bigBox.update()
            # 进一步将三者绑定
            CANVAS.create_window((0, 0), window=bigBox, anchor=tk.N)  # anchor=tk.N 决定了把东西放上面，可以换成W看看
            CANVAS.configure(yscrollcommand=scro.set, scrollregion=CANVAS.bbox("all"))
            CANVAS.pack()


            with open(r'data/version_info.txt', 'r', encoding='utf-8') as f:
                infoV_1_1_0 = f.read()

            tk.Label(bigBox, text="Follow-Up And Registration Tool\nVersion 1.1.0",font=("Arial",18)).pack(padx=10,pady=20)
            tk.Label(bigBox,text=infoV_1_1_0,anchor= tk.W, justify='left',wraplength=350).pack(padx=10)

        def UserManual():
            info = tk.Toplevel()
            info.title('子窗口')

            # 设置窗口大小
            toplevel_winWidth = 450
            toplevel_winHeight = 340
            # 中间位置坐标
            screenWidth = self.winfo_screenwidth()
            screenHeight = self.winfo_screenheight()
            toplevel_x = int((screenWidth - toplevel_winWidth) / 2)
            toplevel_y = int((screenHeight - toplevel_winHeight) / 2)
            # 设置窗口初始位置在屏幕居中
            info.geometry("%sx%s+%s+%s" % (toplevel_winWidth, toplevel_winHeight, toplevel_x, toplevel_y))
            info.resizable(False, False)

            # 创建画布，此处一定一定要加长宽，因为默认大小是380*270左右
            CANVAS = tk.Canvas(master=info, width=toplevel_winWidth, height=toplevel_winHeight)
            # 创建滚动条
            scro = tk.Scrollbar(master=info, width=15)
            scro.pack(side='right', fill='y')
            scro.config(command=CANVAS.yview)
            # 创建画布上存放东西的框架，后续将该frame与画布绑定
            bigBox = tk.Frame(CANVAS, width=toplevel_winWidth, height=1000)
            bigBox.pack(anchor=tk.N, side='right')
            bigBox.pack_propagate(0)
            bigBox.update()
            # 进一步将三者绑定
            CANVAS.create_window((0, 0), window=bigBox, anchor=tk.N)  # anchor=tk.N 决定了把东西放上面，可以换成W看看
            CANVAS.configure(yscrollcommand=scro.set, scrollregion=CANVAS.bbox("all"))
            CANVAS.pack()


            with open(r'data/User Manual.txt', 'r', encoding='utf-8') as f:
                infoV_1_1_0 = f.read()

            tk.Label(bigBox, text="用户手册\nVersion 1.1.0",font=("Arial",18)).pack(padx=10,pady=10)
            tk.Label(bigBox,text=infoV_1_1_0,anchor= tk.W, justify='left',wraplength=380).pack(padx=10)


        menubar = tk.Menu(self.master)

        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label='Save', command=finished)
        filemenu.add_command(label='Exit')

        editmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Help', menu=editmenu)
        editmenu.add_command(label='UserManual', command=UserManual)
        editmenu.add_command(label='About', command=showVersionInfo)

        self.master.config(menu=menubar)

        cnt = 0
        cnt = restore_from_theLastUnfinishedWork()

        frameCCC= tk.Frame(self)
        frameCCC.pack()
        DIV_ = DIV(frameCCC, cnt)
        DIV_.pack()


        # ---------------------------------------------------------
        # 进度条模块
        frameCCC= tk.Frame(self,width=1190,height=40)
        frameCCC.place(x=0, y=0, anchor="nw")
        # frameCCC.propagate(False)

        Pro_Bar_ = Pro_Bar_npnf(frameCCC)
        Pro_Bar_.place(x=0, y=0, anchor="nw")

        # ----------------------------------------------------------
        # 三个按钮模块
        butnnnn = tk.Frame(self)
        butnnnn.place(x=10, y=580, anchor="nw")
        ShangYiWei = tk.Button(butnnnn, text="上一位", font=("黑体", 15), relief=tk.RAISED, width=15, height=2)
        ShangYiWei.pack(side="left")
        ShangYiWei.bind("<Button-1>",lambda e:switch("Previous",ShangYiWei))

        btn_finish = tk.Button(butnnnn, text="完成", font=("黑体", 15), relief=tk.RAISED, width=15, height=2,command=finished)
        btn_finish.pack(side="left",padx=40)

        XiaYiWei = tk.Button(butnnnn, text="下一位", font=("黑体", 15), relief=tk.RAISED, width=15, height=2)
        XiaYiWei.pack(side="left")
        XiaYiWei.bind("<Button-1>",lambda e:switch("Next",XiaYiWei))

        # ----------------------------------------------------------
        # 备注模块
        frame_notes = tk.Frame(self)
        frame_notes.place(x=10, y=340, anchor="nw")

        # 生死备注
        LorD_label = tk.Label(frame_notes, text="生存或死亡（包括准确或模糊的死亡日期，及死亡原因），请务必手打：",font=("黑体",12), justify="left")
        LorD_label.grid(column=0, row=0, sticky="NW")
        scr_deadOrMainInfoRecord = scrolledtext.ScrolledText(frame_notes, font=("华文行楷", 20), width=46, height=2, wrap=tk.WORD)
        scr_deadOrMainInfoRecord.grid(column=0, row=1, sticky="WE", columnspan=1)
        scr_deadOrMainInfoRecord.insert("insert", "")

        # 其他备注
        tk.Label(frame_notes, text="其他想要的备注：",font=("黑体",12), justify="left").grid(column=0, row=2, sticky="NW")
        scr_note = scrolledtext.ScrolledText(frame_notes, font=("", 12), width=60, height=7, wrap=tk.WORD)
        scr_note.grid(column=0, row=3, sticky="WE", columnspan=3)
        scr_note.insert("insert", "")

        # ----------------------------------------------------------
        # 搜索模块
        search = tk.Frame(self)
        search.place(x=10, y=650, anchor="nw")
        tk.Label(search, text="姓名", justify="left",font=("黑体",12)).pack(side='left')
        name_input = tk.Variable()
        tk.Entry(search,textvariable=name_input,width=5,font=("黑体",12)).pack(side='left')
        tk.Label(search, text="住院号", justify="left",font=("黑体",12)).pack(side='left')
        hosId_input = tk.Variable()
        tk.Entry(search, textvariable=hosId_input, width=7,font=("黑体",12)).pack(side='left')
        tk.Button(search, text ="一键搜索",command=searchPat,font=("黑体",12),width=10,relief=tk.RIDGE).pack(side='left',padx=10)

        # 复位到首个未完成的位置
        restore = tk.Frame(self)
        restore.place(x=335, y=650, anchor="nw")
        tk.Button(restore, text ="复位到首个未完成的位置",command=restorationTheWork,font=("黑体",12),width=22,relief=tk.RIDGE).pack(side='left',padx=10)


        content = {"生死备注": ["", scr_deadOrMainInfoRecord],
                   "总备注": ["", scr_note],
                   "完成与否": ["", btn_finish], }
        def read_content():
            # 读取数据库中的内容
            for k in content:
                content[k][0] = ValueInDatabase_read(cnt, k)
                if k != "完成与否":
                    content[k][1].insert("insert", str(content[k][0]))
                else:
                    if content[k][0]!="":
                        content[k][1].config(bg=finished_color,fg="white")
                    else:
                        content[k][1].config(bg="white",fg="black")

        read_content()


class Pro_Bar_npnf(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        # 进度条
        BarStyle_npnf = ttk.Style()
        BarStyle_npnf.theme_use('classic')
        BarStyle_npnf.configure("my0.Horizontal.TProgressbar", troughcolor='white', background='#499c54',thickness=35)

        progressbar = ttk.Progressbar(self, style="my0.Horizontal.TProgressbar", length=200)
        progressbar['maximum'] = len(howManyToFinsh()[0])  # 设置进度条最大值为100
        progressbar['length'] = 1185  # 设置进度条长度
        progressbar['value'] = len(howManyToFinsh()[1])

        progressbar.pack(side='left')
        self.update()

        a = str(len(howManyToFinsh()[0]))
        b = str(len(howManyToFinsh()[1]))
        tk.Label(self.master.master,text=cnt,font=('Arial',12)).place(x=320, y=652, anchor="nw")
        tk.Label(self.master.master,text=b+"/"+a,font=('Arial',12)).place(x=540, y=652, anchor="nw")


class DIV(tk.Frame):
    def __init__(self, master, rowIndex):
        super().__init__(master)
        self.rowIndex = rowIndex

        Frame = tk.Frame(self, bg="#f0f0f0",width=1500, height=800,)
        Frame.pack(side="left", anchor=tk.NW)


        InfoShow(Frame, rowIndex).place(x=5, y=50, anchor="nw")
        # MainInfoRecord(Frame, rowIndex).place(x=600, y=10, anchor="nw")

if __name__ == "__main__":
    app = App()
    app.mainloop()
