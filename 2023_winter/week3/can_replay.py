import os
import can
import time

#os.system('sudo ip link set can0 type can bitrate 100000')
#os.system('sudo ifconfig can0 up') # Enable can0 

bus = can.interface.Bus(channel = 'can0', bustype = 'socketcan')# socketcan_native

f = open('can_data.txt', 'w')
start = time.time()

while (time.time() - start < 5):
    message = bus.recv(10.0)
    ID = message.arbitration_id
    can_data = message.data
    print("ID: ",ID,"   Data: ",can_data)

    f.write(str(ID))
    f.write(' ')
    con = ' '.join(str(s) for s in can_data)
    f.writelines(con)
    f.write('\n')


    
    #if message is None:
    #    print('Timeout occurred, no message received.')
    #else:
    #    message = can.Message(arbitration_id=ID, data=[9, 9, 9, 9, 9, 9, 9, 9],is_extended_id=False)

    #    bus.send(message)

    #os.system('sudo ifconfig can0 down')  #Disable can0

f.close()