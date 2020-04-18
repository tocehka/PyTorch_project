import requests
from config import Config

class ProxyList():
    def __init__(self):
        config = Config()
        r = requests.get(config.proxy_url)
        proxy = r.text.split("\r\n")
        self.__proxy = proxy[:len(proxy)-1]
    def get(self):
        return self.__proxy