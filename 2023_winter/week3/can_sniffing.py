import os
import can

#os.system('sudo ip link set can0 type can bitrate 100000')
#os.system('sudo ifconfig can0 up') # Enable can0 

bus = can.interface.Bus(channel = 'can0', bustype = 'socketcan')# socketcan_native


while 1:
    message = bus.recv(10.0)
    print("Received message:")
    print("  Arbitration ID:", message.arbitration_id)
    print("  Data:", message.data)
    #print("  DLC:", message.dlc)
    #print("  Extended:", message.extended)
    #print("  Timestamp:", message.timestamp)
    #print (message)
    
    if message is None:
        print('Timeout occurred, no message received.')

    #os.system('sudo ifconfig can0 down')  #Disable can0