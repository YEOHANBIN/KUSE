import os
import can
import time

#os.system('sudo ip link set can0 type can bitrate 100000')
#os.system('sudo ifconfig can0 up') # Enable can0 

bus = can.interface.Bus(channel = 'can0', bustype = 'socketcan')# socketcan_native

f = open('can_data.txt', 'r')
can_data = f.readlines()

for i in can_data:
    nList = i.split()
    nList = [int(k) for k in nList]
    print(nList)
    print('ID: ',hex(nList[0]), 'Data: ', nList[1:])
    message = can.Message(arbitration_id=nList[0], data=[nList[t] for t in range(1,9)],is_extended_id=False)

    bus.send(message)





    
    #if message is None:
    #    print('Timeout occurred, no message received.')
    #else:
    #    message = can.Message(arbitration_id=ID, data=[9, 9, 9, 9, 9, 9, 9, 9],is_extended_id=False)

    #    bus.send(message)

    #os.system('sudo ifconfig can0 down')  #Disable can0

f.close()