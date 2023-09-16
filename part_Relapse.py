#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tools import ValueInDatabase_read, ValueInDatabase_write

global DIV_, cnt


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        global DIV_, cnt

        cnt = 1

        self.title("KPS_frame")
        # self.geometry("900x700+600+300")
        self.attributes("-topmost", 1)

        Relapse(self, cnt).pack()


class Relapse(tk.Frame):
    def __init__(self, master, rowIndex):
        super().__init__(master)
        self.rowIndex = rowIndex

        def handlerAdaptor(fun, **kwds):
            """事件处理函数的适配器，相当于中介，进行事件绑定，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧"""
            return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

        def handler(event, cell_name, btn):
            tmp_value = ""  # 尽量别删，谢谢
            cell_value = content[cell_name][0]

            # 默认btn顺位第一是按钮
            def turnGreen():
                btn[0].config(bg="green",fg="white")

            def turnWhite():
                btn[0].config(bg="white",fg="black")

            # ----------------------------------------------
            # 对于普通按钮
            if cell_name[:4] != "ety_":
                if cell_value == "":
                    tmp_value = "True"
                    turnGreen()
                elif cell_value == "True":
                    tmp_value = ""
                    turnWhite()
                else:
                    print("别他妈瞎修改数据库")
                    tmp_value = ""
                    turnWhite()
                content[cell_name][0] = tmp_value  # 修改字典
                ValueInDatabase_write(rowIndex, cell_name, tmp_value)  # 修改数据库
            # ----------------------------------------------
            # 对于带Entry的按钮
            if cell_name[:4] == "ety_":
                if cell_value == "":
                    turnGreen()
                    btn[1]["state"] = "normal"  # 开启entry为可输入状态

                    # 将entry写的内容实时传入数据库
                    def show(*args):
                        ValueInDatabase_write(rowIndex, cell_name, btn[2].get())

                    btn[2].trace("w", show)
                    content[cell_name][0] = btn[2].get()  # 修改字典
                else:
                    turnWhite()
                    btn[1]["state"] = "disabled"
                    btn[2].set("")
                    content[cell_name][0] = ""  # 修改字典
                    ValueInDatabase_write(rowIndex, cell_name, "")  # 修改数据库


        Frame = tk.LabelFrame(self,
                              text="复发与接受治疗的情况",
                              font=("黑体", 10),
                              fg="#000000",
                              width=150, height=190,
                              padx=5, pady=5,
                              labelanchor="nw")
        Frame.pack(side="left", anchor=tk.NW)
        Frame.propagate()

        # /////////////////////////////////////////////////////////////////
        Frame_All = tk.Frame(Frame)
        Frame_All.pack(anchor=tk.NW)

        # /////////////////////////////////////////////////////////////////
        # -----------------------------------------------
        # 第一组
        GroupA = tk.Frame(Frame_All)
        GroupA.pack(anchor=tk.NW, pady=5)

        relapse_ = tk.Button(GroupA, text="无复发")
        relapse_.grid(column=0, row=0, sticky="WE")
        relapse_.bind("<Button-1>", handlerAdaptor(handler, cell_name="btn_无复发", btn=[relapse_]))

        # -----------------------------------------------
        # 中间分隔1
        sep = ttk.Separator(Frame_All, orient=tk.HORIZONTAL, style="red.TSeparator")
        sep.pack(fill=tk.X, padx=5)

        # -----------------------------------------------
        # 第二组
        GroupB = tk.Frame(Frame_All)
        GroupB.pack(anchor=tk.NW, pady=5)

        radiologyNotClear = tk.Button(GroupB, text="影像学不确定")
        radiologyNotClear.grid(column=0, row=0, sticky="WE")
        radiologyNotClear.bind("<Button-1>", handlerAdaptor(handler, cell_name="btn_影像学不确定", btn=[radiologyNotClear]))

        # -----------------------------------------------
        # 中间分隔1
        sep = ttk.Separator(Frame_All, orient=tk.HORIZONTAL, style="red.TSeparator")
        sep.pack(fill=tk.X, padx=5)

        # -----------------------------------------------
        # 第三组
        GroupC = tk.Frame(Frame_All)
        GroupC.pack(anchor=tk.NW, pady=5)

        relapse_true = tk.Button(GroupC, text="明确复发未治疗")
        relapse_true.grid(column=0, row=0, sticky="WE")
        relapse_true.bind("<Button-1>", handlerAdaptor(handler, cell_name="btn_明确复发未治疗", btn=[relapse_true]))

        relapse_2rdOperation = tk.Button(GroupC, text="复发后手术(写备注)")
        relapse_2rdOperation.grid(column=0, row=1, sticky="WE")
        relapse_2rdOperation.bind("<Button-1>", handlerAdaptor(handler, cell_name="btn_复发后手术", btn=[relapse_2rdOperation]))



        content = {"btn_无复发": ["", relapse_],
                   "btn_影像学不确定": ["", radiologyNotClear],
                   "btn_明确复发未治疗": ["", relapse_true],
                   "btn_复发后手术": ["", relapse_2rdOperation]}


        # 读取数据库中的内容，写入Content中
        for k in content:
            content[k][0] = ValueInDatabase_read(rowIndex, k)
        # print(content)



        def SetDefaultColor():
            """
            :return:，按钮的默认值，包括状态，还有输入框后的内容
            """
            # print(content["kps_100__完美"][1])
            for i in content:
                try:
                    if i[:4]=="btn_":
                        # 如果状态是，那么按钮变默认颜色白色
                        if content[i][0] =="":
                            content[i][1].config(bg="white",fg="black")
                        # 如果状态是True或其他状态，变绿
                        else:
                            content[i][1].config(bg="green",fg="white")

                    if i[:4]=="ety_":
                        if content[i][0] =="":
                            content[i][1].config(bg="white",fg="black")
                        # 如果状态是True或其他状态，变绿
                        else:
                            content[i][1].config(bg="green",fg="white")
                            content[i][2]["state"] = "normal"  # 开启entry为可输入状态
                            content[i][3].set(ValueInDatabase_read(rowIndex, i))

                except:pass

        SetDefaultColor()


if __name__ == "__main__":
    app = App()
    app.mainloop()
