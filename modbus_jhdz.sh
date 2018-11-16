# python3 modbus_jhdz_drive.py -server_ip=192.168.131.107 -server_port=5020
#!/bin/bash
for((i=5020;i<5036;i++)); do
{
   
   echo $i
   # python hehe.py &
   python3 modbus_jhdz_drive.py -server_ip=192.168.131.107 -server_port=$i 
} &
done
