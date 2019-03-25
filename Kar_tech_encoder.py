##### Howdy ####

def Kar_tech_encoder(position):
    # identifier is no longer needed. This is defined in the send bus message.
    # position in inches that the actuator should go to

    # initializing 8 byte container
    can_message = ['00', '00', '00', '00', '00', '00', '00', '00']
    # byte 0 and byte 1 will always be these values
    can_message[0] = '0f'
    can_message[1] = '4a'

    # position (inches) multiplied by 1000
    adjusted_position = position * 1000
    # offset defined by Kar Tech Actuator documentation
    offset = 500
    # Value that needs to be turned into hexadecimal
    adjusted_position_with_offset = adjusted_position + offset

    # Changing decimal to hex value
    hex_value = hex(int(adjusted_position_with_offset))
    # Removing '0x' from the start of the hex value
    hex_value_no_0x = hex_value[-3:]

    # Take last two of hex value and set to byte 2
    byte_2_hex = hex_value_no_0x[-2:]
    # Take first letter of hex value and set to byte 3
    byte_3_hex = 'c' + hex_value_no_0x[0]

    # Assigning bytes to the can message
    can_message[2] = byte_2_hex
    can_message[3] = byte_3_hex


    print('identifier: ', identifier)
    print('position: ', position)
    print('can message: ', can_message)

    # Initializing empty container
    send_message = []
    # Looping through bytes in can message and turning into decimal
    for item in can_message:
        item = int(item, 16)
        send_message.append((item))


    print('send message: ', send_message)
    return send_message  # list of integers format -> [00, 00, 00, 00, 00, 00, 00, 00]

Kar_tech_encoder(2)