#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from Frame_MainInfoRecord import MainInfoRecord
from tools import ValueInDatabase_read, ValueInDatabase_write
from tkinter import scrolledtext

global DIV_,cnt
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        global DIV_,cnt

        cnt = 1

        self.title("KPS_frame")
        # self.geometry("900x700+600+300")
        self.attributes("-topmost", 1)

        InfoShow(self, cnt).pack()


class InfoShow(tk.Frame):
    def __init__(self, master, rowIndex):
        super().__init__(master)
        self.rowIndex = rowIndex

        BasicInfo(self, rowIndex).grid(padx=5, pady=5, row=0, column=0, sticky="nw")
        PathologyInfo(self, rowIndex).grid(padx=5, pady=5, row=1, column=0, sticky="nw")
        ConnectionInfo(self, rowIndex).grid(padx=5, pady=5, row=0, column=1, rowspan=100, sticky="nw")


class BasicInfo(tk.Frame):
    """这是一个 tk.Frame 对象，可以比如 KPSFrame(self).pack() 这么来显示"""

    def on_main_click(self, event):
        print("sub-canvas binding")

    def __init__(self, master, rowIndex):
        super().__init__(master)
        self.rowIndex = rowIndex

        label_options = {"fg": "black", "bg": "#f0f0f0", "font": ("仿宋", 13), "anchor": "w", "justify": "left"}
        grid_options = {"sticky": "NW", "pady": 1, "padx": 2}

        patName_ = str(ValueInDatabase_read(rowIndex, "姓名"))
        gender_ = str(ValueInDatabase_read(rowIndex, "性别"))
        age_ = str(ValueInDatabase_read(rowIndex, "年龄"))
        hospID_ = str(ValueInDatabase_read(rowIndex, "住院号"))

        operationDate_ = str(ValueInDatabase_read(rowIndex, "手术日期"))
        timeInHosp_ = str(ValueInDatabase_read(rowIndex, "住院天数"))
        chiefSurgeon_ = str(ValueInDatabase_read(rowIndex, "主刀医生"))
        conditionOfDischarged_ = str(ValueInDatabase_read(rowIndex, "出院情况"))

        # //////////////////////////////////////////////////////////////////////////////////////////
        # 基本信息栏
        # //////////////////////////////////////////////////////////////////////////////////////////
        FRAME_1_basicInfo = tk.LabelFrame(self,
                                          width=360,
                                          height=135,
                                          padx=5, pady=5,
                                          text="基本信息",
                                          font=("黑体", 12),
                                          fg="#2b2b2b",
                                          labelanchor="nw", )
        FRAME_1_basicInfo.pack()
        FRAME_1_basicInfo.propagate(False)
        # ---------------------------------------------------------

        frame1 = tk.Frame(FRAME_1_basicInfo, bg="#f0f0f0")
        frame1.pack(side="left", anchor=tk.NW)
        tk.Label(frame1, text="姓名：" + patName_,fg="white", bg="#3c3f41", font=("黑体", 13), anchor="w",justify="left").grid(row=1, column=0, **grid_options)
        tk.Label(frame1, text="性别：" + gender_, **label_options).grid(row=2, column=0, **grid_options)
        tk.Label(frame1, text="年龄：" + age_, **label_options).grid(row=3, column=0, **grid_options)
        tk.Label(frame1, text="住院号：" + hospID_, **label_options).grid(row=4, column=0, **grid_options)

        # 中间分隔1
        sep = ttk.Separator(FRAME_1_basicInfo, orient=tk.VERTICAL, style="red.TSeparator")
        sep.pack(side="left", fill=tk.Y, padx=5)

        # 右侧信息栏
        frame2 = tk.Frame(FRAME_1_basicInfo, bg="#f0f0f0")
        frame2.pack(side="left", anchor=tk.NW)
        tk.Label(frame2, text="手术日期：" + operationDate_, **label_options).grid(row=1, column=0, **grid_options)
        tk.Label(frame2, text="住院天数：" + timeInHosp_, **label_options).grid(row=2, column=0, **grid_options)
        tk.Label(frame2, text="主刀医生：" + chiefSurgeon_, **label_options).grid(row=3, column=0, **grid_options)
        tk.Label(frame2, text="出院情况：" + conditionOfDischarged_, **label_options).grid(row=4, column=0,
                                                                                          **grid_options)


