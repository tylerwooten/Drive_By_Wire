import can
from can import Message
import pygame
import os



#os.system('sudo /sbin/ip link set can0 up type can bitrate 250000')

bus = can.interface.Bus(channel='can0', bustype='socketcan_native')






left = Message(arbitration_id= 419365113, data=[4, 0, 0, 0, 0, 1, 0, 0])
right = Message(arbitration_id= 419365113, data=[4, 0, 0, 0, 0, 0, 0, 0])
print(left)
print(right)

while True:
    ...
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_a]:
       bus.send(left)

    if pressed[pygame.K_d]:
        bus.send(right)

#bus.send(test2)

#while True:
#    message = str(bus.recv())
#    print(message)