##### Howdy ####

def Kar_tech_encoder(identifier, position):
    can_message = ['00', '00', '00', '00', '00', '00', '00', '00']
    can_message[0] = '0f'
    can_message[1] = '4a'

    adjusted_position = position * 1000
    offset = 500
    adjusted_position_with_offset = adjusted_position + offset

    hex_value = hex(int(adjusted_position_with_offset))
    hex_value_no_0x = hex_value[-3:]

    byte_2_hex = hex_value_no_0x[-2:]
    byte_3_hex = 'c' + hex_value_no_0x[0]

    can_message[2] = byte_2_hex
    can_message[3] = byte_3_hex


    print('identifier: ', identifier)
    print('position: ', position)
    print('can message: ', can_message)

    send_message = []

    for item in can_message:
        item = int(item, 16)
        send_message.append((item))


    print('send message: ', send_message)
    return send_message

Kar_tech_encoder('0x00FF0000', 2)