class PathologyInfo(tk.Frame):
    def __init__(self, master, rowIndex):
        super().__init__(master)
        self.rowIndex = rowIndex

        label_options = {"fg": "black", "bg": "#f0f0f0", "font": ("仿宋", 13), "anchor": "w", "justify": "left"}
        grid_options = {"sticky": "NW", "pady": 2, "padx": 2}

        disType_ = str(ValueInDatabase_read(rowIndex,"type"))
        pathologyDescribe_ = str(ValueInDatabase_read(rowIndex,"病理描述"))

        FRAME_1_pathologyInfo = tk.LabelFrame(self,
                                              width=360,
                                              height=130,
                                              padx=10, pady=5,
                                              text="病理信息",
                                              font=("黑体", 12),
                                              fg="#2b2b2b",
                                              labelanchor="nw", )
        FRAME_1_pathologyInfo.pack()
        FRAME_1_pathologyInfo.propagate(False)
        # ---------------------------------------------------------

        frame1 = tk.Frame(FRAME_1_pathologyInfo, bg="#f0f0f0")
        frame1.pack(side="left", anchor=tk.NW)
        tk.Label(frame1, text="病种：" + disType_, **label_options).grid(row=1, column=0, **grid_options)
        scrol_w = 40
        scrol_h = 4
        scr = scrolledtext.ScrolledText(frame1, font=("仿宋", 12), width=scrol_w, height=scrol_h, wrap=tk.WORD)
        scr.grid(column=0, row=4, sticky="WE", columnspan=3)
        scr.insert("insert", "【病理描述】：\n" + pathologyDescribe_)


