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

        KPSAfter3Month(self, cnt).pack()


class KPSAfter3Month(tk.Frame):
    def __init__(self, master, rowIndex):
        super().__init__(master)
        self.rowIndex = rowIndex


        def handlerAdaptor(fun, **kwds):
            """事件处理函数的适配器，相当于中介，进行事件绑定，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧"""
            return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

        def handler(event, cell_name, btn):
            tmp_value = ""      # 尽量别删，谢谢
            cell_value = content[cell_name][0]

            # 默认btn顺位第一是按钮
            def turnGreen():
                btn[0].config(bg="green",fg="white")
            def turnWhite():
                btn[0].config(bg="white",fg="black")

            # ----------------------------------------------
            # 对于普通按钮
            if cell_name[:4] == "btn_":
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

            ScoreCunt()

        def ScoreCunt():
            # print(content)
            # 首先展示分类的情况
            DDD = {"kps1000":[],"kps8090":[],"kps6070":[],"kps3050":[],"kps1020":[]}
            DDD_score = {"kps1000": 0, "kps8090": 0, "kps6070": 0, "kps3050": 0, "kps1020": 0}
            showScore = ""

            # -----------------------------------------
            # 将原始的content转换成上述两个表
            for key in DDD:
                for btname in content:
                    if btname[4:11]==key:
                        DDD[key].append(content[btname][0])
                        if content[btname][0] != "":
                            DDD_score[key]+=1
            # print(DDD)

            # -----------------------------------------
            # 判断10-20分
            if DDD_score["kps1020"]>1:
                showScore="10"
            elif DDD_score["kps1020"]==1:
                showScore = "20"
            else:
                # 判断30-50分
                if DDD_score["kps3050"] >3:
                    showScore = "30"
                elif 1 < DDD_score["kps3050"] <= 3:
                    showScore = "40"
                elif DDD_score["kps3050"] ==1:
                    showScore = "50"
                else:
                    # 判断60-70分
                    if DDD_score["kps6070"] > 2:
                        showScore = "60"
                    elif 0 < DDD_score["kps6070"] <= 2:
                        showScore = "70"
                    else:
                        # 判断80-90分
                        if DDD_score["kps8090"] > 2:
                            showScore = "80"
                        elif 0 < DDD_score["kps8090"] <= 2:
                            showScore = "90"
                        else:
                            if DDD_score["kps1000"] == 1:
                                showScore = "100"
            var_score.set(showScore + "(自动)")
            ValueInDatabase_write(rowIndex, "术后3月KPS评分", showScore)




        Frame = tk.LabelFrame(self,
                              text="术后3月KPS评分",
                              width=220, height=430,
                              font=("黑体", 10),
                              fg="#000000",
                              padx=5, pady=5,
                              labelanchor="nw")
        Frame.pack(side="left", anchor=tk.NW)
        Frame.propagate(False)

        # /////////////////////////////////////////////////////////////////
        F_KPS_ALL = tk.Frame(Frame)
        F_KPS_ALL.pack(anchor=tk.NW)

        # /////////////////////////////////////////////////////////////////
        # 标题行
        F_KPS_title = tk.Frame(F_KPS_ALL)
        F_KPS_title.pack(anchor=tk.NW)
        var_score = tk.StringVar()
        tk.Label(F_KPS_title, text="KPS评分：",font=("黑体", 13)).grid(column=0, row=0, sticky="WE")
        tk.Entry(F_KPS_title, font=("", 15), width=8,textvariable=var_score).grid(column=1, row=0, sticky="WE")
        def var_score_show(*args):
            ValueInDatabase_write(rowIndex, "术后3月KPS评分", var_score.get())
        var_score.trace("w", var_score_show)

        # /////////////////////////////////////////////////////////////////
        # KPS_100
        F_KPS_line100 = tk.Frame(F_KPS_ALL)
        F_KPS_line100.pack(anchor=tk.NW)
        tk.Label(F_KPS_line100, text="正常生活工作，无后遗症(100)").grid(column=0, row=0, sticky="WE")
        kps100 = tk.Button(F_KPS_line100, text="完美")
        kps100.grid(column=1, row=0, sticky="WE")
        kps100.bind("<Button-1>", handlerAdaptor(handler, cell_name="btn_kps1000_完美", btn=[kps100]))

        # /////////////////////////////////////////////////////////////////
        # -----------------------------------------------
        # KPS_80-90
        F_KPS_line8090_t = tk.Frame(F_KPS_ALL)
        F_KPS_line8090_t.pack(anchor=tk.NW)
        tk.Label(F_KPS_line8090_t, text="正常生活工作，有症状和体征(80-90)").grid(column=0, row=0, sticky="WE")

        F_KPS_line8090 = tk.Frame(F_KPS_ALL)
        F_KPS_line8090.pack(anchor=tk.NW)

        kps8090_1 = tk.Button(F_KPS_line8090, text="头痛")
        kps8090_1.grid(column=0, row=0, sticky="WE")
        kps8090_1.bind("<Button-1>", handlerAdaptor(handler, cell_name="btn_kps8090_头痛", btn=[kps8090_1]))

        kps8090_2 = tk.Button(F_KPS_line8090, text="头晕")
        kps8090_2.grid(column=1, row=0, sticky="WE")
        kps8090_2.bind("<Button-1>", handlerAdaptor(handler, cell_name="btn_kps8090_头晕", btn=[kps8090_2]))

        kps8090_3 = tk.Button(F_KPS_line8090, text="记忆")
        kps8090_3.grid(column=2, row=0, sticky="WE")
        kps8090_3.bind("<Button-1>", handlerAdaptor(handler, cell_name="btn_kps8090_记忆", btn=[kps8090_3]))

        kps8090_4 = tk.Button(F_KPS_line8090, text="语言")
        kps8090_4.grid(column=3, row=0, sticky="WE")
        kps8090_4.bind("<Button-1>", handlerAdaptor(handler, cell_name="btn_kps8090_语言", btn=[kps8090_4]))

        kps8090_5 = tk.Button(F_KPS_line8090, text="肢体")
        kps8090_5.grid(column=4, row=0, sticky="WE")
        kps8090_5.bind("<Button-1>", handlerAdaptor(handler, cell_name="btn_kps8090_肢体", btn=[kps8090_5]))

        F_KPS_line8090_other = tk.Frame(F_KPS_ALL)
        F_KPS_line8090_other.pack(anchor=tk.NW)

        # 按钮：其他
        kps8090_other = tk.Button(F_KPS_line8090_other, text="其他")
        kps8090_other.grid(column=0, row=0, sticky="WE")
        # 设置后面输入框的变量
        kps8090_other_var = tk.StringVar()
        # 按钮-其他 后面的输入框
        kps8090_other_entry = tk.Entry(F_KPS_line8090_other, textvariable=kps8090_other_var, width=10)
        kps8090_other_entry["state"] = "disabled"
        kps8090_other_entry.grid(column=1, row=0, sticky="WE")
        # 最后绑定事件
        kps8090_other.bind("<Button-1>", handlerAdaptor(handler, cell_name="ety_kps8090_其他",
                                                        btn=[kps8090_other, kps8090_other_entry, kps8090_other_var]))

        # /////////////////////////////////////////////////////////////////
        # -----------------------------------------------
        # kps60-70
        F_KPS_line6070_t = tk.Frame(F_KPS_ALL)
        F_KPS_line6070_t.pack(anchor=tk.NW)
        tk.Label(F_KPS_line6070_t, text="生活基本能自理，不工作(60-70)").grid(column=0, row=0, sticky="WE")

        F_KPS_line6070 = tk.Frame(F_KPS_ALL)
        F_KPS_line6070.pack(anchor=tk.NW)

        kps6070_1 = tk.Button(F_KPS_line6070, text="偶尔卧床")
        kps6070_1.grid(column=0, row=0, sticky="WE")
        kps6070_1.bind("<Button-1>", handlerAdaptor(handler, cell_name="btn_kps6070_偶尔卧床", btn=[kps6070_1]))

        kps6070_2 = tk.Button(F_KPS_line6070, text="穿衣等偶尔需协助")
        kps6070_2.grid(column=1, row=0, sticky="WE")
        kps6070_2.bind("<Button-1>", handlerAdaptor(handler, cell_name="btn_kps6070_穿衣等偶尔需协助", btn=[kps6070_2]))

        kps6070_3 = tk.Button(F_KPS_line6070, text="癫痫")
        kps6070_3.grid(column=2, row=0, sticky="WE")
        kps6070_3.bind("<Button-1>", handlerAdaptor(handler, cell_name="btn_kps6070_癫痫", btn=[kps6070_3]))

        F_KPS_line6070_other = tk.Frame(F_KPS_ALL)
        F_KPS_line6070_other.pack(anchor=tk.NW)
        # 按钮：其他
        kps6070_other = tk.Button(F_KPS_line6070_other, text="其他")
        kps6070_other.grid(column=1, row=1, sticky="WE")
        # 设置后面输入框的变量
        kps6070_other_var = tk.StringVar()
        # 按钮-其他 后面的输入框
        kps6070_other_entry = tk.Entry(F_KPS_line6070_other, textvariable=kps6070_other_var, width=10)
        kps6070_other_entry["state"] = "disabled"
        kps6070_other_entry.grid(column=2, row=1, sticky="WE")
        # 最后绑定事件
        kps6070_other.bind("<Button-1>", handlerAdaptor(handler, cell_name="ety_kps6070_其他",
                                                        btn=[kps6070_other, kps6070_other_entry, kps6070_other_var]))

        # -----------------------------------------------
        # kps30-50
        F_KPS_line3050_t = tk.Frame(F_KPS_ALL)
        F_KPS_line3050_t.pack(anchor=tk.NW)
        tk.Label(F_KPS_line3050_t, text="必须要人照顾(30-50)").grid(column=0, row=0, sticky="WE")

        F_KPS_line3050 = tk.Frame(F_KPS_ALL)
        F_KPS_line3050.pack(anchor=tk.NW)

        kps3050_1 = tk.Button(F_KPS_line3050, text="基本卧床")
        kps3050_1.grid(column=0, row=0, sticky="WE")
        kps3050_1.bind("<Button-1>", handlerAdaptor(handler, cell_name="btn_kps3050_基本卧床", btn=[kps3050_1]))

        kps3050_2 = tk.Button(F_KPS_line3050, text="无法穿衣洗漱等")
        kps3050_2.grid(column=1, row=0, sticky="WE")
        kps3050_2.bind("<Button-1>", handlerAdaptor(handler, cell_name="btn_kps3050_无法穿衣洗漱等", btn=[kps3050_2]))

        kps3050_3 = tk.Button(F_KPS_line3050, text="大小便障碍")
        kps3050_3.grid(column=0, row=1, sticky="WE")
        kps3050_3.bind("<Button-1>", handlerAdaptor(handler, cell_name="btn_kps3050_大小便障碍", btn=[kps3050_3]))

        kps3050_4 = tk.Button(F_KPS_line3050, text="意识障碍")
        kps3050_4.grid(column=1, row=1, sticky="WE")
        kps3050_4.bind("<Button-1>", handlerAdaptor(handler, cell_name="btn_kps3050_意识障碍", btn=[kps3050_4]))

        # -----------------------------------------------
        # kps10-20
        F_KPS_line1020_t = tk.Frame(F_KPS_ALL)
        F_KPS_line1020_t.pack(anchor=tk.NW)
        tk.Label(F_KPS_line1020_t, text="病危，接近死亡(10-20)").grid(column=0, row=0, sticky="WE")

        F_KPS_line1020 = tk.Frame(F_KPS_ALL)
        F_KPS_line1020.pack(anchor=tk.NW)

        kps1020_1 = tk.Button(F_KPS_line1020, text="医院保守")
        kps1020_1.grid(column=0, row=0, sticky="WE")
        kps1020_1.bind("<Button-1>", handlerAdaptor(handler, cell_name="btn_kps1020_医院保守", btn=[kps1020_1]))

        kps1020_2 = tk.Button(F_KPS_line1020, text="临终关怀机构")
        kps1020_2.grid(column=1, row=0, sticky="WE")
        kps1020_2.bind("<Button-1>", handlerAdaptor(handler, cell_name="btn_kps1020_临终关怀机构", btn=[kps1020_2]))

        kps1020_3 = tk.Button(F_KPS_line1020, text="在家等待")
        kps1020_3.grid(column=2, row=0, sticky="WE")
        kps1020_3.bind("<Button-1>", handlerAdaptor(handler, cell_name="btn_kps1020_在家等待", btn=[kps1020_3]))

        F_KPS_line1020_other = tk.Frame(F_KPS_ALL)
        F_KPS_line1020_other.pack(anchor=tk.NW)
        # 按钮：其他
        kps1020_other = tk.Button(F_KPS_line1020_other, text="其他")
        kps1020_other.grid(column=1, row=1, sticky="WE")
        # 设置后面输入框的变量
        kps1020_other_var = tk.StringVar()
        # 按钮-其他 后面的输入框
        kps1020_other_entry = tk.Entry(F_KPS_line1020_other, textvariable=kps1020_other_var, width=10)
        kps1020_other_entry["state"] = "disabled"
        kps1020_other_entry.grid(column=2, row=1, sticky="WE")
        # 最后绑定事件
        kps1020_other.bind("<Button-1>", handlerAdaptor(handler, cell_name="ety_kps1020_其他",
                                                        btn=[kps1020_other, kps1020_other_entry, kps1020_other_var]))

        # -----------------------------------------------
        # kps0
        F_KPS_line0000_t = tk.Frame(F_KPS_ALL)
        F_KPS_line0000_t.pack(anchor=tk.NW)
        tk.Label(F_KPS_line0000_t, text="死亡(0)").grid(column=0, row=0, sticky="WE")

        content = {"btn_kps1000_完美": ["",kps100],      # 100分
                   "btn_kps8090_头痛": ["",kps8090_1],      # 8090分
                   "btn_kps8090_头晕": ["",kps8090_2],
                   "btn_kps8090_记忆": ["",kps8090_3],
                   "btn_kps8090_语言": ["",kps8090_4],
                   "btn_kps8090_肢体": ["",kps8090_5],
                   "ety_kps8090_其他": ["",kps8090_other,kps8090_other_entry, kps8090_other_var],
                   "btn_kps6070_偶尔卧床": ["",kps6070_1],        # 6070分
                   "btn_kps6070_穿衣等偶尔需协助": ["",kps6070_2],
                   "btn_kps6070_癫痫": ["",kps6070_3],
                   "ety_kps6070_其他": ["",kps6070_other,kps6070_other_entry, kps6070_other_var],
                   "btn_kps3050_基本卧床": ["",kps3050_1],        # 3050分
                   "btn_kps3050_无法穿衣洗漱等": ["",kps3050_2],
                   "btn_kps3050_大小便障碍": ["",kps3050_3],
                   "btn_kps3050_意识障碍": ["",kps3050_4],
                   "btn_kps1020_医院保守": ["",kps1020_1],        # 1020分
                   "btn_kps1020_临终关怀机构": ["",kps1020_2],
                   "btn_kps1020_在家等待": ["",kps1020_3],
                   "ety_kps1020_其他": ["",kps1020_other,kps1020_other_entry, kps1020_other_var]}

        # 读取数据库中的内容，写入Content中
        for k in content:
            content[k][0] = ValueInDatabase_read(rowIndex, k)
        # print(content)
        var_score.set(ValueInDatabase_read(rowIndex, "术后3月KPS评分"))


        def SetDefaultColor():
            """
            :return:，按钮的默认值，包括状态，还有输入框后的内容
            """
            # print(content["btn_kps1000_完美"][1])
            for i in content:
                try:
                    if i[:4]=="btn_":
                        #　如果状态是False，那么按钮变默认颜色白色
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
