import main.modules.read_write as wr
from os import path
import datetime

PATH = 'data/data.json'

class AllItems:
    __JSON = [{
        'electro': {
            'min': None,
            'max': None,
            'limit': None,
            'actual': None,
            'prev': None,
            'sum': None
        },
        'voda': {
            'actual': None,
            'prev': None,
            'tarif': None,
            'sum': None
        },
        'gaz': {
            'isLich': False,
            'actual': None,
            'prev': None,
            'tarif': None,
            'transit': None,
            'sum': None
        },
        'dom': {
            'actual': None
        },
        'date': 'test',
        'allSum': None
    }]

    def __init__(self):
        if not path.exists(PATH):
            wr.write_to_json(PATH, self.__JSON)
        else:
            self.__JSON = wr.read_json(PATH)

    def get_json(self):
        return self.__JSON

    def get_prev_json(self):
        return self.__JSON[-1]

    @staticmethod
    def write_all_to_json(ob_all_items):
        wr.write_to_json(PATH, ob_all_items)


class KomunItem:
    data = {}

    def __init__(self, name):
        self.__name = name

    @staticmethod
    def raznica(new_data, old_data):
        return new_data["actual"] - old_data["actual"]

    @staticmethod
    def all_price_sum(list_price):
        return sum(list_price)

    @staticmethod
    def item_price_sum(new_data, old_data):
        return KomunItem.raznica(new_data, old_data) * new_data['tarif']

    def get_name(self):
        return self.__name

    def get_data(self):
        return self.data


class Electro(KomunItem):
    def __init__(self, new_data, name='electro'):
        super().__init__(name)
        self.data = new_data

    def item_price_sum(self, new_data, old_data):
        r = self.raznica(new_data, old_data)
        if self.data['limit'] > r:
            return self.data['tarif']['min'] * r
        else:
            return self.data['tarif']['max'] * r

class Voda(KomunItem):
    def __init__(self,new_data, name='voda'):
        super().__init__(name)
        self.data = new_data

class Gaz(KomunItem):
    def __init__(self, new_data, name='gaz'):
        super().__init__(name)
        self.data = new_data

    def item_price_sum(self, flag=False, new_data=None, old_data=None):
        if flag:
            self.data['isLich'] = flag
            return (self.data['tarif'] * self.raznica(new_data, old_data)) + self.data['transit']
        else:
            return self.data['actual']

class Dom(KomunItem):
    def __init__(self, new_data, name='dom'):
        super().__init__(name)
        self.data = new_data

    def item_price_sum(self, data=True):
        return self.data['actual']
