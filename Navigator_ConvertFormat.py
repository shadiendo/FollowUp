#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import shutil
import tkinter as tk
import windnd
from tkinter import scrolledtext
from tkinter import messagebox
import pandas as pd
import datetime
from tkinter.filedialog import askopenfile
from tkinter.filedialog import asksaveasfile


class ChangeFileFormat(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('KPS_frame')
        self.geometry('465x620+100+200')
        # self.wm_attributes('-topmost', 1)  # 将当前GUI作为工具窗口
        self.wm_attributes('-toolwindow', 1)  # 置顶，当前GUI为普通窗口
        self.focus_force()  # 强制聚焦


        global convertFiles
        global Pkl2Csv_
        global Csv2Pkl_

        Pkl2Csv_ = Pkl2Csv(self)
        Csv2Pkl_ = Csv2Pkl(self)

        def start2pkl():
            global convertFiles
            global Pkl2Csv_
            global Csv2Pkl_
            Pkl2Csv_.destroy()
            Csv2Pkl_.destroy()
            convertFiles = []

            Csv2Pkl_ = Csv2Pkl(self)
            Csv2Pkl_.pack()

            btn1.config(bg="#6a8759", fg="white")
            btn2.config(bg="#f0f0f0", fg="black")


        def start2csv():
            global convertFiles
            global Pkl2Csv_
            global Csv2Pkl_
            Pkl2Csv_.destroy()
            Csv2Pkl_.destroy()
            convertFiles = []

            Pkl2Csv_ = Pkl2Csv(self)
            Pkl2Csv_.pack()

            btn1.config(bg="#f0f0f0", fg="black")
            btn2.config(bg="#4487a7", fg="white")

        def OpenDir_data():
            crentpath = os.path.abspath(os.curdir)  # 获得当前工作目录
            os.system("start explorer " + crentpath + '\\data\\')
        tk.Button(self,text='在此打开Data目录',command=OpenDir_data,
                  width=70,height=2,
                  bg = '#434e3c',fg='white',font=('黑体', 10),
                  relief=tk.RAISED).pack()


        # 按钮
        F_titleButton = tk.Frame(self,width=600,height=40)
        F_titleButton.pack()

        btn1 = tk.Button(F_titleButton,
                  text = 'csv → pkl',
                  font=('黑体', 17),
                  command= start2pkl,
                  width=19,height=1,
                  relief=tk.RIDGE)
        btn1.place(relx=.0,rely=.5, anchor="w")


        btn2 = tk.Button(F_titleButton,
                  text = 'pkl → csv',
                  font=('黑体', 17),
                  command= start2csv,
                  width=19,height=1,
                  relief=tk.RIDGE)
        btn2.place(relx=1,rely=.5, anchor="e")


        Csv2Pkl_.pack()
        btn1.config(bg="#6a8759", fg="white")


class Csv2Pkl(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        time = datetime.datetime.now().strftime('_%Y%m%d_%H%M%S')
        cwd_path = os.getcwd()

        def OpenDir_data():
            file_open = askopenfile(mode='r', filetypes=[('CSV Files', '*.csv')])
            file_name =file_open.name

            if file_open is not None:
                scr.insert("end", f'▶▶▶尝试读取文件\n{file_open}')

                df = pd.read_csv(file_open, encoding='gb2312')
                scr.insert("end", '▶▶▶读取csv文件成功\n')
                df.fillna('', inplace=True)

                # 判断是否含有目标的表头
                scr.insert("end", '▶▶▶核验表头\n')
                colNames = df.columns.to_list()
                target = ['随访者', '手术日期', '住院天数', '出院情况', '住院号', '姓名', '性别', '年龄', '现住址',
                          '电话1', '电话2', '电话3', '主刀医生', 'type', '病理描述']
                errorName = []
                for i in target:
                    if i not in colNames:
                        errorName.append(i)
                if len(errorName) > 0:
                    scr.insert("end", '--------------------------------\n警告：你的csv文件第一行里没有如下内容，奉劝你先打开backup文件夹，看一下范例文件！'
                               + str(errorName) + '\n' + '' + '\n')
                    messagebox.showinfo(title='警告', message='你的表头有缺失，详见日志！')
                    return

                scr.insert("end", f'▶▶▶表头核验成功')

                # 下面开始正式转换
                filePath_pkl_new = os.path.join(cwd_path, 'data', 'CoreData.pkl')
                df.to_pickle(filePath_pkl_new)
                scr.insert("end", f'▶▶▶转pkl文件成功')

                # 如果老的CoreData.pkl存在的话，转移到history
                if os.path.exists(filePath_pkl_new):
                    shutil.move(filePath_pkl_new, os.path.join(cwd_path,'data','history', 'CoreData' + time + '.pkl'))
                    scr.insert("end", '▶▶▶老pkl文件转移至 ./data/history 目录下\n')
                else:
                    scr.insert("end", f'▶▶▶表头核验成功')

                # 如果没有老pkl文件，直接转换并保存
                df.to_pickle(filePath_pkl_new)
                scr.insert("end", '▶▶▶②CoreData.pkl已生成在 ./data 目录下\n')
                scr.insert("end", '▶▶▶文件格式转换+转移成功，老文件请到history目录查看\n')


        LF = tk.LabelFrame(self,text=" 日志 ")
        LF.pack(anchor=tk.W)
        scr = scrolledtext.ScrolledText(LF, width=60, height=30, wrap=tk.WORD)
        scr.see(tk.END)
        scr.pack(padx=10,pady=10)

        scr.insert("end", f'▶▶▶当前脚本执行目录为{cwd_path}\n')

        F_btn = tk.Frame(self)
        F_btn.pack(padx=10,pady=10)
        tk.Button(F_btn,
                  text = '导入',
                  font=('黑体', 12),
                  command= OpenDir_data,
                  width=10,height=2,
                  bg='#9e2927',fg='white',
                  relief=tk.RIDGE).pack()


        tk.Label(self, text='note:主程序与CoreData.pkl文件实时交互，为减少报错，不支持excel',font=('', 10)).pack(anchor=tk.N, padx=20,pady=0)
        tk.Label(self, text='转换器版本v1.0.0 作者邮箱：1390886519@qq.com', font=('', 8)).pack(anchor=tk.N, padx=20, pady=0)


class Pkl2Csv(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        cwd_path = os.getcwd()
        data_file_path = os.path.join(cwd_path, 'data', 'CoreData.pkl')
        # df = pd.read_pickle(data_file_path)

        def ExportDir_data():
            file_save = asksaveasfile(filetypes=[('CSV Files', '*.csv')],defaultextension='.csv',initialfile='output')
            if file_save is not None:
                df = pd.read_pickle(data_file_path)
                df.to_csv(file_save, index=False,encoding = 'gb2312')
                scr.insert("insert", '导出成功\n')

                messagebox.showinfo(title='提示', message='导出CSV成功')


        LF = tk.LabelFrame(self,text=" 日志 ")
        LF.pack(anchor=tk.E)
        scr = scrolledtext.ScrolledText(LF, width=60, height=30, wrap=tk.WORD)
        scr.see(tk.END)
        scr.pack(padx=10,pady=10)

        data_file_path = os.path.join(cwd_path, 'data', 'CoreData.pkl')
        if os.path.exists(data_file_path):
            scr.insert("end", f'▶▶▶读取pkl文件成功\n{data_file_path}')
        else:
            messagebox.showinfo(title='警告', message='pkl文件不存在')
            scr.insert("end", f'▶▶▶pkl文件不存在\n{cwd_path}')

        F_btn = tk.Frame(self)
        F_btn.pack(padx=10,pady=10)
        tk.Button(F_btn,
                  text = '导出',
                  font=('黑体', 12),
                  command= ExportDir_data,
                  width=10,height=2,
                  bg='#9e2927',fg='white',
                  relief=tk.RIDGE).pack()

        tk.Label(self, text='转换器版本v1.0.0 作者邮箱：1390886519@qq.com', font=('', 8)).pack(anchor=tk.N, padx=20, pady=0)


if __name__ == "__main__":
    app = ChangeFileFormat()
    app.mainloop()
