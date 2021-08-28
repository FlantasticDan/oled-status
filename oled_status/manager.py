from typing import Dict
import time
from threading import Thread

import board
import adafruit_ssd1306
from PIL import Image

from . import WIDTH, HEIGHT, VERSION
from .draw import generate_status_image

class OLED:
    """
    OLED Display Manager, automatically cycles through messages and prevents burn in.
    """    
    def __init__(self) -> None:
        self.i2c = board.I2C()
        self.display = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, self.i2c, addr=0x3C)
    
        self.messages = []
        self.current = 0
        self.inverted = False
    
        boot_img = generate_status_image('oled-status', f'v. {VERSION}', 'SERVER STARTED')
        self.update_display(boot_img)

        self.cycle_thread = Thread(target=self.cycle)
        self.cycle_thread.start()
    
    def update_display(self, image: Image.Image, inverted=False) -> None:
        """Draw image to OLED display

        Parameters
        ----------
        image : Image.Image
            Image to be draw to display
        inverted : bool, optional
            Used to clear the display in the most optimal way, by default False
        """        
        # Clear the Display
        if inverted:
            self.display.fill(255)
        else:
            self.display.fill(0)
        # self.display.show()

        # Write Image to Screen
        self.display.image(image)
        self.display.show()
    
    def update(self, message: Dict[str, str], index: int) -> None:
        """Generate image and draw that image on the OLED display

        Parameters
        ----------
        message : Dict[str, str]
            Status message information
        index : int
            Message Index
        """        
        footer = str(index + 1) + '/' + str(len(self.messages))
        # self.inverted = not(self.inverted)
        image = generate_status_image(message['header'], message['body'], footer, self.inverted)
        self.update_display(image, self.inverted)

    def cycle(self) -> None:
        """
        Cycle the OLED display through the messages.
        """        
        while True:
            time.sleep(5)

            # Placeholder if there are no valid messages
            if len(self.messages) == 0:
                self.current = 0
                self.update({'header': 'oled-status', 'body': 'No Messages'}, -1)
                continue
            
            # Advance to Next Message
            self.current += 1
            if self.current > len(self.messages):
                self.current = 0
            self.update(self.messages[self.current], self.current)


if __name__ == '__main__':
    OLED()