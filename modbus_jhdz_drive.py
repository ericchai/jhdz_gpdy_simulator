#!/usr/bin/env python
"""
Pymodbus Server With Updating Thread
--------------------------------------------------------------------------

This is an example of having a background thread updating the
context while the server is operating. This can also be done with
a python thread::

    from threading import Thread

    thread = Thread(target=updating_writer, args=(context,))
    thread.start()
"""
# --------------------------------------------------------------------------- #
# import the modbus libraries we need
# --------------------------------------------------------------------------- #
import argparse
from pymodbus.server.async import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer

# --------------------------------------------------------------------------- #
# import the twisted libraries we need
# --------------------------------------------------------------------------- #
from twisted.internet.task import LoopingCall

# --------------------------------------------------------------------------- #
# configure the service logging
# --------------------------------------------------------------------------- #
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)
# --------------------------------------------------------------------------- #
# define your callback process
# --------------------------------------------------------------------------- #


def updating_writer(a):
    """ A worker process that runs every so often and
    updates live values of the context. It should be noted
    that there is a race condition for the update.

    :param arguments: The input arguments to the call
    """
    log.debug("updating the context")
    context = a[0]
    
    slave_id = 0x01
    
    hold_register = 3
    input_register = 4
    coil = 1
    
    #address = 0x10
    
    address = 0x00
    
    # 佳环高频电源modbus-tcp的模拟量输出
    values = context[slave_id].getValues(hold_register, address, count=200)
    values = [v + 1 for v in values]
    log.debug("new values: " + str(values))
    context[slave_id].setValues(hold_register, address, values)
    
    # 模拟佳环高频电源modbus-tcp的开关量输出
    values = context[slave_id].getValues(coil, address, count=200)
    values_new = []
    for v in values:
        if v ==0:
            values_new.append(1)
        else:
            values_new.append(0)
            
    log.debug("new values: " + str(values_new))
    
    context[slave_id].setValues(coil, address, values_new)
    
    # 佳环高频电源modbus-tcp的模拟量输入
    values = context[slave_id].getValues(input_register, address, count=10)
    values = [v + 1 for v in values]
    log.debug("new values: " + str(values))
    context[slave_id].setValues(input_register, address, values)

def run_updating_server():
    # ----------------------------------------------------------------------- # 
    # initialize your data store
    # ----------------------------------------------------------------------- # 
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-server_ip', action='store', dest='server_ip', type=str, help='Input the ip address of modbus server')
    parser.add_argument('-server_port', action='store', dest='server_port', type=int, help='Input the port of modbus server')
    arg = parser.parse_args()
    
    # 模拟佳环高频电源modbus-tcp的开关量输出
    list_co_context=[]
    for i in range(200):   #0000000-000157 一共158点
        
        if i%2 == 0:
            list_co_context.append(0)
        else:
            list_co_context.append(1)
    # 模拟佳环高频电源modbus-tcp的模拟量输入
    list_ir_context=[]
    for i in range(10):
        list_ir_context.append(i+0)

        
    # 模拟佳环高频电源modbus-tcp的模拟量输出
    list_hr_context=[]
    for i in range(200):   #400011-400164 一共154点
        list_hr_context.append(i+0)
       
   
    #store = ModbusSlaveContext(
        #di = ModbusSequentialDataBlock(0, [11]*100),       
        #co = ModbusSequentialDataBlock(0, [12]*100),
        #hr = ModbusSequentialDataBlock(0, [13]*100),
        #ir = ModbusSequentialDataBlock(0, [14]*100))
    
    store = ModbusSlaveContext(
        di = ModbusSequentialDataBlock(0, [0]*100),       
        co = ModbusSequentialDataBlock(0, list_co_context),
        hr = ModbusSequentialDataBlock(0, list_hr_context),
        ir = ModbusSequentialDataBlock(0, list_ir_context))
    
    context = ModbusServerContext(slaves=store, single=True)
    
    
    # ----------------------------------------------------------------------- # 
    # initialize the server information
    # ----------------------------------------------------------------------- # 
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/bashwork/pymodbus/'
    identity.ProductName = 'pymodbus Server'
    identity.ModelName = 'pymodbus Server'
    identity.MajorMinorRevision = '1.0'
    
    # ----------------------------------------------------------------------- # 
    # run the server you want
    # ----------------------------------------------------------------------- # 
    time = 2  # 5 seconds delay
    loop = LoopingCall(f=updating_writer, a=(context,))
    loop.start(time, now=False) # initially delay by time
    #StartTcpServer(context, identity=identity, address=("192.168.168.100", 5021))
    StartTcpServer(context, identity=identity, address=(arg.server_ip, arg.server_port))


if __name__ == "__main__":
    run_updating_server()
