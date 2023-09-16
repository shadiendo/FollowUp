#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import scrolledtext
import pandas as pd
from tkinter.filedialog import askopenfile


class ChangeFileFormat(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('文本格式表格转置')
        self.geometry('500x450+100+200')

        Csv2Pkl(self).pack()

class Csv2Pkl(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        def OpenDir_data():
            file_open = askopenfile(mode='r', filetypes=[('TXT Files', '*.txt')])
            save_path = file_open.name[:-4] + '_transRet.txt'

            if file_open is not None:
                scr.insert("end", f'▶▶▶尝试读取文件\n{file_open}')

                # 直接保存
                data = pd.read_table(file_open,sep='\t',index_col=0)
                data.T.to_csv(save_path, sep='\t', index=True, header = True)
                scr.insert("end", '▶▶▶文件格式转换+转移成功\n')

        LF = tk.LabelFrame(self,text=" 日志 ")
        LF.pack(anchor=tk.N,ipadx=10,ipady=5)
        scr = scrolledtext.ScrolledText(LF, width=60, height=25, wrap=tk.WORD)
        scr.see(tk.END)
        scr.pack()

        F_btn = tk.Frame(self)
        F_btn.pack(padx=10,pady=5)
        tk.Button(F_btn,
                  text = '导入',
                  font=('黑体', 13),
                  command= OpenDir_data,
                  width=51,height=2,
                  bg='#9e2927',fg='white',
                  relief=tk.RIDGE).pack()

        tk.Label(self, text='转换器版本v1.0.0 作者邮箱：1390886519@qq.com', font=('', 8)).pack(anchor=tk.N, padx=20, pady=10)


if __name__ == "__main__":
    app = ChangeFileFormat()
    app.mainloop()
