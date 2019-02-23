import can
from can import Message

#os.system('sudo /sbin/ip link set can0 up type can bitrate 250000')

bus = can.interface.Bus(channel='can0', bustype='socketcan_native')





test2 = Message(arbitration_id= 419365113, data=[0, 0, 0, 0, 0, 0, 0, 0])
print(test2)
print(test2.data)

bus.send(test2)

#while True:
#    message = str(bus.recv())
#    print(message)