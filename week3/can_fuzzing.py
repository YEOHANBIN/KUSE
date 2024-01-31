import os
import can
import time
import random

#os.system('sudo ip link set can0 type can bitrate 100000')
#os.system('sudo ifconfig can0 up') # Enable can0 

bus = can.interface.Bus(channel = 'can0', bustype = 'socketcan')# socketcan_native
message = bus.recv(10.0)
ID = message.arbitration_id
n_buf = [0, 0, 0, 0, 0, 0, 0, 0]
while 1:
    for i in range(0,8):
        n = random.randint(0,255)
        n_buf[i] = n
    print(n_buf)

    msg = can.Message(arbitration_id=ID, data=n_buf,is_extended_id=False)
    bus.send(msg)
    time.sleep(1)