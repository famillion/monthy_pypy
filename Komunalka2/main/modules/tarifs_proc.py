from os import path
from main.modules.read_write import read_json, write_to_json
import json

PATH = 'data/tarifs.json'

class Tarifs:
    __TARIFS = {
        'electro': {
            'min': None, #type: float,
            'max': None, #type: float,
            'limit': None  # type: float
        },
        'voda': {
            'tarif': None,  # type: float
        },
        'gaz': {
            'tarif': None,  # type: float
            'transit': 0,  # type: float
        }
    }

    def __init__(self):

        if not path.exists(PATH):
            self.__create_tarifs_json()
        else:
            self.__set_tarifs_from_json()

    def __set_tarifs_from_json(self):
        self.__TARIFS = read_json(PATH)

    def __create_tarifs_json(self):
        write_to_json(PATH, self.__TARIFS)

    def get_tarifs(self):
        return self.__TARIFS

    def set_new_tarif_item(self, name, ob):
        j = read_json(PATH)
        j[name] = ob
        write_to_json(PATH, j)



