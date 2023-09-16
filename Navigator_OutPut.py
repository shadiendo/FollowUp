#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import tkinter as tk
from tkinter import scrolledtext
import pandas as pd
import datetime
from tkinter import filedialog
from tools import messageBoxxx


class UploadPage(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('KPS_frame')
        self.geometry('465x450+100+200')
        self.wm_attributes('-topmost', 1)  # 将当前GUI作为工具窗口
        # self.wm_attributes('-toolwindow', 1)  # 置顶，当前GUI为普通窗口
        self.focus_force()  # 强制聚焦

        def OutputCSV():
            # scr.delete(1.0, tk.END)  # 清空佛祖

            # 判断文件位置
            crentpath = os.path.abspath(os.curdir)  # 获得当前工作目录
            target_path = os.path.join(crentpath,'data','CoreData.pkl')

            if not os.path.exists(target_path):
                scr.insert("end", '🔺警告：工作目录 '+crentpath+' 的data文件夹下不存在 CoreData.pkl文件！\n')
                messageBoxxx(self,'文件不存在?','请查看软件工作目录下的data目录！')
                return

            df = pd.read_pickle(target_path)

            time = datetime.datetime.now().strftime('_%Y%m%d')
            url = filedialog.asksaveasfilename(initialdir=os.getcwd(), defaultextension=".csv",
                                               title="选择导出路径",
                                               initialfile='导出'+time,
                                       filetypes=(("Python Files", "*.csv"), ("All Files", "*.*")))

            df.to_csv(url, index=False, encoding='gb2312')
            scr.insert("insert", '【文件导出成功】\n' + url + '\n')



        LF = tk.LabelFrame(self,text=" 日志 ")
        LF.pack(anchor=tk.E)
        scr = scrolledtext.ScrolledText(LF, width=60, height=28, wrap=tk.WORD)
        scr.see(tk.END)
        scr.pack(padx=10,pady=10)


        # 按钮
        F_titleButton = tk.Frame(self,width=600,height=40)
        F_titleButton.pack()

        btn1 = tk.Button(F_titleButton,
                  text = 'Click Here!',
                  font=('黑体', 17),
                  width=38,height=1,
                  command=OutputCSV,
                  relief=tk.RIDGE)
        btn1.place(relx=.0,rely=.5, anchor="w")
        btn1.config(bg="#2b2b2b", fg="#ecbb06")


        lucky = '''
_ooOoo_
o8888888o
88" . "88
(| -_- |)
 O\ = /O
___/`---'\____
.   ' \\\\| |// `.
/ \\\\||| : |||// \\
/ _||||| -:- |||||- \\
| | \\\\\ - /// | |
| \_| ''\---/'' | |
\ .-\__ `-` ___/-. /
___`. .' /--.--\ `. . __
."" '< `.___\_<|>_/___.' >'"".
| | : `- \`.;`\ _ /`;.`/ - ` : | |
\ \ `-. \_ __\ /__ _/ .-` / /
======`-.____`-.___\_____/___.-`____.-'======
`=---='
.............................................
          佛曰：bug泛滥，我已瘫痪！
'''

        scr.insert("insert",lucky)

if __name__ == "__main__":
    app = UploadPage()
    app.mainloop()
