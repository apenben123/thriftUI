#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys

import thriftpy2
from thriftpy2.rpc import make_client
from thriftpy2.transport import TFramedTransportFactory

from app_path import *

# 获取 Thrift 文件所在的目录路径
if getattr(sys, 'frozen', False):
    thrift_dir = os.path.join(app_path(), "idl")
else:
    # 直接运行Python代码
    thrift_dir = get_resource_path("idl")


#基于反射的实现
# 获取目录中的所有 Thrift 文件名
thrift_files = [f for f in os.listdir(thrift_dir) if f.endswith('.thrift')]

thrift_modules = {}

# 遍历每个 Thrift 文件，并使用反射加载它们
for thrift_file in thrift_files:
    # 构建模块名，将文件名中的 '.' 替换为 '_'
    thrift_name = os.path.splitext(thrift_file)[0]
    module_name = thrift_file[:-6].replace('.', '_') + '_thrift'
    # 使用反射加载 Thrift 文件  
    module = thriftpy2.load(os.path.join(thrift_dir, thrift_file), module_name=module_name)
    if thrift_name.endswith('service'):
        thrift_modules[thrift_name] = module


def get_thrift_client(srervice, host, port):
    return make_client(
        srervice, host, port,
        trans_factory=TFramedTransportFactory())