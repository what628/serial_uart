#!/usr/bin/python
# encoding=utf-8

import sys
import time
from enum import Enum

import serial
import serial.tools.list_ports

# micro-defined
__SYS_ARGV_COMM = "COMM="
__SYS_ARGV_COMM_DELETE_STR = "M="

# the specified comm port.
__COMM_PORT = "NULL"
__COMM_BAUDRATE = 921600

__COMM_RECEIVER_TIMEOUT = 3


def sys_exit():
    # 退出
    sys.exit(1)

def comm_port_from_sysArgv():
    # 指定的COM port
    sys_argv_list = sys.argv
    sys_argv_len = len(sys_argv_list)

    __comm_port = "NULL"
    for i in range(sys_argv_len):
        # get the specified COMM port.
        if sys_argv_list[i].find(__SYS_ARGV_COMM) != -1 :
            __comm_port = sys_argv_list[i].replace(__SYS_ARGV_COMM_DELETE_STR, '')
            print("COMM:", __comm_port, "argv:", sys_argv_list[i])
    #    else:
    #        print("请输入正确的串口号(例如：COMM=11)")
    return __comm_port

def comm_port_matched(port):
    # 获取所有串口设备实例。
    # 如果没找到串口设备，则输出：“无串口设备。”
    # 如果找到串口设备，则依次输出每个设备对应的串口号和描述信息。
    ports_list = list(serial.tools.list_ports.comports())
    if len(ports_list) <= 0:
        print("无串口设备。")
    else:
        print("可用的串口设备如下：")
        for comport in ports_list:
            print(list(comport)[0], type(list(comport)[0]), list(comport)[1])
            # check if the specified COMM port exists or not.
            if list(comport)[0] == port :
                return 0
        return -1

    return -2

def comm_port_open(port, baud, to):
    self = serial.Serial(port=port,
                        baudrate=baud,
                        timeout=to)

    if self.isOpen():
        print("打开串口成功。")
        return self

    print("打开串口失败。")
    sys_exit()

def comm_port_close(self):
    self.close()
    if self.isOpen():
        print("串口未关闭。")
    else:
        print("串口已关闭。")

# frame format: 'B'+'E'+'S'+CMD+LEN+PAYLOAD+CHK+'S'+'E'+'B'
# the proccessed frame state.
class COMM_FRAME_PROC_STATE(Enum):
    INIT = 0
    CONNECT = 1
    PARSING = 2
    OTHER = 3

g_comm_frame_proc_stat = COMM_FRAME_PROC_STATE.INIT
def comm_frame_procStat_get():
    return g_comm_frame_proc_stat

def comm_frame_procStat_set(stats):
    global g_comm_frame_proc_stat
    g_comm_frame_proc_stat = stats

def comm_frame_parse(rx_buf):
    print("rx_buf:", rx_buf.decode('UTF-8'), type(rx_buf))
    if comm_frame_procStat_get() == COMM_FRAME_PROC_STATE.PARSING:
        print(comm_frame_procStat_get())
    elif comm_frame_procStat_get() == COMM_FRAME_PROC_STATE.INIT:
        print(comm_frame_procStat_get())
    elif comm_frame_procStat_get() == COMM_FRAME_PROC_STATE.CONNECT:
        print(comm_frame_procStat_get())
    else:
        print(comm_frame_procStat_get())




__COMM_PORT = comm_port_from_sysArgv()
if __COMM_PORT == "NULL" :
    print("请输入正确的串口号(例如：COMM=11)")
    sys_exit()
elif comm_port_matched(__COMM_PORT) == 0:
    print("打开串口：", __COMM_PORT)

    # open the specified comm.
    serialHdl = comm_port_open(__COMM_PORT, __COMM_BAUDRATE, 0.5)
    
    serialHdl.write(b'this is test string\r\n')

    timer_start = time.perf_counter()
    while ( round(time.perf_counter() - timer_start) <= __COMM_RECEIVER_TIMEOUT ):
        len = serialHdl.in_waiting
        if len != 0:
            rx_buf = serialHdl.read_all()
            # 透传transparent transmission
            # print(rx_buf.decode('UTF-8'))
            comm_frame_parse(rx_buf)
            timer_start = time.perf_counter()

    print("RX timeout:", round(time.perf_counter() - timer_start), "S")
    # close the specified comm.
    comm_port_close(serialHdl)





else:
    print("请检查设备端口，然后输入有效的串口号")
    sys_exit()









