# thriftUI

[![Thrift Support](https://img.shields.io/badge/thrift-supported-green)](https://thrift.apache.org/)

ThriftUI 是一个基于 Python 的 Thrift 客户端测试工具，支持通过图形界面快速测试 Thrift 服务端接口。只需提供 `.thrift` 文件，即可动态生成客户端并调用接口。

---

## 特性

- **动态加载 `.thrift` 文件**：无需手动编译 IDL 文件（utf-8），工具会自动解析并生成客户端代码。
- **直观的图形界面**：通过 GUI 界面轻松配置服务地址、端口、方法名及参数。
- **多协议支持**：支持 Thrift 传输协议（TFramedTransport）。
---

## 安装

### 克隆仓库
```bash
git clone https://github.com/apenben123/thriftUI.git
cd thriftUI
```

### 文件结构

```shell
[root@xxxx bin]# tree
.
├── idl                     // thrift文件目录
├── readme.md               // 说明文档
└── thrift_tool.exe         // 测试工具执行文件
```

### 执行方式
1. 先将thrift 文件拷贝到执行文件同目录下的 idl 目录中
2. 使用编码转换器将thrift文件转换成utf-8编码(如果已经是utf-8编码则无需此步骤)
3. 双击执行*thrift_tool.exe*
   - 先选择rpc服务
   - 然后填充服务地址
   - 再选择要测试的rpc接口
   - 填充入参 - 结构体类型需要构建结构体
   - 请求
   - 查看返回

### 其他
1. 暂时不支持入参为嵌套结构体类型
