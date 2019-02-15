import can
import os
import time

#os.system('sudo /sbin/ip link set can0 up type can bitrate 250000')
#time.sleep(0.1)
#print('Press CTL-C to exit')

bus = can.interface.Bus(channel='can0', bustype='socketcan_native')

#notifier = can.Notifier(bus, [can.Printer()])

msg = can.Message(arbitration_id=100, data=bytearray([1, 0, 5, 0, 0, 0, 0, 0]), extended_id=False)

print(msg)
bus.send(msg)

print('done')