import pygame
import can
from can import Message
import os

#os.system('sudo /sbin/ip link set can0 up type can bitrate 250000')
bus = can.interface.Bus(channel='can0', bustype='socketcan_native')

#Define all messages to be sent
#Left1 = Message(arbitration_id= 419365113, data=[3, 255, 255, 255, 255, 241, 0, 0])
#Left2 = Message(arbitration_id= 419365113, data=[3, 255, 255, 255, 255, 243, 0, 0])
#Left3 = Message(arbitration_id= 419365113, data=[3, 255, 255, 255, 255, 245, 0, 0])
#Right1 = Message(arbitration_id= 419365113, data=[3, 0, 0, 0, 0, 1, 0, 0])
#Right2 = Message(arbitration_id= 419365113, data=[3, 0, 0, 0, 0, 3, 0, 0])
#Right3 = Message(arbitration_id= 419365113, data=[3, 0, 0, 0, 0, 5, 0, 0])
StopAll = Message(arbitration_id= 419365113, data=[0, 0, 0, 0, 0, 0, 0, 0])

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.

#------------------------------- START COMMAND ENCODER FUNCTION ----------------------------------------#

def command_encoder(identifier, type, position, speed):
    # example command to run: command_encoder('18FF00F9', '05ff', 0.29, 0.6), 0.29 rev at 0.6 speed

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

    #print('Position: ', hex_position)

    # Conversion of speed to hex
    hex_speed = hex((int(convert_speed) + (1 << speed_bits)) % (1 << speed_bits))
    while len(hex_speed) < 6:
        hex_speed = str(hex_speed)
        hex_speed = hex_speed[:2] + '0' + hex_speed[2:]

    #print('Speed: ', hex_speed)

    n = 2

    hex_position = (str(hex_position[2:]))
    holder_position = [hex_position[i:i + n] for i in range(0, len(hex_position), n)]
    #print('check:', holder_position)


    hex_speed = (str(hex_speed[2:]))
    holder_speed = [hex_speed[i:i+n] for i in range(0, len(hex_speed), n)]
    #print('check:', holder_speed)


    identifier = [identifier, '#', type]

    command = holder_position[::-1] + holder_speed[::-1]
    final_command = ''.join(command)
    holder_command = [final_command[i:i + n] for i in range(0, len(final_command), n)]  #reformatted to data input for this script
    #print(holder_command)

    message_send = Message(arbitration_id= 419365113, data= holder_command)
    return message_send

#-----------------------------------START XBOX CONTROLLER SECTION -----------------------------------------------#

class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def printtext(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10

pygame.init()

# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Drive By Wire")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

# Get ready to print
textPrint = TextPrint()

# -------- Main Program Loop -----------
while done == False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            printtext("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            printtext("Joystick button released.")

    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    textPrint.printtext(screen, "Number of joysticks: {}".format(joystick_count))
    textPrint.indent()

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        textPrint.printtext(screen, "Joystick {}".format(i))
        textPrint.indent()

        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        textPrint.printtext(screen, "Joystick name: {}".format(name))

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.printtext(screen, "Number of axes: {}".format(axes))
        textPrint.indent()

        for i in range(axes):
            axis = joystick.get_axis(i)
            textPrint.printtext(screen, "Axis {} value: {:>6.3f}".format(i, axis))
        textPrint.unindent()

        ################ ----------------So begins my choppy code--------------------- ######################
        axis0 = joystick.get_axis(0) # Left knob, left (-1) and right (1)
        axis1 = joystick.get_axis(1) # Left knob, up (-1) and down (1)
        axis2 = joystick.get_axis(2) # Triggers, Left (1) Right (-1)

        mode = 1

        # Stops turning section
        if -0.15 < axis0 < 0.15:
            bus.send(StopAll)
            print("not moving\n")

        else:
            #recommend adding on a limit multiplier/divider of axis 0 so we can expand or contract the max/min turn amount
            message_send = command_encoder('18FF00F9', '05ff', axis0, mode)  # axis 0 updated -1 to 1 and changes the position. mode is the speed mode and can be updated by pressing the buttons
            bus.send(message_send)

        # Turning right section
        # if 0.15 < axis0 < 0.3:
        #     #message_send = command_encoder('18FF00F9', '05ff', 0.5, 2)
        #     message_send = Message(arbitration_id=419365113, data=[5, 255, 0, 0, 4, 0, 19, 0])
        #     bus.send(message_send)
        #     print("Right 1\n")
        #
        # if 0.3 < axis0 < 0.6:
        #     #message_send = command_encoder('18FF00F9', '05ff', 0.5, 5)
        #     message_send = Message(arbitration_id=419365113, data=[5, 255, 0, 0, 4, 0, 80, 0])
        #     bus.send(message_send)
        #     print("Right 2\n")
        #
        # if 0.6 < axis0 <= 1.00:
        #     #message_send = command_encoder('18FF00F9', '05ff', 0.5, 10)
        #     message_send = Message(arbitration_id=419365113, data=[5, 255, 0, 0, 4, 0, 0, 1])
        #     bus.send(message_send)
        #     print("Right 3\n")
        #
        # # Turning Left section
        # if -0.15 > axis0 > -0.3:
        #     #message_send = command_encoder('18FF00F9', '05ff', -0.5, 2)
        #     message_send = Message(arbitration_id=419365113, data=[5, 255, 0, 0, 252, 255, 19, 0])
        #     bus.send(message_send)
        #     print("Left 1\n")
        #
        # if -0.3 > axis0 > -0.6:
        #     #message_send = command_encoder('18FF00F9', '05ff', -0.5, 5)
        #     message_send = Message(arbitration_id=419365113, data=[5, 255, 0, 0, 252, 255, 80, 0])
        #     bus.send(message_send)
        #     print("Left 2\n")
        #
        # if -0.6 > axis0 >= -1.00:
        #     #message_send = command_encoder('18FF00F9', '05ff', -0.5, 10)
        #     message_send = Message(arbitration_id= 419365113, data=[5, 255, 0, 0, 252, 255, 0, 1])
        #     bus.send(message_send)
        #     print("Left 3\n")

        ############### ADD IN SENDING CAN SIGNAL HERE

        #### ADDING BUTTON FUNCTIONALITY
        # buttons = joystick.get_numbuttons()
        # textPrint.print(screen, "Number of buttons: {}".format(buttons))
        # textPrint.indent()
        #
        # for i in range(buttons):
        #     button = joystick.get_button(i)
        #     textPrint.print(screen, "Button {:>2} value: {}".format(i, button))
        # textPrint.unindent()
        #
        # # Hat switch. All or nothing for direction, not like joysticks.
        # # Value comes back in an array.
        # hats = joystick.get_numhats()
        # textPrint.print(screen, "Number of hats: {}".format(hats))
        # textPrint.indent()
        #
        # for i in range(hats):
        #     hat = joystick.get_hat(i)
        #     textPrint.print(screen, "Hat {} value: {}".format(i, str(hat)))
        # textPrint.unindent()
        #
        # textPrint.unindent()

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()