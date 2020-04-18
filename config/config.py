import json
from os import listdir

class Config:
    def __init__(self):
        with open("config.json", "r") as json_file:
            conf = json.load(json_file)
            self.__dict__.update(conf)