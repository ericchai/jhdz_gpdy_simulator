# jhdz_gpdy_simulator

modbus TCP salve模拟器

此模拟器基于python3,使用pymodbus模块，作用是模拟公司的设备，测试服务器端的采集程序。

使用说明：

1.使用pip安装pymodus模块
  
  pip install pymodbus

2.安装异步服务twisted模块
  
  pip install twisted
  
3.如果只模拟一个设备的话，直接在终端执行下面的命令：后面跟IP地址和端口号
  
  python modbus_jhdz_drive.py -server_ip=192.168.131.9 -server_port=502
  
4.如果是模拟多台设备的话，可以执行modbus_jhdz.sh脚本文件：(在脚本文件里可修改IP地址和开始的端口号和设备的数量)
  
  ./modbus_jhdz.sh
  
