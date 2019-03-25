import pygame
import can
from can import Message
import os

def command_encoder(position, speed):
    # example command to run: command_encoder(0.29, 0.6), 0.29 rev at 0.6 speed

    # IQ20 conversion
    convert_position = float(position * 2 ** 20)
    convert_speed = float(speed * 2 ** 8)

    # Initializing number of bits for each variable
    position_bits = 32
    speed_bits = 16

    # Conversion of position to hex
    hex_position = hex((int(convert_position) + (1 << position_bits)) % (1 << position_bits))
    while len(hex_position) < 10:
        hex_position = str(hex_position)
        hex_position = hex_position[:2] + '0' + hex_position[2:]

    # Conversion of speed to hex
    hex_speed = hex((int(convert_speed) + (1 << speed_bits)) % (1 << speed_bits))
    while len(hex_speed) < 6:
        hex_speed = str(hex_speed)
        hex_speed = hex_speed[:2] + '0' + hex_speed[2:]

    n = 2

    hex_position = (str(hex_position[2:]))
    holder_position = [hex_position[i:i + n] for i in range(0, len(hex_position), n)]

    hex_speed = (str(hex_speed[2:]))
    holder_speed = [hex_speed[i:i + n] for i in range(0, len(hex_speed), n)]

    command = holder_position[::-1] + holder_speed[::-1]

    test_command = ''.join(command)
    holder_command = [test_command[i:i + n] for i in range(0, len(test_command), n)]

    print(holder_command)

    final_command = []
    for item in holder_command:
        item = int(item, 16)
        final_command.append(item)

    temp_list = [5, 255]
    temp_list.extend(final_command)

    # Create message_send and return it to function caller
    message_send = Message(arbitration_id=419365113, data=temp_list)
    return message_send
