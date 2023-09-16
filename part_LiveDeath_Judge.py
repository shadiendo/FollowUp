
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import time
from tools import ValueInDatabase_read, ValueInDatabase_write
import datetime


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        global DIV_, cnt

        cnt = 0

        self.title("KPS_frame")
        # self.geometry("900x700+600+300")
        # self.attributes("-topmost", 1)

        LifeOrDeath(self, cnt).pack()


class LifeOrDeath(tk.Frame):
    """这是一个 tk.Frame 对象，可以比如 KPSFrame(self).pack() 这么来显示"""

    def __init__(self, master, rowIndex):
        super().__init__(master)
        self.rowIndex = rowIndex

        c_On = {"bg": "green", "fg": "white"}  # btn_lightUp_color
        c_Off = {"bg": "white", "fg": "black"}  # btn_turnOff_color

        global TimeOfDeath_, TimeOfLive_
        content = {}

        def handlerAdaptor(fun, **kwds):
            """事件处理函数的适配器，相当于中介，进行事件绑定，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧"""
            return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

        def handler(event, cell_name, btn):
            tmp_value = ""  # 尽量别删，谢谢
            cell_value = content[cell_name][0]
            # ----------------------------------------------
            # 进行很重要的逻辑判断，两者之能存在一个
            if cell_name == "btn_生存中" and content["btn_已死亡"][0] != "":
                content["btn_已死亡"][1].config(**c_Off)
                content["btn_已死亡"][0] = ""  # 修改字典
                ValueInDatabase_write(rowIndex, "btn_已死亡", "")  # 修改数据库
            elif cell_name == "btn_已死亡" and content["btn_生存中"][0] != "":
                content["btn_生存中"][1].config(**c_Off)
                content["btn_生存中"][0] = ""  # 修改字典
                ValueInDatabase_write(rowIndex, "btn_生存中", "")  # 修改数据库

            # ----------------------------------------------
            # 对于普通按钮
            if cell_name[:4] != "ety_":
                if cell_value == "":
                    tmp_value = "True"
                    btn[0].config(**c_On)
                elif cell_value == "True":
                    tmp_value = ""
                    btn[0].config(**c_Off)
                else:
                    print("别他妈瞎修改数据库")
                    tmp_value = ""
                    btn[0].config(**c_Off)
                content[cell_name][0] = tmp_value  # 修改字典
                ValueInDatabase_write(rowIndex, cell_name, tmp_value)  # 修改数据库
            # ----------------------------------------------
            # 对于带Entry的按钮
            if cell_name[:4] == "ety_":
                # 如果按钮是关闭状态
                if cell_value == "" and btn[1]["state"] == "disabled":
                    btn[0].config(**c_On)
                    btn[1]["state"] = "normal"  # 开启entry为可输入状态

                    # 将entry写的内容实时传入数据库
                    def show(*args):
                        ValueInDatabase_write(rowIndex, cell_name, btn[2].get())

                    btn[2].trace("w", show)
                    content[cell_name][0] = btn[2].get()  # 修改字典
                # 不管按钮开没开，只要后面的输入框是开启状态的，点击按钮就能关闭，并且触发后续一系列操作
                elif btn[1]["state"] == "normal":
                    btn[0].config(**c_Off)
                    btn[1]["state"] = "disabled"
                    btn[2].set("")
                    content[cell_name][0] = ""  # 修改字典
                    ValueInDatabase_write(rowIndex, cell_name, "")  # 修改数据库

        def thisOneIsAlive():
            global TimeOfLive_
            TimeOfLive_.destroy()
            TimeOfDeath_.destroy()

            TimeOfLive_ = TimeOfLive(FRAME_1_pathologyInfo, rowIndex)
            TimeOfLive_.pack(anchor=tk.NW, side="left")

        def thisOneIsDead():
            global TimeOfDeath_
            TimeOfLive_.destroy()
            TimeOfDeath_.destroy()

            TimeOfDeath_ = TimeOfDeath(FRAME_1_pathologyInfo, rowIndex)
            TimeOfDeath_.pack(anchor=tk.NW, side="left")

        FRAME_1_pathologyInfo = tk.LabelFrame(self,
                                              width=550,
                                              height=135,
                                              padx=0, pady=5,
                                              text="生存情况记录(截至随访日期)",
                                              font=("黑体", 10),
                                              fg="#000000",
                                              labelanchor="nw", )
        FRAME_1_pathologyInfo.pack()
        FRAME_1_pathologyInfo.propagate(False)

        # ---------------------------------------------------------
        frame_general = tk.Frame(FRAME_1_pathologyInfo, bg="#f0f0f0")
        frame_general.pack(anchor=tk.NW, side="left")

        btn_live = tk.Button(frame_general, text="生存", command=thisOneIsAlive, font=("黑体", 15), width=10)
        btn_live.pack(padx=10, pady=10)
        btn_live.bind("<Button-1>", handlerAdaptor(handler, cell_name="btn_生存中", btn=[btn_live]))
        content.update({"btn_生存中": ["", btn_live]})

        btn_dead = tk.Button(frame_general, text="死亡", command=thisOneIsDead, font=("黑体", 15), width=10)
        btn_dead.pack(padx=10, pady=5)
        btn_dead.bind("<Button-1>", handlerAdaptor(handler, cell_name="btn_已死亡", btn=[btn_dead]))
        content.update({"btn_已死亡": ["", btn_dead]})

        # 中间分隔
        sep = ttk.Separator(FRAME_1_pathologyInfo, orient=tk.VERTICAL, style="red.TSeparator")
        sep.pack(side="left", fill=tk.Y, padx=5)

        TimeOfDeath_ = TimeOfDeath(FRAME_1_pathologyInfo, rowIndex)
        TimeOfLive_ = TimeOfLive(FRAME_1_pathologyInfo, rowIndex)

        # 读取数据库中的内容，写入Content中
        for i in content:
            content[i][0] = ValueInDatabase_read(rowIndex, i)

        def SetCondition():
            """
            :return:，按钮的默认值，包括状态，还有输入框后的内容
            """
            for key in content:
                try:
                    if key == "btn_生存中":
                        # 如果状态是False，那么按钮变默认颜色白色
                        if content[key][0] == "":
                            content[key][1].config(**c_Off)
                        # 如果状态是True或其他状态，变绿
                        else:
                            content[key][1].config(**c_On)
                            thisOneIsAlive()

                    if key == "btn_已死亡":
                        # 如果状态是False，那么按钮变默认颜色白色
                        if content[key][0] == "":
                            content[key][1].config(**c_Off)
                        # 如果状态是True或其他状态，变绿
                        else:
                            content[key][1].config(**c_On)
                            thisOneIsDead()

                except:
                    pass

        SetCondition()


        # 创建静态的内容
        content_static = {"【随访日期】": str(time.strftime("%Y-%m-%d"))}
        # 先读，有个好处是可以创建不存在的特征名
        for key in content_static:
            ValueInDatabase_read(rowIndex, key)
        # 写入数据库中
        for i in content_static:
            ValueInDatabase_write(rowIndex, i, str(content_static[i]))


