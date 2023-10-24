import tkinter as tk
from functools import partial

from thriftpy2.thrift import TType, parse_spec
from thriftpy2.utils import serialize

from thrift_tool import *
from tk_tool import *


class ThriftObjectViewer:
    def __init__(self, obj):
        self.obj = obj
        # 创建字典用于存储字段值
        self.field_values = {}
        self.root = tk.Tk()
        self.root.title("Object Type: {}".format(self.obj))

    def show_and_build(self, entry):
        row = 0
        # 遍历对象的字段，并根据字段类型创建相应的展示组件
        for id, filed in self.obj.thrift_spec.items():
            f_type = filed[0]
            f_name = filed[1]
            f_vtype = filed[2]
            f_required = filed[3] if len(filed) > 3 else filed[2]

            text = "{}\n({}): ".format(f_name, parse_spec(f_type))

            # 根据字段类型创建相应的展示组件
            if f_type == TType.STRING or f_type == TType.BOOL\
              or f_type == TType.I08 or f_type == TType.I16\
              or f_type == TType.I32 or f_type == TType.I64\
              or f_type == TType.DOUBLE :
                self.field_values[f_name] = add_label_entry(self.root, text, row); row+=1
            elif f_type == TType.LIST or f_type == TType.SET:
                tk.Label(self.root, text=text).grid(row=row, sticky="w")
                attr_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, width=35)
                attr_listbox.grid(row=row, column=1, sticky=tk.W)
                self.field_values[f_name] = attr_listbox
                entry_button_frame = tk.Frame(self.root)
                entry_button_frame.grid(row=row, column=2, sticky=tk.S)
                attr_entry = tk.Entry(entry_button_frame)
                attr_entry.pack(side=tk.LEFT)
                add_button = tk.Button(entry_button_frame, text="添加到列表", width=10, command=lambda lb=attr_listbox, entry=attr_entry: self.add_item(lb, entry))
                add_button.pack(side=tk.LEFT)
                row +=1
        # 创建按钮用于构建新的对象并打印
        tk.Button(self.root, text="确定", width=10, command=partial(self.build_and_get, entry)).grid(row=row, column=1, sticky="w")
        self.root.mainloop()

    def build_and_get(self, entry):
        new_obj = self.obj()
        for id, filed in self.obj.thrift_spec.items():
            f_type = filed[0]
            f_name = filed[1]
            f_vtype = filed[2]
            f_required = filed[3] if len(filed) > 3 else filed[2]

            if f_name in self.field_values.keys():
                field_value = self.field_values[f_name]
                if isinstance(field_value, tk.Entry):
                    data = field_value.get() or ''
                    if f_type == TType.I08 or f_type == TType.I16\
                      or f_type == TType.I32 or f_type == TType.I64:
                        setattr(new_obj, f_name, int(data) if data else 0)
                    elif f_type == TType.DOUBLE:
                        setattr(new_obj, f_name, float(data) if data else 0.0)
                    elif f_type == TType.BOOL:
                        setattr(new_obj, f_name, bool(data) if data else False)
                    elif f_type == TType.STRING:
                        setattr(new_obj, f_name, data)
                elif isinstance(field_value, tk.Listbox):
                    list_value = listbox_get_all_data(field_value)
                    if f_vtype == TType.I08 or f_vtype == TType.I16\
                      or f_vtype == TType.I32 or f_vtype == TType.I64:
                        list_value = [int(item) for item in list_value]
                    elif f_vtype == TType.DOUBLE:
                        list_value = [float(item) for item in list_value]
                    elif f_vtype == TType.BOOL:
                        list_value = [bool(item) for item in list_value]
                    elif f_vtype == TType.STRING:
                        pass
                    if TType.SET == f_type:
                        setattr(new_obj, f_name, set(list_value))
                    elif TType.LIST == f_type:
                        setattr(new_obj, f_name, list_value)
        print(new_obj)
        #关闭页面
        self.root.destroy()
        if entry:
            show = new_obj.__str__()
            show = show[show.find("(")+1:show.rfind(")")]
            print(show)
            data = serialize(new_obj)
            entry_set_data(entry, data)
        return new_obj

    def add_item(self, listbox, entry):
        item = entry.get()
        if item:
            listbox.insert(tk.END, item)
            entry.delete(0, tk.END)

