#!/usr/bin/python
# -*- coding: UTF-8 -*-

import inspect
import tkinter as tk
from functools import partial
from tkinter import ttk

from thriftpy2.utils import deserialize

from thrift_tool import *
from thriftobj_viewer import *
from tk_tool import *

DEFAULT_RPC_ADDR = "0.0.0.0:8888"

        
class ThriftTool():
    DEFAULT_SRV = '---'

    def __init__(self) -> None:
        self.cur_service    = None
        self.cur_func_name  = ''

        self.root = tk.Tk()
        self.root.title("thrift rpc接口测试")
        self.rowIdx = 0

        def on_thrift_module_service_selection(event):
            thrift_name = self.comboModule.get()
            if thrift_name == self.DEFAULT_SRV:
                return self.clear()

            module = thrift_modules[thrift_name]
            for member_name in dir(module):
                if member_name.endswith("Service") or member_name.endswith("service"):
                    service = getattr(module, member_name)
                    if callable(service):
                        self.cur_service = service
                        self.listboxFunc.delete(0, tk.END)
                        for func in service.thrift_services: 
                            self.listboxFunc.insert(tk.END, func)
                        self.listboxFunc.bind("<<ListboxSelect>>", on_thrift_func_select)

        def on_thrift_func_select(event):
            try:
                clear_frame(self.rpcparams_frame)
                func_name = self.listboxFunc.get(self.listboxFunc.curselection())
                self.cur_func_name = func_name
                row = self.rowIdx
                # 显示函数的参数    
                if self.cur_func_name and self.cur_service:
                    args_name = self.cur_func_name + '_args'
                    args = getattr(self.cur_service, args_name)
                    defalut_args = args.default_spec
                    thrift_args = args.thrift_spec
                    # 创建一个列表
                    req_entries = {}
                    for idx, arg in thrift_args.items():
                        arg_type = arg[0]
                        arg_name = arg[1]
                        item = arg[2]
                        text = f'{arg_name}\n({item.__name__})' if inspect.isclass(item) else f'{arg_name}\n({parse_spec(arg_type)})'
                        entry = add_label_entry(self.rpcparams_frame, text, row+idx)
                        if inspect.isclass(item):
                            entry.config(state="readonly")
                            if item.__name__ != 'ZipkinHeader':
                                obj_btn = tk.Button(self.rpcparams_frame, text=f"构建", width=10, command=partial(self.obj_create, item, entry))
                                obj_btn.grid(row=row+idx, column=2, sticky="w")
                        req_entries[arg_name] = (entry, arg_type, item)
                    row = row + len(thrift_args) + 1
                tk.Label(self.root, text="").grid(row=row+1)
                resp_entry = add_label_text(self.rpcparams_frame, "rpc返回数据", row+1, height=10)
                rpc_btn = tk.Button(self.rpcparams_frame, text="请求", width=35, command=partial(self.rpc_call, req_entries, resp_entry))
                rpc_btn.grid(row=row, column=1, sticky="nwse", padx=10, pady=5)

            except Exception as e:
                print(e)
                self.cur_func_name = ''

        tk.Label(self.root, text='选择rpc服务').grid(row=self.rowIdx, column=0, sticky="w")
        self.comboModule = ttk.Combobox(self.root,width=60)
        self.comboModule['values'] = (self.DEFAULT_SRV,) + tuple(thrift_modules.keys())
        self.comboModule.current(0)
        self.comboModule.grid(row=self.rowIdx, column=1, padx=10, pady=5); self.rowIdx +=1
        self.comboModule.bind('<<ComboboxSelected>>', on_thrift_module_service_selection)

        self.entry_ibsmAddr = add_label_entry_with_defaultdata(self.root, "rpc服务地址", self.rowIdx, DEFAULT_RPC_ADDR, width=60); self.rowIdx +=1
        tk.Label(self.root, text="").grid(row=self.rowIdx); 
        tk.Label(self.root, text="rpc参数列表").grid(row=self.rowIdx, column=2, sticky="w"); self.rowIdx +=1
        # rpc函数列表
        tk.Label(self.root, text='选择rpc函数').grid(row=self.rowIdx, column=0, sticky="w")
        frame = tk.Frame(self.root) # 创建一个Frame作为容器
        frame.grid(row=self.rowIdx, column=1, sticky="nsew")
        scrollbar = ttk.Scrollbar(frame) # 创建一个Scrollbar
        scrollbar.grid(row=self.rowIdx, column=2, sticky="ns")
        self.listboxFunc = tk.Listbox(frame, selectmode=tk.SINGLE, yscrollcommand=scrollbar.set, width=60, height=30, exportselection=False)  # 创建一个Listbox并与Scrollbar关联
        self.listboxFunc.grid(row=self.rowIdx, column=1, padx=10, pady=5, sticky="nsew")
        scrollbar.config(command=self.listboxFunc.yview) # 将Scrollbar与Listbox关联

        # rpc函数参数列表
        self.rpcparams_frame = tk.Frame(self.root)
        self.rpcparams_frame.grid(row=self.rowIdx, column=2, sticky="nsew")

    def run(self):
        frame_center(self.root, 1010, 660)
        #self.root.resizable(0,0) #固定窗体
        # 开启事件主循环
        self.root.mainloop()

    def get_client(self, service):
        try:
            addr = self.entry_ibsmAddr.get()
            # 先检查ibsm地址
            if check_addr(addr):
                return get_thrift_client(service or self.cur_service, host=addr.split(':')[0], port=int(addr.split(':')[1]))
        except Exception as e:
            tk.messagebox.showerror(title="Error", message=str(e))
        return None

    def obj_create(self, obj, entry):
        viewer = ThriftObjectViewer(obj)
        obj_ins = viewer.show_and_build(entry)

    def rpc_call(self, entries, resp_entry):

        client = self.get_client(self.cur_service)
        func = getattr(client, self.cur_func_name)
        params = {}
        for name, item in entries.items():
            entry = item[0]
            ktype = item[1]
            data = entry.get()
            if ktype == TType.STRUCT:
                obj_cls = item[2]
                if obj_cls and data:
                    obj = obj_cls()
                    deserialize(obj, data.encode())
                    params[name] = obj
            elif ktype == TType.I08 or ktype == TType.I16 or ktype == TType.I32 or ktype == TType.I64:
                params[name] = int(data) if data else 0
            elif ktype == TType.DOUBLE:
                params[name] = float(data) if data else 0.0
            elif ktype == TType.BOOL:
                params[name] = bool(data) if data else False
            elif ktype == TType.STRING:
                params[name] = data
            else:
                params[name] = eval(data) if data else None
                
        resp = func(**params)
        text_set_data(resp_entry, resp)
        print(resp)

    def clear(self):
        self.cur_service    = None
        self.cur_func_name  = ''
        
        self.listboxFunc.delete(0, tk.END)
        clear_frame(self.rpcparams_frame)

        
    
if __name__ == '__main__':
    ThriftTool().run()