class TimeOfLive(tk.Frame):
    """这是一个 tk.Frame 对象，可以比如 KPSFrame(self).pack() 这么来显示"""
    global fuzzyTime_month_var

    def __init__(self, master, rowIndex):
        super().__init__(master)
        self.rowIndex = rowIndex

        label_options = {"fg": "black", "bg": "#f0f0f0", "font": ("黑体", 15), "anchor": "w", "justify": "left"}
        # ---------------------------------------------------
        # 现在的时间
        localtime = time.localtime(time.time())
        c_year = localtime[0]
        c_month = localtime[1]
        c_day = localtime[2]
        timeNoew = datetime.datetime(c_year, c_month, c_day)
        print(f"今天的日期为：{c_year}年{c_month}月{c_day}日")

        # 手术日期
        operationDate_ = ValueInDatabase_read(0, "手术日期")
        year = int(operationDate_.split("/")[0])
        month = int(operationDate_.split("/")[1])
        day = int(operationDate_.split("/")[2])
        opTime = datetime.datetime(year, month, day)
        print(f"当年病人的手术日期为：{year}年{month}月{day}日")

        # 日期相减获得生存天数
        day2Live = (timeNoew - opTime).days

        # ---------------------------------------------------
        Frame_A = tk.Frame(self, bg="#f0f0f0", width=400, height=100)
        Frame_A.pack()

        tk.Label(Frame_A, text=f"生存至随访日期：{c_year}年{c_month}月{c_day}日", **label_options
                 ).place(x=60, y=10, anchor="nw")

        Frame_down_count = tk.Frame(Frame_A, bg="#f0f0f0")
        Frame_down_count.place(x=60, y=50, anchor="nw")

        tk.Label(Frame_down_count, text="存活时间：", font=("黑体", 20)).pack(side="left")
        var_live = tk.StringVar()
        var_live.set(str(day2Live) + "天")
        tk.Entry(Frame_down_count, width=7, font=("黑体", 20), state="readonly", textvariable=var_live).pack(
            side="left")

        # ---------------------------------------------------
        # 将静态的内容写入数据库中
        content_notBTN = {"【生存时间(准确)】": var_live.get()}
        for i in content_notBTN:
            ValueInDatabase_write(rowIndex, i, str(content_notBTN[i]))


