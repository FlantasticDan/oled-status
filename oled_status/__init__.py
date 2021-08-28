import time
from threading import Thread

import httpx

WIDTH = 128
HEIGHT = 32
VERSION = '0.0.2'

class Status:
    """OLED Display Status
    """
    def __init__(self, header: str, body:str) -> None:
        """Adds a new Status Message to the OLED Display Cycle

        Parameters
        ----------
        header : str
            Message Header
        body : str
            Message Contents
        """        
        self.header = header
        self.body = body

        self.key = None

        self.startup = Thread(target=self._add_message)
        self.startup.start()
    
    def _add_message(self) -> None:
        """__Internal Method__ to add a message in another thread"""        
        while not self.key:
            try:
                self.key = httpx.post('http://localhost:6533/add', json={'header': self.header, 'body': self.body}).text
                return
            except:
                time.sleep(1)
    
    def update(self, body: str, header=None) -> None:
        """
        Update OLED Display Status Message

        Parameters
        ----------
        body : str
            Message Body
        header : [type], optional
            Message Header, by default None which leaves the existing Header in place.
        """        
        if header:
            self.header = header
        self.body = body

        self.replace = Thread(target=self._replace_message)
        self.replace.start()
    
    def _replace_message(self) -> None:
        """__Internal Method__ to replace a message in another thread"""
        while True:
            try:
                httpx.post(f'http://localhost:6533/replace/{self.key}', json={'header': self.header, 'body': self.body})
                return
            except:
                time.sleep(1)
    
    def clear(self) -> None:
        """Delete Message from the OLED"""
        self.delete = Thread(target=self._delete_message)
        self.delete.start()

    def _delete_message(self) -> None:
        """__Internal Method__ to remove a message in another thread"""
        while True:
            try:
                httpx.get(f'http://localhost:6533/delete/{self.key}')
                return
            except:
                time.sleep(1)

if __name__ == '__main__':
    s = Status('Header', 'Messager')