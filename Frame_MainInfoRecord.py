#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from part_LiveDeath_Judge import LifeOrDeath
from part_AliveCondition import AliveCondition
from part_KPSafter3month import KPSAfter3Month
from part_Relapse import Relapse
from part_Treatment import Treatment


global DIV_, cnt

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        global DIV_, cnt

        cnt = 1

        self.title('KPS_frame')
        # self.geometry('900x700+600+300')
        self.attributes("-topmost", 1)

        MainInfoRecord(self, cnt).pack()


class MainInfoRecord(tk.Frame):
    def __init__(self, master, rowIndex):
        super().__init__(master)
        self.rowIndex = rowIndex

        Frame = tk.LabelFrame(self,
                              width=575, height=630,
                              padx=5, pady=5,
                              text="随访信息登记",
                              font=('黑体', 12),
                              fg='#2b2b2b',
                              labelanchor='nw')
        Frame.pack(side='left', anchor=tk.NW)
        Frame.propagate(False)

        LifeOrDeath(Frame, rowIndex).place(x=5, y=5, anchor='nw')

        KPSAfter3Month(Frame, rowIndex).place(x=5, y=160, anchor='nw')
        AliveCondition(Frame, rowIndex).place(x=235, y=160, anchor='nw')
        Treatment(Frame, rowIndex).place(x=405, y=160, anchor='nw')
        Relapse(Frame, rowIndex).place(x=405, y=400, anchor='nw')





if __name__ == "__main__":
    app = App()
    app.mainloop()
