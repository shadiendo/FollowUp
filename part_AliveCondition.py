#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
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

        AliveCondition(self, cnt).pack()


class AliveCondition(tk.Frame):
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
                """按钮变绿"""
                btn[0].config(bg="green", fg="white")
            def turnWhite():
                """按钮变白"""
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
                              text="术后发生过的并发症",
                              width=160, height=430,
                              font=("黑体", 10),
                              fg="#000000",
                              padx=5, pady=0,
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
        GroupA.pack(anchor=tk.NW, pady=10)

        # -----------------------------------------------
        GroupA_1 = tk.Frame(GroupA)
        GroupA_1.pack(anchor=tk.NW)
        # 按钮：意识
        consciousness = tk.Button(GroupA_1, text="意识障碍")
        consciousness.grid(column=0, row=0, sticky="WE")
        # 设置后面输入框的变量
        consciousness_var = tk.StringVar()
        # 按钮 后面的输入框
        consciousnessety_ = tk.Entry(GroupA_1, textvariable=consciousness_var, width=10)
        consciousnessety_["state"] = "disabled"
        consciousnessety_.grid(column=1, row=0, sticky="WE")
        # 最后绑定事件
        consciousness.bind("<Button-1>", handlerAdaptor(handler, cell_name="ety_意识障碍",
                                                        btn=[consciousness, consciousnessety_,
                                                             consciousness_var]))

        # -----------------------------------------------
        GroupA_2 = tk.Frame(GroupA)
        GroupA_2.pack(anchor=tk.NW)
        # 按钮：癫痫
        epilepsy = tk.Button(GroupA_2, text="癫痫")
        epilepsy.grid(column=0, row=0, sticky="WE")
        # 设置后面输入框的变量
        epilepsy_var = tk.StringVar()
        # 按钮 后面的输入框
        epilepsyety_ = tk.Entry(GroupA_2, textvariable=epilepsy_var, width=10)
        epilepsyety_["state"] = "disabled"
        epilepsyety_.grid(column=1, row=0, sticky="WE")
        # 最后绑定事件
        epilepsy.bind("<Button-1>", handlerAdaptor(handler, cell_name="ety_癫痫",
                                                   btn=[epilepsy, epilepsyety_,
                                                        epilepsy_var]))

        # -----------------------------------------------
        GroupA_3 = tk.Frame(GroupA)
        GroupA_3.pack(anchor=tk.NW)
        # 按钮：大小便障碍
        DysuriaAndDysporia = tk.Button(GroupA_3, text="大小便障碍")
        DysuriaAndDysporia.grid(column=0, row=0, sticky="WE")
        # 设置后面输入框的变量
        DysuriaAndDysporia_var = tk.StringVar()
        # 按钮 后面的输入框
        DysuriaAndDysporiaety_ = tk.Entry(GroupA_3, textvariable=DysuriaAndDysporia_var, width=10)
        DysuriaAndDysporiaety_["state"] = "disabled"
        DysuriaAndDysporiaety_.grid(column=1, row=0, sticky="WE")
        # 最后绑定事件
        DysuriaAndDysporia.bind("<Button-1>", handlerAdaptor(handler, cell_name="ety_大小便障碍",
                                                             btn=[DysuriaAndDysporia, DysuriaAndDysporiaety_,
                                                                  DysuriaAndDysporia_var]))

        # /////////////////////////////////////////////////////////////////
        # -----------------------------------------------
        # 第二组
        GroupB = tk.Frame(Frame_All)
        GroupB.pack(anchor=tk.NW, pady=10)

        # -----------------------------------------------
        GroupB_1 = tk.Frame(GroupB)
        GroupB_1.pack(anchor=tk.NW)
        # 按钮：肌力下降
        muscleWeakness = tk.Button(GroupB_1, text="肌力下降")
        muscleWeakness.grid(column=0, row=0, sticky="WE")
        # 设置后面输入框的变量
        muscleWeakness_var = tk.StringVar()
        # 按钮 后面的输入框
        muscleWeaknessety_ = tk.Entry(GroupB_1, textvariable=muscleWeakness_var, width=10)
        muscleWeaknessety_["state"] = "disabled"
        muscleWeaknessety_.grid(column=1, row=0, sticky="WE")
        # 最后绑定事件
        muscleWeakness.bind("<Button-1>", handlerAdaptor(handler, cell_name="ety_肌力下降",
                                                         btn=[muscleWeakness, muscleWeaknessety_,
                                                              muscleWeakness_var]))

        # -----------------------------------------------
        GroupB_2 = tk.Frame(GroupB)
        GroupB_2.pack(anchor=tk.NW)
        # 按钮：感觉障碍
        sensoryDisturbance = tk.Button(GroupB_2, text="感觉障碍")
        sensoryDisturbance.grid(column=0, row=0, sticky="WE")
        # 设置后面输入框的变量
        sensoryDisturbance_var = tk.StringVar()
        # 按钮 后面的输入框
        sensoryDisturbanceety_ = tk.Entry(GroupB_2, textvariable=sensoryDisturbance_var, width=10)
        sensoryDisturbanceety_["state"] = "disabled"
        sensoryDisturbanceety_.grid(column=1, row=0, sticky="WE")
        # 最后绑定事件
        sensoryDisturbance.bind("<Button-1>", handlerAdaptor(handler, cell_name="ety_感觉障碍",
                                                             btn=[sensoryDisturbance, sensoryDisturbanceety_,
                                                                  sensoryDisturbance_var]))

        # -----------------------------------------------
        GroupB_3 = tk.Frame(GroupB)
        GroupB_3.pack(anchor=tk.NW)
        # 按钮：走路不稳
        walkUnsteadily = tk.Button(GroupB_3, text="走路不稳")
        walkUnsteadily.grid(column=0, row=0, sticky="WE")
        # 设置后面输入框的变量
        walkUnsteadily_var = tk.StringVar()
        # 按钮 后面的输入框
        walkUnsteadilyety_ = tk.Entry(GroupB_3, textvariable=walkUnsteadily_var, width=10)
        walkUnsteadilyety_["state"] = "disabled"
        walkUnsteadilyety_.grid(column=1, row=0, sticky="WE")
        # 最后绑定事件
        walkUnsteadily.bind("<Button-1>", handlerAdaptor(handler, cell_name="ety_走路不稳",
                                                         btn=[walkUnsteadily, walkUnsteadilyety_,
                                                              walkUnsteadily_var]))

        # /////////////////////////////////////////////////////////////////
        # -----------------------------------------------
        # 第三组
        GroupC = tk.Frame(Frame_All)
        GroupC.pack(anchor=tk.NW, pady=10)

        # -----------------------------------------------
        GroupC_1 = tk.Frame(GroupC)
        GroupC_1.pack(anchor=tk.NW)
        # 按钮：语言障碍
        languageObstacle = tk.Button(GroupC_1, text="语言障碍")
        languageObstacle.grid(column=0, row=0, sticky="WE")
        # 设置后面输入框的变量
        languageObstacle_var = tk.StringVar()
        # 按钮 后面的输入框
        languageObstacleety_ = tk.Entry(GroupC_1, textvariable=languageObstacle_var, width=10)
        languageObstacleety_["state"] = "disabled"
        languageObstacleety_.grid(column=1, row=0, sticky="WE")
        # 最后绑定事件
        languageObstacle.bind("<Button-1>", handlerAdaptor(handler, cell_name="ety_语言障碍",
                                                           btn=[languageObstacle, languageObstacleety_,
                                                                languageObstacle_var]))

        # -----------------------------------------------
        GroupC_2 = tk.Frame(GroupC)
        GroupC_2.pack(anchor=tk.NW)
        # 按钮：视力障碍
        visionDisorder = tk.Button(GroupC_2, text="视力障碍")
        visionDisorder.grid(column=0, row=0, sticky="WE")
        # 设置后面输入框的变量
        visionDisorder_var = tk.StringVar()
        # 按钮 后面的输入框
        visionDisorderety_ = tk.Entry(GroupC_2, textvariable=visionDisorder_var, width=10)
        visionDisorderety_["state"] = "disabled"
        visionDisorderety_.grid(column=1, row=0, sticky="WE")
        # 最后绑定事件
        visionDisorder.bind("<Button-1>", handlerAdaptor(handler, cell_name="ety_视力障碍",
                                                         btn=[visionDisorder, visionDisorderety_,
                                                              visionDisorder_var]))

        # /////////////////////////////////////////////////////////////////
        # -----------------------------------------------
        # 第四组
        GroupD = tk.Frame(Frame_All)
        GroupD.pack(anchor=tk.NW, pady=10)

        # -----------------------------------------------
        GroupD_1 = tk.Frame(GroupD)
        GroupD_1.pack(anchor=tk.NW)
        # 按钮：记忆力下降
        memoryDecline = tk.Button(GroupD_1, text="记忆力下降")
        memoryDecline.grid(column=0, row=0, sticky="WE")
        # 设置后面输入框的变量
        memoryDecline_var = tk.StringVar()
        # 按钮 后面的输入框
        memoryDeclineety_ = tk.Entry(GroupD_1, textvariable=memoryDecline_var, width=10)
        memoryDeclineety_["state"] = "disabled"
        memoryDeclineety_.grid(column=1, row=0, sticky="WE")
        # 最后绑定事件
        memoryDecline.bind("<Button-1>", handlerAdaptor(handler, cell_name="ety_记忆力下降",
                                                        btn=[memoryDecline, memoryDeclineety_,
                                                             memoryDecline_var]))

        # -----------------------------------------------
        GroupD_2 = tk.Frame(GroupD)
        GroupD_2.pack(anchor=tk.NW)
        # 按钮：情绪改变
        emotionalChange = tk.Button(GroupD_2, text="情绪改变")
        emotionalChange.grid(column=0, row=0, sticky="WE")
        # 设置后面输入框的变量
        emotionalChange_var = tk.StringVar()
        # 按钮 后面的输入框
        emotionalChangeety_ = tk.Entry(GroupD_2, textvariable=emotionalChange_var, width=10)
        emotionalChangeety_["state"] = "disabled"
        emotionalChangeety_.grid(column=1, row=0, sticky="WE")
        # 最后绑定事件
        emotionalChange.bind("<Button-1>", handlerAdaptor(handler, cell_name="ety_情绪改变",
                                                          btn=[emotionalChange, emotionalChangeety_,
                                                               emotionalChange_var]))

        # -----------------------------------------------
        GroupD_2 = tk.Frame(GroupD)
        GroupD_2.pack(anchor=tk.NW)
        # 按钮：精神障碍
        mentalDisorder = tk.Button(GroupD_2, text="精神障碍")
        mentalDisorder.grid(column=0, row=0, sticky="WE")
        # 设置后面输入框的变量
        mentalDisorder_var = tk.StringVar()
        # 按钮 后面的输入框
        mentalDisorderety_ = tk.Entry(GroupD_2, textvariable=mentalDisorder_var, width=10)
        mentalDisorderety_["state"] = "disabled"
        mentalDisorderety_.grid(column=1, row=0, sticky="WE")
        # 最后绑定事件
        mentalDisorder.bind("<Button-1>", handlerAdaptor(handler, cell_name="ety_精神障碍",
                                                         btn=[mentalDisorder, mentalDisorderety_,
                                                              mentalDisorder_var]))

        content = {"ety_意识障碍": ["", consciousness, consciousnessety_, consciousness_var],
                   "ety_癫痫": ["", epilepsy, epilepsyety_, epilepsy_var],
                   "ety_大小便障碍": ["", DysuriaAndDysporia, DysuriaAndDysporiaety_, DysuriaAndDysporia_var],
                   "ety_肌力下降": ["", muscleWeakness, muscleWeaknessety_, muscleWeakness_var],
                   "ety_感觉障碍": ["", sensoryDisturbance, sensoryDisturbanceety_, sensoryDisturbance_var],
                   "ety_走路不稳": ["", walkUnsteadily, walkUnsteadilyety_, walkUnsteadily_var],
                   "ety_语言障碍": ["", languageObstacle, languageObstacleety_, languageObstacle_var],
                   "ety_视力障碍": ["", visionDisorder, visionDisorderety_, visionDisorder_var],
                   "ety_记忆力下降": ["", memoryDecline, memoryDeclineety_, memoryDecline_var],
                   "ety_情绪改变": ["", emotionalChange, emotionalChangeety_, emotionalChange_var],
                   "ety_精神障碍": ["", mentalDisorder, mentalDisorderety_, mentalDisorder_var]}

        # 读取数据库中的内容，写入Content中
        for k in content:
            content[k][0] = ValueInDatabase_read(rowIndex, k)

        def SetDefaultColor():
            """
            :return:，按钮的默认值，包括状态，还有输入框后的内容
            """
            # print(content["btn_kps1000_完美"][1])
            for i in content:
                try:
                    if i[:4]=="btn_":
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