class ConnectionInfo(tk.Frame):
    """这是一个 tk.Frame 对象，可以比如 KPSFrame(self).pack() 这么来显示"""
    def __init__(self, master, rowIndex):
        super().__init__(master)
        self.rowIndex = rowIndex

        global MainInfoRecord_

        label_options = {"fg": "black", "bg": "#f0f0f0", "font": ("仿宋", 13), "anchor": "w", "justify": "left"}
        grid_options = {"sticky": "NW", "pady": 2, "padx": 2}


        whoIsFollowingUp_ = str(ValueInDatabase_read(rowIndex,"随访者"))
        LiveNow_ = str(ValueInDatabase_read(rowIndex,"现住址"))
        phone1_ = str(ValueInDatabase_read(rowIndex,"电话1"))
        phone2_ = str(ValueInDatabase_read(rowIndex,"电话2"))
        phone3_ = str(ValueInDatabase_read(rowIndex,"电话3"))

        FRAME_1_pathologyInfo = tk.LabelFrame(self,
                                              width=200,
                                              height=275,
                                              padx=10, pady=5,
                                              text="随访者：" +whoIsFollowingUp_,
                                              font=("黑体", 12),
                                              fg="#2b2b2b",
                                              labelanchor="nw", )
        FRAME_1_pathologyInfo.pack()
        FRAME_1_pathologyInfo.propagate(False)
        # ---------------------------------------------------------

        frame1 = tk.Frame(FRAME_1_pathologyInfo, bg="#f0f0f0")
        frame1.pack(anchor=tk.NW)

        VarEntry1 = tk.StringVar()
        VarEntry1.set(LiveNow_)
        tk.Label(frame1, text="患者住址：", **label_options).grid(row=0, column=0, **grid_options)
        tk.Entry(frame1, textvariable=VarEntry1,width=23).grid(row=1, column=0, **grid_options)
        tk.Label(frame1, text="患者电话：", **label_options).grid(row=2, column=0, **grid_options)
        tk.Label(frame1, text="  %s\n  %s\n  %s"%(phone1_,phone2_,phone3_), **label_options).grid(row=3, column=0, **grid_options)

        connected_color = "green"
        CannotConnected_color = "#d72323"
        Crashed_color = "#d72323"


        global content
        def connect():
            global MainInfoRecord_,content
            if content["接通状态_接通"][0]=="True":
                content["接通状态_接通"][1].config(bg="#f0f0f0",fg="black")
                content["接通状态_接通"][0] = ""
                ValueInDatabase_write(rowIndex, "接通状态_接通", "")
            else:
                MainInfoRecord_.place(x=600,y=50, anchor="nw")
                content["接通状态_接通"][1].config(bg=connected_color, fg="#ffffff")
                print("接通")
                content["接通状态_接通"][0]="True"
                ValueInDatabase_write(rowIndex,"接通状态_接通","True")

        MainInfoRecord_ = MainInfoRecord(self.master.master,rowIndex)


        def CannotConnect():
            if content["接通状态_不通"][0]!="":
                content["接通状态_不通"][1].config(bg="#f0f0f0",fg="black")
                content["接通状态_不通"][0] = ""
                ValueInDatabase_write(rowIndex, "接通状态_不通", "")
            else:
                content["接通状态_不通"][1].config(bg=CannotConnected_color, fg="white")
                content["接通状态_不通"][0]="True"
                ValueInDatabase_write(rowIndex,"接通状态_不通","True")


                print("无法接通")
                main_toplevel = tk.Toplevel(self)
                winWidth = 500
                winHeight = 400
                screenWidth = self.winfo_screenwidth()  # 1920
                screenHeight = self.winfo_screenheight()  # 1080
                x = int((screenWidth - winWidth) / 2)
                y = int((screenHeight - winHeight) / 2)
                main_toplevel.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
                main_toplevel.overrideredirect(True)  # 取消窗口边框
                main_toplevel.attributes("-topmost", True)  # 为了让注册页面置顶



                def CannotConnect_1():
                    content["接通状态_不通"][0] = "拒接"
                    ValueInDatabase_write(rowIndex, "接通状态_不通", "拒接")
                    QuitCancel()
                def CannotConnect_2():
                    content["接通状态_不通"][0] = "关机"
                    ValueInDatabase_write(rowIndex, "接通状态_不通", "关机")
                    QuitCancel()
                def CannotConnect_3():
                    content["接通状态_不通"][0] = "接者不了解"
                    ValueInDatabase_write(rowIndex, "接通状态_不通", "接者不了解")
                    QuitCancel()
                def CannotConnect_4():
                    content["接通状态_不通"][0] = "拒绝沟通"
                    ValueInDatabase_write(rowIndex, "接通状态_不通", "拒绝沟通")
                    QuitCancel()
                def CannotConnect_5():
                    content["接通状态_不通"][0] = "其他"+str(var_1.get())
                    ValueInDatabase_write(rowIndex, "接通状态_不通", "其他"+str(var_1.get()))
                    QuitCancel()


                def QuitFrame():
                    self.quit()
                    # self.destroy()
                    # self.master.destroy()
                def QuitCancel():
                    # self.quit()
                    main_toplevel.destroy()
                    BC_toplevel.destroy()
                    # self.master.destroy()

                cnt=0


                tk.Label(main_toplevel).pack(pady=15)
                tk.Label(main_toplevel, text="接通失败情况记录", font=("黑体", 25)).pack(pady=0)
                tk.Label(main_toplevel, text="\n假如退不出透明黑屏：1.按alt+F4 2.按win键", font=("黑体", 12)).pack()

                note = tk.Frame(main_toplevel, bg="#f0f0f0")
                note.pack()
                btn_toplevel_CannotConnect = {"fg": "black", "bg": "#ecbb06", "font": ("黑体", 15), "width": 15,"height": 2, "relief": tk.GROOVE}
                grid_toplevel = {"sticky": "NW", "pady": 5, "padx": 5}

                tk.Button(note,text ="拒接", command=CannotConnect_1, **btn_toplevel_CannotConnect).grid(row=0, column=0,**grid_toplevel)
                tk.Button(note,text ="关机", command=CannotConnect_2, **btn_toplevel_CannotConnect).grid(row=0, column=1,**grid_toplevel)
                tk.Button(note,text ="接者不了解", command=CannotConnect_3, **btn_toplevel_CannotConnect).grid(row=1, column=0,**grid_toplevel)
                tk.Button(note,text ="拒绝沟通", command=CannotConnect_4,**btn_toplevel_CannotConnect).grid(row=1, column=1,**grid_toplevel)
                tk.Button(note,text ="其他", command=CannotConnect_5, **btn_toplevel_CannotConnect).grid(row=2, column=0,**grid_toplevel)
                var_1 = tk.Variable()
                tk.Entry(note,width=7,font=("黑体", 25),textvariable=var_1).grid(row=2, column=1,**grid_toplevel)


                # ---------------------------- 先放黑色背景 ------------------------------------
                BC_toplevel = tk.Toplevel(self)
                BC_toplevel.attributes("-alpha", 0.5)  # 设置透明度
                BC_toplevel.overrideredirect(True)  # 取消窗口边框
                BC_toplevel.state("zoomed")  # 最大化
                BC_toplevel.attributes("-topmost", True)  # 是否置顶
                Curtain = tk.Frame(BC_toplevel, bg="black")  # 设置幕布背景为纯黑
                Curtain.pack(fill=tk.BOTH, expand=True)  # 完全填充



        def Crashed():
            if content["接通状态_挂机"][0]!="":
                content["接通状态_挂机"][1].config(bg="#f0f0f0",fg="black")
                content["接通状态_挂机"][0] = ""
                ValueInDatabase_write(rowIndex, "接通状态_挂机", "")
            else:
                content["接通状态_挂机"][1].config(bg=Crashed_color, fg="#ffffff")
                content["接通状态_挂机"][0]="True"
                ValueInDatabase_write(rowIndex,"接通状态_挂机","True")

                print("死机")
                main_toplevel = tk.Toplevel(self)
                winWidth = 500
                winHeight = 400
                screenWidth = self.winfo_screenwidth()  # 1920
                screenHeight = self.winfo_screenheight()  # 1080
                x = int((screenWidth - winWidth) / 2)
                y = int((screenHeight - winHeight) / 2)
                main_toplevel.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
                main_toplevel.overrideredirect(True)  # 取消窗口边框
                main_toplevel.attributes("-topmost", True)  # 为了让注册页面置顶

                def Crashed_1():
                    content["接通状态_挂机"][0] = "停机"
                    ValueInDatabase_write(rowIndex, "接通状态_挂机", "停机")
                    QuitCancel()
                def Crashed_2():
                    content["接通状态_挂机"][0] = "空号"
                    ValueInDatabase_write(rowIndex, "接通状态_挂机", "空号")
                    QuitCancel()
                def Crashed_3():
                    content["接通状态_挂机"][0] = "电话错"
                    ValueInDatabase_write(rowIndex, "接通状态_挂机", "电话错")
                    QuitCancel()
                def Crashed_4():
                    content["接通状态_挂机"][0] = "沟通态度极差"
                    ValueInDatabase_write(rowIndex, "接通状态_挂机", "沟通态度极差")
                    QuitCancel()
                def Crashed_5():
                    content["接通状态_挂机"][0] = "其他"+str(var_2.get())
                    ValueInDatabase_write(rowIndex, "接通状态_挂机", "其他"+str(var_2.get()))
                    QuitCancel()


                def QuitFrame():
                    self.quit()
                    # self.destroy()
                    # self.master.destroy()
                def QuitCancel():
                    # self.quit()
                    main_toplevel.destroy()
                    BC_toplevel.destroy()
                    # self.master.destroy()

                tk.Label(main_toplevel).pack(pady=15)
                tk.Label(main_toplevel, text="标记为失访", font=("黑体", 25)).pack(pady=0)
                tk.Label(main_toplevel, text="\n假如退不出透明黑屏：1.按alt+F4 2.按win键", font=("黑体", 12)).pack()

                note = tk.Frame(main_toplevel, bg="#f0f0f0")
                note.pack()
                btn_toplevel_Crashed = {"fg": "white", "bg": "#c75450", "font": ("黑体", 15), "width": 15,"height": 2, "relief": tk.GROOVE}
                grid_toplevel = {"sticky": "NW", "pady": 5, "padx": 5}
                tk.Button(note,text ="停机", command=Crashed_1, **btn_toplevel_Crashed).grid(row=0, column=0,**grid_toplevel)
                tk.Button(note,text ="空号", command=Crashed_2, **btn_toplevel_Crashed).grid(row=0, column=1,**grid_toplevel)
                tk.Button(note,text ="电话错", command=Crashed_3, **btn_toplevel_Crashed).grid(row=1, column=0,**grid_toplevel)
                tk.Button(note,text ="沟通态度极差", command=Crashed_4,**btn_toplevel_Crashed).grid(row=1, column=1,**grid_toplevel)
                tk.Button(note,text ="其他", command=Crashed_5, **btn_toplevel_Crashed).grid(row=2, column=0,**grid_toplevel)
                var_2 = tk.Variable()
                tk.Entry(note,width=7,font=("黑体", 27),textvariable=var_2).grid(row=2, column=1,**grid_toplevel)

                # ---------------------------- 先放黑色背景 ------------------------------------
                BC_toplevel = tk.Toplevel(self)
                BC_toplevel.attributes("-alpha", 0.5)  # 设置透明度
                BC_toplevel.overrideredirect(True)  # 取消窗口边框
                BC_toplevel.state("zoomed")  # 最大化
                BC_toplevel.attributes("-topmost", True)  # 是否置顶
                Curtain = tk.Frame(BC_toplevel, bg="black")  # 设置幕布背景为纯黑
                Curtain.pack(fill=tk.BOTH, expand=True)  # 完全填充


        frame_btn = tk.Frame(FRAME_1_pathologyInfo, bg="#f0f0f0")
        frame_btn.pack()
        connectState_Y = tk.Button(frame_btn, text="接通", font=("黑体", 15), relief=tk.RAISED, width=15, height=1,command=connect)
        connectState_Y.grid(row=1, column=0)
        connectState_N = tk.Button(frame_btn, text="不通", font=("黑体", 15), relief=tk.RAISED, width=15, height=1,command=CannotConnect)
        connectState_N.grid(row=2, column=0)
        connectState_Die = tk.Button(frame_btn, text="挂机", font=("黑体", 15), relief=tk.RAISED, width=15, height=1,command=Crashed)
        connectState_Die.grid(row=3, column=0)



        content = {"接通状态_接通": ["",connectState_Y],
                   "接通状态_不通": ["",connectState_N],
                   "接通状态_挂机": ["",connectState_Die],}

        # 读取数据库中的内容
        for k in content:
            content[k][0] = ValueInDatabase_read(rowIndex, k)
            # print(str(content[k][0]))

            if str(content[k][0]) != "":
                if k == "接通状态_接通":
                    print("接通满足")
                    content[k][1].config(bg=connected_color, fg="#ffffff")
                    MainInfoRecord_.place(x=600, y=50, anchor="nw")
                elif k == "接通状态_不通":
                    print("不通满足")
                    content[k][1].config(bg=CannotConnected_color, fg="#ffffff")
                elif k == "接通状态_挂机":
                    print("挂机满足")
                    content[k][1].config(bg=Crashed_color, fg="#ffffff")



if __name__ == "__main__":
    app = App()
    app.mainloop()
