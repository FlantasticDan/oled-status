# oled-status
Status message logger for embedded systems equipped with a small OLED display.

OLED Status has two parts: the server module that drives the display and the client library that pushes data to the display.  The server is meant to be run as a module and requires the following Setup procedure.  The client is designed to be embedded in other apps running on the device to show relevant information on an otherwise embedded app.

## Setup
OLED Status requires both hardware and software setup to work properly.  This setup is required to use OLED Status on a display attached to the device.

### Hardware
A Single Board Computer running Linux with I<sup>2</sup>C support connected to a 0.91" 128x32 OLED Display driven by a SSD1306.  OLED Status was developed and has only been tested on a Raspberry Pi 4 with a Treedix Display Module.

- Displays
    - [Treedix 0.91" OLED Display Module (Blue/White)](https://www.amazon.com/gp/product/B08D9FPLYH)
    - [Adafruit Monochrome 0.91" 128x32 I2C OLED Display - STEMMA QT / Qwiic](https://www.adafruit.com/product/4440)
    - [Adafruit PiOLED - 128x32 Monochrome OLED Add-on for Raspberry Pi](https://www.adafruit.com/product/3527)
- Single Board Computer
    - [Raspberry Pi 4](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)

For wiring instructions, see [Adafruit's Python Wiring Guide](https://learn.adafruit.com/monochrome-oled-breakouts/python-wiring).

### Software
Adafruit's Circuit Python compatability layer, Blinka, drives the OLED display and can be a bit tricky to install.  OLED was developed and testes only on Ubuntu 20.04 but should be fully compatiable with any Blinka supported OS.

#### Ubuntu
1. Update Ubuntu and it's packages:
```bash
sudo apt update
sudo apt upgrade
```
2. Ubuntu doesn't ship with a compatiable version of Python, install Python 3.9+ and it's dependencies:
```bash
sudo apt install python3.9 python3.9-venv python3.9-dev
```
3. Ubuntu resticts access to the I<sup>2</sup>C bus to root users by default.  Create a udev rule to allow all users access automatically at boot by writing the following file at `/etc/udev/rules.d/i2c.rules`:
```
ACTION=="add", KERNEL=="i2c-[0-1]*", MODE="0666"
```
  - Learn more from [this StackExchange Answer](https://unix.stackexchange.com/questions/147494/how-can-i-set-device-rw-permissions-permanently-on-raspbian)
4. Reboot for the udev rule to take effect:
```bash
sudo reboot
```
5. Optionally setup a virtual environment:
```bash
python3.9 -m venv ./venv
. venv/bin/activate
```

The remainder of the setup will be handled by `pip` when OLED Status is installed.

#### Raspberry Pi OS
See [Adafruit's Circuit Python Installation Guide](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi#update-your-pi-and-python-2993452-6) and then setup a virtual environment if desired.


## Installation
OLED Status is distributed via [Github Releases](https://github.com/FlantasticDan/oled-status/releases) and [PyPI](https://pypi.org/project/oled-status).

### Server
The server should be installed and set to autorun **_once_**, multiple client libraries and processes can connect to a single server instance.
1. Install the OLED Status Server from PyPI:
```bash
pip install oled-status[server]
```
- **Note** this also installs the relevant Circuit Python dependecies to communicate with the display.  If it fails to install, try again after running `pip install wheel` to add support for `bdist_wheel`.

At this point the server can be started with `python -m oled_status.server` and the OLED Display will be initialized.  It's likly preferable that the server be automatically started at bootup, in which case continue:

2. Create a service to automatically start the OLED Status Server, this varies depending on if a virtual environemnt (recommended) is in use.  These are the instructions for using a virtual environment:
    1. Create a `start-oled-status-server.sh` script which activates the virtual environment and then starts the OLED Status Server:
    ```bash
    #!/bin/bash
    cd <directory>
    . venv/bin/activate
    python -m oled_status.server
    ```
    2. Modify the script so it is executable: `sudo chmod +x start-oled-status-server.sh`
    3. Create a service the run the script at startup by writing the following file at `/etc/systemd/system/oled-status.service`:
    ```
    [Unit]
    Description=OLED Status Server
    StartLimitIntervalSec=0

    [Service]
    Type=simple
    Restart=always
    RestartSec=1
    User=<username>
    ExecStart=/path/to/start-oled-status-server.sh

    [Install]
    WantedBy=multi-user.target
    ```
    4. Enable the startup service: `systemctl enable oled-status`
    5. Reboot

### Client
The client libary is to be used by any locally running application that wishes to display data on the OLED Display.
```bash
pip install oled-status
```

## Use
The OLED Status provides a single `Status` Class which when intantiated allows for messages to be added to, modified on, and removed from the OLED Display.  The client communicates with the server over local port `6533` on seperate threads to prevent status updates from blocking execution.

When there are multiple messages to be displayed on the OLED Display, they are automatically cycled through, each showing for 5 seconds in the order they were recieved.  Messages that are updated retain their original position in the cycle.  As a result of the cycle, messages are not instantly displayed.

```python
from oled_status import Status

# Publish a new message
message = Status('Heading', 'Message Contents')

# Update a message
message.update('Updated Message')

# Clear a message
message.clear()
```

**Note** The OLED Display is tiny, messages that are longer than about 14 uppercase letters will be truncated.
