import os
import can
import time

#os.system('sudo ip link set can0 type can bitrate 100000')
#os.system('sudo ifconfig can0 up') # Enable can0 

bus = can.interface.Bus(channel = 'can0', bustype = 'socketcan')# socketcan_native
message = bus.recv(10.0)
ID = message.arbitration_id

while 1:
    msg = can.Message(arbitration_id=ID, data=[9, 9, 9, 9, 9, 9, 9, 9],is_extended_id=False)
    bus.send(msg)
    time.sleep(0.01)