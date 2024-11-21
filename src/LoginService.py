import logging
import os
from dotenv import load_dotenv

from src.CommonConstants import *

class LoginService :

    def __init__(self):
        load_dotenv()

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

        self.USERS_INFO = os.getenv("USERS_INFO", "") + os.getenv("USERS_INFO2", "")

    def verifyLogin(self, username, password):
        self.logger.info(f"verifyLogin : started ... ")

        search_text = "###" + username + "=" + password + "###"

        result = None
        if search_text in self.USERS_INFO:
            result = username  # Authentication successful
            self.logger.info(f"verifyLogin : Login sucessfull for the user : {username} ")
        else :
            result = None
            self.logger.info(f"verifyLogin : Login failed for the user : {username} ")
        return result

