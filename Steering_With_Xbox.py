import pygame
import can
from can import Message

#os.system('sudo /sbin/ip link set can0 up type can bitrate 250000')
bus = can.interface.Bus(channel='can0', bustype='socketcan_native')

#Define all messages to be sent
Left1 = Message(arbitration_id= 419365113, data=[3, FF, FF, FF, FF, 1, 0, 0])
Left2 = Message(arbitration_id= 419365113, data=[3, FF, FF, FF, FF, 3, 0, 0])
Left3 = Message(arbitration_id= 419365113, data=[3, FF, FF, FF, FF, 5, 0, 0])
Right1 = Message(arbitration_id= 419365113, data=[3, 0, 0, 0, 0, 1, 0, 0])
Right2 = Message(arbitration_id= 419365113, data=[3, 0, 0, 0, 0, 3, 0, 0])
Right3 = Message(arbitration_id= 419365113, data=[3, 0, 0, 0, 0, 5, 0, 0])
StopAll = Message(arbitration_id= 419365113, data=[0, 0, 0, 0, 0, 0, 0, 0])

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
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
        # RECOMMEND: Knob movements don't do anything from -0.15 to 0.15 because it is never really 0

        # Stops turning section
        if -0.15 < axis0 < 0.15:
            bus.send(StopAll)
            print("not moving\n")

        # Turning right section
        if 0.15 < axis0 < 0.3:
            bus.send(Right1)
            print("Right 1\n")

        if 0.3 < axis0 < 0.6:
            bus.send(Right2)
            print("Right 2\n")

        if 0.6 < axis0 <= 1.00:
            bus.send(Right3)
            print("Right 3\n")

        # Turning Left section
        if -0.15 > axis0 > -0.3:
            bus.send(Left1)
            print("Left 1\n")

        if -0.3 > axis0 > -0.6:
            bus.send(Left2)
            print("Left 2\n")

        if -0.6 > axis0 >= -1.00:
            bus.send(Left3)
            print("Left 3\n")

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