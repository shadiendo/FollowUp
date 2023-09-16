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
        self.attributes("-topmost", 1)

        Treatment(self, cnt).pack()


class Treatment(tk.Frame):
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
                btn[0].config(bg="white", fg="black")

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
                # 如果按钮是关闭状态
                if cell_value == "" and btn[1]["state"] == "disabled":
                    turnGreen()
                    btn[1]["state"] = "normal"  # 开启entry为可输入状态
                    # 将entry写的内容实时传入数据库
                    def show(*args):
                        ValueInDatabase_write(rowIndex, cell_name, btn[2].get())
                    btn[2].trace("w", show)
                    content[cell_name][0] = btn[2].get()  # 修改字典
                # 不管按钮开没开，只要后面的输入框是开启状态的，点击按钮就能关闭，并且触发后续一系列操作
                elif btn[1]["state"] == "normal":
                    turnWhite()
                    btn[1]["state"] = "disabled"
                    btn[2].set("")
                    content[cell_name][0] = ""  # 修改字典
                    ValueInDatabase_write(rowIndex, cell_name, "")  # 修改数据库


        Frame = tk.LabelFrame(self,
                              text="治疗方式",
                              font=("黑体", 10),
                              fg="#000000",
                              width=150, height=210,
                              padx=5, pady=5,
                              labelanchor="nw")
        Frame.pack(side="left", anchor=tk.NW)
        Frame.propagate(False)

        # /////////////////////////////////////////////////////////////////
        Frame_All = tk.Frame(Frame)
        Frame_All.pack(anchor=tk.NW)

        # /////////////////////////////////////////////////////////////////
        # -----------------------------------------------
        # 第一组
        GroupA = tk.Frame(Frame_All)
        GroupA.pack(anchor=tk.NW, pady=5)

        radiotherapy = tk.Button(GroupA, text="   放疗   ")
        radiotherapy.grid(column=0, row=0, sticky="WE")
        radiotherapy.bind("<Button-1>", handlerAdaptor(handler, cell_name="btn_放疗", btn=[radiotherapy]))

        electricFieldTherapy = tk.Button(GroupA, text="电场治疗")
        electricFieldTherapy.grid(column=1, row=0, sticky="WE")
        electricFieldTherapy.bind("<Button-1>", handlerAdaptor(handler, cell_name="btn_电场", btn=[electricFieldTherapy]))


        whereToTreat = tk.Frame(GroupA)
        whereToTreat.grid(column=0, row=1, sticky="WE",columnspan=10)
        # 按钮：其他
        whereToTreat_btn = tk.Button(whereToTreat, text="治疗地点")
        whereToTreat_btn.grid(column=0, row=0, sticky="WE")
        # 设置后面输入框的变量
        whereToTreat_var = tk.StringVar()
        # 按钮-其他 后面的输入框
        whereToTreat_ety = tk.Entry(whereToTreat, textvariable=whereToTreat_var, width=10)
        whereToTreat_ety["state"] = "disabled"
        whereToTreat_ety.grid(column=1, row=0, sticky="WE")
        # 最后绑定事件
        whereToTreat_btn.bind("<Button-1>", handlerAdaptor(handler, cell_name="ety_治疗地点",
                                                        btn=[whereToTreat_btn, whereToTreat_ety, whereToTreat_var]))

        # -----------------------------------------------
        # 中间分隔1
        sep = ttk.Separator(Frame_All, orient=tk.HORIZONTAL, style="red.TSeparator")
        sep.pack(fill=tk.X, padx=5)

        # -----------------------------------------------
        # 第二组
        GroupB = tk.Frame(Frame_All)
        GroupB.pack(anchor=tk.NW, pady=5)

        temozolomide = tk.Button(GroupB, text="替莫唑胺")
        temozolomide.grid(column=0, row=0, sticky="WE")
        temozolomide.bind("<Button-1>", handlerAdaptor(handler, cell_name="btn_替莫唑胺", btn=[temozolomide]))

        PCVplan = tk.Button(GroupB, text="PCV方案")
        PCVplan.grid(column=1, row=0, sticky="WE")
        PCVplan.bind("<Button-1>", handlerAdaptor(handler, cell_name="btn_PCV方案", btn=[PCVplan]))


        targetedDrug = tk.Button(GroupB, text="靶向药")
        targetedDrug.grid(column=0, row=1, sticky="WE")
        # 设置后面输入框的变量
        targetedDrug_var = tk.StringVar()
        # 按钮 后面的输入框
        targetedDrug_ety = tk.Entry(GroupB, textvariable=targetedDrug_var, width=10)
        targetedDrug_ety["state"] = "disabled"
        targetedDrug_ety.grid(column=1, row=1, sticky="WE")
        # 最后绑定事件
        targetedDrug.bind("<Button-1>", handlerAdaptor(handler, cell_name="ety_靶向药",
                                                              btn=[targetedDrug, targetedDrug_ety,
                                                                   targetedDrug_var]))

        # -----------------------------------------------
        # 中间分隔1
        sep = ttk.Separator(Frame_All, orient=tk.HORIZONTAL, style="red.TSeparator")
        sep.pack(fill=tk.X, padx=5)

        # -----------------------------------------------
        # 第三组
        GroupC = tk.Frame(Frame_All)
        GroupC.pack(anchor=tk.NW, pady=5)

        taditionalChineseMedicine = tk.Button(GroupC, text="中药")
        taditionalChineseMedicine.grid(column=1, row=0, sticky="WE")
        taditionalChineseMedicine.bind("<Button-1>", handlerAdaptor(handler, cell_name="btn_中药", btn=[taditionalChineseMedicine]))



        content = {"btn_放疗": ["", radiotherapy],
                   "btn_电场": ["", electricFieldTherapy],
                   "ety_治疗地点": ["", whereToTreat_btn, whereToTreat_ety, whereToTreat_var],
                   "btn_替莫唑胺": ["", temozolomide],
                   "btn_PCV方案": ["", PCVplan],
                   "ety_靶向药": ["", targetedDrug,targetedDrug_ety,targetedDrug_var],
                   "btn_中药": ["", taditionalChineseMedicine]}


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
                        #如果状态是False，那么按钮变默认颜色白色
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
