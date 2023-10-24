# thrift_rpc_test
A tool for testing Thrift RPC functions

### 文件结构

```shell
[root@xxxx bin]# tree
.
├── idl                     // thrift文件目录
├── readme.md               // 说明文档
├── thrift_tool.exe         // 测试工具执行文件
└── UltraCodingSwitch.exe   // 文件编码转换工具, idl目录下的所有thrift文件需要是utf-8编码格式.
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
