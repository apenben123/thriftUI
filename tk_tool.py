#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import tkinter as tk
from tkinter import messagebox


# 检查地址格式
def check_addr(addr) -> bool:
    # 使用正则表达式验证格式
    pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+"
    if not re.match(pattern, addr):
        messagebox.showerror("错误", "无效的地址格式. ip:port")
        return False
    return True

def frame_center(window, Width, Hight):
    '''
        设置窗口居中和宽高
        :param window:主窗体
        :param Width:窗口宽度
        :param Hight:窗口高度
    '''
    # 获取屏幕宽度和高度
    sw = window.winfo_screenwidth()
    sh = window.winfo_screenheight()
    # 计算中心坐标
    cen_x = (sw - Width) / 2
    cen_y = (sh - Hight) / 2
    # 设置窗口大小并居中
    window.geometry('%dx%d+%d+%d' % (Width, Hight, cen_x, cen_y))
    
def add_label_entry(root, text, row, width=35, wraplength=100):
    tk.Label(root, text=text,wraplength=wraplength).grid(row=row, sticky="w")
    entry = tk.Entry(root, width=width, show="")
    entry.grid(row=row, column=1)
    return entry
    
def add_label_entry_with_defaultdata(root, text, row, defaultdata, width=35):
    def on_entry_click(event):
        if entry.get() == defaultdata:
            entry.delete(0, "end")
            entry.config(fg="black")
            
    def on_entry_leave(event):
        if entry.get() == "":
            entry.insert(0, defaultdata)
            entry.config(fg="gray")
            
    tk.Label(root, text=text).grid(row=row, sticky="w")
    entry = tk.Entry(root, width=width)
    entry.bind("<FocusIn>", on_entry_click)
    entry.bind("<FocusOut>", on_entry_leave)
    entry.insert(0, defaultdata)
    entry.config(fg="gray")
    entry.grid(row=row, column=1, padx=10, pady=5)
    return entry
        
def add_label_text(root, text, row, width=35, height=5):
    tk.Label(root, text=text).grid(row=row, sticky="w")
    text_box = tk.Text(root, height=height, width=width)
    text_box.grid(row=row, column=1)
    return text_box

def entry_set_data(entry, data, bReadOnly = True, bClean = True):
    entry.config(state="normal")
    if bClean:
        entry.delete(0, tk.END)  # 先删除现有的数据
    entry.insert(0, data)  # 插入新的数据
    if bReadOnly:
        entry.config(state="readonly")

def text_set_data(text, data, bReadOnly = True, bClean=True):
    text.config(state="normal")
    if bClean:
        text.delete(1.0, tk.END)  # 先删除现有的数据
    text.insert(tk.END, data)  # 插入新的数据
    if bReadOnly:
        text.config(state="disabled")

def text_get_data(text) -> str:
    data = text.get(1.0, tk.END)
    data = data.replace("\n", "")
    return data

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def listbox_get_all_data(listbox):
    num_items = listbox.size()
    all_data = [listbox.get(index) for index in range(num_items)]
    return all_data
