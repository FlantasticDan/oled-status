import time
import secrets
from typing import Dict
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
    
        self.keys = []

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
            if self.current >= len(self.messages):
                self.current = 0
            try:
                self.update(self.messages[self.current], self.current)
            except:
                continue
    
    def new_key(self) -> str:
        """Generate a new, unique message key

        Returns
        -------
        str
            Unique Message Key
        """        
        while True:
            key = secrets.token_hex(2)
            if key not in self.keys:
                self.keys.append(key)
                return key

    def add_message(self, header: str, body: str) -> str:
        """Add a message to the status cycle

        Parameters
        ----------
        header : str
            Message Header
        body : str
            Content of the Message

        Returns
        -------
        str
            Message Key, to be used in futre requests to this message.
        """        
        message = {
            'header': header,
            'body': body,
            'key': self.new_key()
        }
        self.messages.append(message)
        return message['key']
    
    def replace_message(self, key: str, header: str, body: str) -> None:
        """Replace a message in the status cycle with a new message

        Parameters
        ----------
        key : str
            Message Key
        header : str
            Message Header
        body : str
            Content of the Message
        """        
        for i, message in enumerate(self.messages):
            if key == message['key']:
                self.messages[i]['header'] = header
                self.messages[i]['body'] = body
                return
    
    def delete_message(self, key: str) -> None:
        """Delete a message from the status cycle

        Parameters
        ----------
        key : str
            [description]
        """        
        for i, message in enumerate(self.messages):
            if key == message['key']:
                self.messages.pop(i)
                self.keys.remove(key)
                return

if __name__ == '__main__':
    o = OLED()
    a = o.add_message('Test', 'Message 1')
    time.sleep(6)
    b = o.add_message('Example', 'Important Info')
    time.sleep(11)
    o.replace_message(a, 'Test', 'Updated Message 1')
    time.sleep(15)
    o.delete_message(a)
    time.sleep(10)
    o.delete_message(b)
    time.sleep(6)
    c = o.add_message('oled-status', 'Test Completed')