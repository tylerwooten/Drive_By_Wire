##### Howdy ####

def command_encoder(identifier, type, position, speed):

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

    print('Position: ', hex_position)

# Conversion of speed to hex
    hex_speed = hex((int(convert_speed) + (1 << speed_bits)) % (1 << speed_bits))
    while len(hex_speed) < 6:
        hex_speed = str(hex_speed)
        hex_speed = hex_speed[:2] + '0' + hex_speed[2:]

    print('Speed: ', hex_speed)

    n = 2

    hex_position = (str(hex_position[2:]))
    holder_position = [hex_position[i:i + n] for i in range(0, len(hex_position), n)]
    print('check:', holder_position)


    hex_speed = (str(hex_speed[2:]))
    holder_speed = [hex_speed[i:i+n] for i in range(0, len(hex_speed), n)]
    print('check:', holder_speed)


    identifier = [identifier, '#', type]

    command = identifier + holder_position[::-1] + holder_speed[::-1]
    final_command = ''.join(command)
    print(final_command)

