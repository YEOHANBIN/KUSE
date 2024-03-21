import os
import can
import time
import random

#os.system('sudo ip link set can0 type can bitrate 100000')
#os.system('sudo ifconfig can0 up') # Enable can0 

bus = can.interface.Bus(channel = 'can0', bustype = 'socketcan')# socketcan_native
message = bus.recv(10.0)
ID = message.arbitration_id
can_data = message.data

while 1:
    for i in range(0,len(can_data)):
        n = random.randint(0,255)
        can_data[i] = n
    print(can_data)

    msg = can.Message(arbitration_id=ID, data=can_data,is_extended_id=False)
    bus.send(msg)
    time.sleep(1)