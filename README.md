# Drive By Wire Golf Cart
## MEEN 401 Senior Design

The Drive By Wire system developed by this Mechanical Engineering Senior Design Team at Texas A&M allows a user to remotely operate a Polaris Gem e6 Golf Cart with a controller. This project is the first step is a series of projects to create an autonomous vehicle that can be summoned by people with mobility impairements. Once the vehicle arrives, the user can wheel into the cart, lock themselves into place, and be transported autonomously to their desired location. This will allow people with mobility impairements to have more freedom to explore and travel where they need to go. 

## Getting Started

The first step to getting started is to clone/download this project and open the file "DriveByWireMainProgram.py" in your favorite IDE/Python environment. For the purposes of this project, this code was cloned to a raspberry pi 3B+ and ran there. 

IQ 20 - 

### Prerequisites

The following components were used for this project:

1. Joystick/Controller - Plug in a USB joystick or controller to the raspberry pi. This team used a Logitech Joystick
2. CAN shield - mounts onto the top of the raspberry pi and provides the CAN signaling LINK
3. Steering Motor - (ensure this is the "autonomous ready" version -- see the steering motor documentation)
4. Actuator - Two actuators, one for accelerating and one for braking (see the actuator documentation)


## Running The Script

Once the script is ran, the pygame window will launch and show the output of the joystick. Moving the joystick left/right will turn the steering motor and forward/backwards will move the two actuators.


## Built With

* [Python 3.6](https://www.python.org/downloads/release/python-360/) - Language
* [Python-Can](https://pypi.org/project/python-can/#targetText=The%20can%20package%20provides%20controller,on%20Mac%2C%20Linux%20and%20Windows.) - Used to communicate with actuators and steering motor
* [PyGame](https://www.pygame.org/wiki/GettingStarted) - Allows the logitech controller to communicate with the pi

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **Kyle Snell** - *Initial work* -
* **Tyler Wooten** - *Initial work* - 
* **Addison Avila** - *Initial work* - 
* **Parker Denning** - *Initial work* -
* **Matthew Kress** - *Initial work* - 

## Acknowledgments

* Thank you to Dr. Saripalli at Texas A&M for being the project sponsor
