from selenium import webdriver	
from dotenv import dotenv_values

class Browser:
    _instance = None
    _keyword = None
    config = dotenv_values(".env")
    _bot = config.get('BOT_NAME')
    def __new__(cls):
        if cls._instance is None:
            cls._instance = webdriver.Firefox()
        return cls._instance
    
    def get(self, url, bot_name):
        self._instance.get(url)
        self._bot = bot_name
        
    def instance(self, status):
        self._instance = status