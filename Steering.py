import can
from can import Message
import os
import time

#os.system('sudo /sbin/ip link set can0 up type can bitrate 250000')
#time.sleep(0.1)
#print('Press CTL-C to exit')

bus = can.interface.Bus(channel='can0', bustype='socketcan_native')

#notifier = can.Notifier(bus, [can.Printer()])

#msg = can.Message(arbitration_id=100, data=[1, 0, 5, 0, 0, 0, 0, 0], extended_id=False)

#print(msg)
#bus.send(msg)

#print('done')
#howdy

#while True:
#    message = str(bus.recv())
#    print(message)



test2 = Message(arbitration_id= 419365113, data=[0, 0, 0, 0, 0, 0, 0, 0])
print(test2)
print(test2.data)
bus.send(test2)