class TimeOfDeath(tk.Frame):
    global date_death_acc, date_death_fuu
    global fuzzyTime_year_var, fuzzyTime_month_var, fuzzyTime_season_var, fuzzyTime_halfyear


    def __init__(self, master, rowIndex):
        global fuzzyTime_month_var, date_death_acc, date_death_fuu

        date_death_acc = ""
        date_death_fuu = ""

        super().__init__(master)
        self.rowIndex = rowIndex

        label_options = {"fg": "black", "bg": "#f0f0f0", "font": ("黑体", 12), "anchor": "w", "justify": "left"}
        content = {}
        def handlerAdaptor(fun, **kwds):
            """事件处理函数的适配器，相当于中介，进行事件绑定，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧"""
            return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

        def handler(event, cell_name,btn):
            # 本链接针对要存储的数据类型为值（不管是entry还是别的）

            # 将entry写的内容实时传入数据库
            def show(*args):
                ValueInDatabase_write(rowIndex, cell_name, btn[0].get())

            btn[1].trace("w", show)
            content[cell_name][0] = btn[1].get()  # 修改字典
            ValueInDatabase_write(rowIndex, cell_name, btn[1].get())  # 修改数据库


        # ///////////////////////////////////////////////////////////////////////////
        # 准确日期记录
        # ///////////////////////////////////////////////////////////////////////////
        Frame_up = tk.Frame(self, bg="#f0f0f0", width=400, height=50)
        Frame_up.pack()

        # --------------------------------------------
        Frame_up_left = tk.Frame(Frame_up, bg="#f0f0f0")
        Frame_up_left.place(x=0, y=0, anchor="nw")

        tk.Label(Frame_up_left, text="死亡日期准确记录：", **label_options).pack(anchor=tk.NW)

        # 根据输入获取手术日期
        def getCurrentOperationTime():
            operationDate_ = ValueInDatabase_read(rowIndex, "手术日期")
            opTime_ = datetime.datetime(int(operationDate_.split("/")[0]), int(operationDate_.split("/")[1]),
                                        int(operationDate_.split("/")[2]))
            return opTime_

        opTime = getCurrentOperationTime()


        def show_accurate(*args):
            global date_death_acc, date_death_fuu
            """
            :param args:
            :return:如果当前输入的时间格式满足要求计算要求，那么讲估分值放入后面的框中
            """
            flag = 0
            try:
                year = accTime_year_var.get()
                month = accTime_month_var.get()
                day = accTime_day_var.get()

                deathTime = datetime.datetime(int(year), int(month), int(day))
                date_death_acc = str(year) + "-" + str(month) + "-" + str(day)

                liveDay = (deathTime - opTime).days
                var_lifeTime.set(str(liveDay) + "天")

                # 更新数据
                content_notBTN["【死亡日期(准确)】"] = str(date_death_acc)
                content_notBTN["【生存时间(准确)】"] = str(liveDay)
                # 写入数据库
                for i in content_notBTN:
                    ValueInDatabase_write(rowIndex, i, content_notBTN[i])

            except:
                flag = 1

            if flag == 1:
                var_lifeTime.set("有误")

        Frame_up_left_c = tk.Frame(Frame_up_left, bg="#f0f0f0")
        Frame_up_left_c.pack(anchor=tk.NW)

        accTime_year_var = tk.StringVar()
        accTime_year_var.trace("w", show_accurate)
        accTime_year_entry = tk.Entry(Frame_up_left_c, width=5, font=("黑体", 14), textvariable=accTime_year_var)
        accTime_year_entry.pack(side="left")
        accTime_year_entry.bind("<Button-1>", handlerAdaptor(handler, cell_name="var_准确死亡_年",btn=[accTime_year_entry,accTime_year_var]))
        tk.Label(Frame_up_left_c, text="年", **label_options).pack(side="left")
        content.update({"var_准确死亡_年": ['',accTime_year_var]})


        accTime_month_var = tk.StringVar()
        accTime_month_var.trace("w", show_accurate)
        accTime_month_entry = tk.Entry(Frame_up_left_c, width=2, font=("黑体", 14), textvariable=accTime_month_var)
        accTime_month_entry.pack(side="left")
        accTime_month_entry.bind("<Button-1>", handlerAdaptor(handler, cell_name="var_准确死亡_月",btn=[accTime_month_entry,accTime_month_var]))
        tk.Label(Frame_up_left_c, text="月", **label_options).pack(side="left")
        content.update({"var_准确死亡_月": ['',accTime_month_var]})

        accTime_day_var = tk.StringVar()
        accTime_day_var.trace("w", show_accurate)
        accTime_day_entry = tk.Entry(Frame_up_left_c, width=2, font=("黑体", 14), textvariable=accTime_day_var)
        accTime_day_entry.pack(side="left")
        accTime_day_entry.bind("<Button-1>", handlerAdaptor(handler, cell_name="var_准确死亡_日",btn=[accTime_day_entry,accTime_day_var]))
        tk.Label(Frame_up_left_c, text="日", **label_options).pack(side="left")
        content.update({"var_准确死亡_日": ['',accTime_day_var]})

        # --------------------------------------------
        # 进行计算
        Frame_up_count = tk.Frame(Frame_up, bg="#f0f0f0")
        Frame_up_count.place(x=310, y=0, anchor="nw")

        tk.Label(Frame_up_count, text="存活(精确)", **label_options).pack()
        var_lifeTime = tk.StringVar()
        tk.Entry(Frame_up_count, width=7, font=("黑体", 14), state="readonly", textvariable=var_lifeTime).pack()

        # ///////////////////////////////////////////////////////////////////////////
        # 中间分隔1
        sep = ttk.Separator(self, orient=tk.HORIZONTAL, style="red.TSeparator")
        sep.pack(fill=tk.X, pady=3)

        # ///////////////////////////////////////////////////////////////////////////
        # 模糊日期记录
        # ///////////////////////////////////////////////////////////////////////////
        Frame_down = tk.Frame(self, bg="#f0f0f0", width=400, height=50)
        Frame_down.pack()

        # --------------------------------------------
        Frame_down_left = tk.Frame(Frame_down, bg="#f0f0f0")
        Frame_down_left.place(x=0, y=0, anchor="nw")

        tk.Label(Frame_down_left, text="死亡日期模糊记录：", **label_options).pack(anchor=tk.NW)

        def show_fuzzy(*args):
            global date_death_acc, date_death_fuu,fuzzyTime_year_var,fuzzyTime_month_var,fuzzyTime_season_var,fuzzyTime_halfyear
            """
            :param args:
            :return:如果当前输入的时间格式满足要求计算要求，那么讲估分值放入后面的框中
            """
            year = 0

            # 先获取年份，根据只有年份的算出时间
            try:
                year = int(fuzzyTime_year_var.get())
                date_death_fuu = year

            # 有问题
            except ValueError:
                var_lifeTime_fuzzy.set("有误")

            # 先获取日期了，没问题就继续运行
            else:
                # ----------------------------------------------------------------------
                # 死亡时间估算为
                # 术后到该年末；如果在手术当年死亡，死亡时间设置为 (年底-手术日期)/2    ；如果在别的年份，设置为6月1号
                if year == opTime.year:
                    # 算出相隔时间
                    liveDay_fuzzy = (datetime.datetime(year, 12, 31) - opTime).days // 2
                    var_lifeTime_fuzzy.set(str(liveDay_fuzzy) + "天")
                else:
                    deathTime = datetime.datetime(year, 6, 1)
                    liveDay_fuzzy = (deathTime - opTime).days
                    var_lifeTime_fuzzy.set(str(liveDay_fuzzy) + "天")

                # ----------------------------------------------------------------------
                # 获取 哪半年，根据哪半年，算出估算
                try:
                    monthDya = [0, 0]
                    date_death_fuu = str(year) + fuzzyTime_halfYear_var.get()
                    if fuzzyTime_halfYear_var.get() == "上半年":
                        monthDya = [3, 1]
                    elif fuzzyTime_halfYear_var.get() == "下半年":
                        monthDya = [9, 1]
                    deathTime = datetime.datetime(year, monthDya[0], monthDya[1])
                    liveDay_fuzzy = (deathTime - opTime).days
                    var_lifeTime_fuzzy.set(str(liveDay_fuzzy) + "天")
                except ValueError:
                    print('哪半年没写')

                # ----------------------------------------------------------------------
                # 获取 季节，如果有就覆盖原来的值
                try:
                    monthDya = [0, 0]
                    date_death_fuu = str(year) + fuzzyTime_season_var.get()
                    if fuzzyTime_season_var.get() == "春":
                        monthDya = [1, 15]
                    elif fuzzyTime_season_var.get() == "夏":
                        monthDya = [4, 15]
                    elif fuzzyTime_season_var.get() == "秋":
                        monthDya = [7, 15]
                    elif fuzzyTime_season_var.get() == "冬":
                        monthDya = [10, 15]
                    deathTime = datetime.datetime(year, monthDya[0], monthDya[1])
                    liveDay_fuzzy = (deathTime - opTime).days
                    var_lifeTime_fuzzy.set(str(liveDay_fuzzy) + "天")
                except ValueError:
                    print('季节没写')

                # ----------------------------------------------------------------------
                # 获取 月份，覆盖强度最大
                try:
                    monthDya = [0, 0]
                    date_death_fuu = str(year) +"年"+ fuzzyTime_month_var.get()
                    if fuzzyTime_month_var.get() != "月份":
                        monthDya = [int(fuzzyTime_month_var.get()[:-1]), 15]
                    deathTime = datetime.datetime(year, monthDya[0], monthDya[1])
                    liveDay_fuzzy = (deathTime - opTime).days
                    var_lifeTime_fuzzy.set(str(liveDay_fuzzy) + "天")
                except ValueError:
                    print('月份没写')

                # 更新数据
                content_notBTN["【死亡日期(模糊)】"] = str(date_death_fuu)
                content_notBTN["【生存时间(模糊)】"] = str(liveDay_fuzzy)
                # 写入数据库
                for k in content_notBTN:
                    ValueInDatabase_write(rowIndex, k, content_notBTN[k])

            # print(f"【模糊日期】年份{year}；{fuzzyTime_halfYear_var.get()}；{fuzzyTime_season_var.get()}；{fuzzyTime_season_var.get()}")



        Frame_down_left_c = tk.Frame(Frame_down_left, bg="#f0f0f0")
        Frame_down_left_c.pack(anchor=tk.NW)


        global fuzzyTime_year_var
        fuzzyTime_year_var = tk.StringVar()
        fuzzyTime_year_var.trace("w", show_fuzzy)
        fuzzyTime_year_entry = tk.Entry(Frame_down_left_c, width=5, font=("黑体", 14), textvariable=fuzzyTime_year_var)
        fuzzyTime_year_entry.pack(side="left")
        fuzzyTime_year_entry.bind("<Button-1>", handlerAdaptor(handler, cell_name="var_模糊死亡_年",btn=[fuzzyTime_year_entry,fuzzyTime_year_var]))
        tk.Label(Frame_down_left_c, text="年", **label_options).pack(side="left")
        content.update({"var_模糊死亡_年": ['',fuzzyTime_year_var]})

        global fuzzyTime_month_var
        fuzzyTime_month_var = tk.StringVar()
        fuzzyTime_month_var.set("月份")
        fuzzyTime_month_var.trace("w", show_fuzzy)
        fuzzyTime_month_cbx = ttk.Combobox(
            Frame_down_left_c,
            width=4,
            state="readonly",
            font=("黑体", 12),
            textvariable=fuzzyTime_month_var,
            values=("none", "1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月",))
        fuzzyTime_month_cbx.pack(side="left")
        fuzzyTime_month_cbx.bind("<Leave>", handlerAdaptor(handler, cell_name="cbx_模糊死亡_月",btn=[fuzzyTime_month_cbx,fuzzyTime_month_var]))
        tk.Label(Frame_down_left_c, text="或").pack(side="left")
        content.update({"cbx_模糊死亡_月": ['',fuzzyTime_month_var]})

        global fuzzyTime_season_var
        fuzzyTime_season_var = tk.StringVar()
        fuzzyTime_season_var.set("季节")
        fuzzyTime_season_var.trace("w", show_fuzzy)
        fuzzyTime_season_cbx = ttk.Combobox(
            Frame_down_left_c,
            width=4,  # 宽度
            state="readonly",
            font=("黑体", 12),
            textvariable=fuzzyTime_season_var,
            values=("none", "春", "夏", "秋", "冬"))
        fuzzyTime_season_cbx.pack(side="left")
        fuzzyTime_season_cbx.bind("<Leave>", handlerAdaptor(handler, cell_name="cbx_模糊死亡_季节",btn=[fuzzyTime_season_cbx,fuzzyTime_season_var]))
        tk.Label(Frame_down_left_c, text="或").pack(side="left")
        content.update({"cbx_模糊死亡_季节": ['',fuzzyTime_season_var]})


        global fuzzyTime_halfYear_var
        fuzzyTime_halfYear_var = tk.StringVar()
        fuzzyTime_halfYear_var.set("哪半年")
        fuzzyTime_halfYear_var.trace("w", show_fuzzy)
        fuzzyTime_halfYear_cbx = ttk.Combobox(
            Frame_down_left_c,
            width=6,  # 宽度
            state="readonly",
            font=("黑体", 12),
            textvariable=fuzzyTime_halfYear_var,
            values=("none", "上半年", "下半年"),)
        fuzzyTime_halfYear_cbx.pack(side="left")
        fuzzyTime_halfYear_cbx.bind("<Leave>", handlerAdaptor(handler, cell_name="cbx_模糊死亡_上下半年",btn=[fuzzyTime_halfYear_cbx,fuzzyTime_halfYear_var]))
        content.update({"cbx_模糊死亡_上下半年": ['',fuzzyTime_halfYear_var]})

        # --------------------------------------------
        # 进行估算
        Frame_down_count = tk.Frame(Frame_down, bg="#f0f0f0")
        Frame_down_count.place(x=310, y=0, anchor="nw")

        tk.Label(Frame_down_count, text="存活(估算)", **label_options).pack()
        var_lifeTime_fuzzy = tk.StringVar()
        tk.Entry(Frame_down_count, width=7, font=("黑体", 14), state="readonly", textvariable=var_lifeTime_fuzzy).pack()

        content_notBTN = {"【死亡日期(准确)】": date_death_acc,
                          "【死亡日期(模糊)】": var_lifeTime.get(),
                          "【生存时间(准确)】": date_death_fuu,
                          "【生存时间(模糊)】": var_lifeTime_fuzzy.get(), }


        # 读取数据库中的内容
        for key in content_notBTN:
            ValueInDatabase_read(rowIndex, key)

        for key in content:
            content[key][0] = ValueInDatabase_read(rowIndex, key)
            content[key][1].set(ValueInDatabase_read(rowIndex, key))


if __name__ == "__main__":
    app = App()
    app.mainloop()
