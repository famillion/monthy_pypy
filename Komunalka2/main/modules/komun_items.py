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
            'sum': None,
            'raznica': None
        },
        'voda': {
            'actual': None,
            'prev': None,
            'tarif': None,
            'sum': None,
            'raznica': None
        },
        'gaz': {
            'isLich': False,
            'actual': None,
            'prev': None,
            'tarif': None,
            'transit': None,
            'sum': None,
            'raznica': None
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

    def __init__(self, data, name):
        self.data = data
        self.__name = name

    def raznica(self):
        r = 0
        if self.data["actual"] and self.data["prev"]:
            r = self.data["actual"] - self.data["prev"]
            self.data['raznica'] = r
        return r

    @staticmethod
    def all_price_sum(list_price):
        return sum(list_price)

    def item_price_sum(self):
        summ = self.raznica() * self.data['tarif']
        self.data['sum'] = float(format(summ, '.2f'))
        return float(format(summ, '.2f'))

    def get_name(self):
        return self.__name

    def get_data(self):
        return self.data


class Electro(KomunItem):
    def __init__(self, data, name='electro'):
        super().__init__(data, name)

    def item_price_sum(self):
        r = self.raznica()
        summ = 0
        if self.data['limit'] > r:
            summ = self.data['min'] * r
        else:
            summ = self.data['max'] * r
        self.data['sum'] = float(format(summ, '.2f'))
        return float(format(summ, '.2f'))

class Voda(KomunItem):
    def __init__(self, data, name='voda'):
        super().__init__(data, name)

class Gaz(KomunItem):
    def __init__(self, data, name='gaz'):
        super().__init__(data, name)

    def item_price_sum(self, flag=False):
        summ = 0
        if flag:
            self.data['isLich'] = flag
            summ = (self.data['tarif'] * self.raznica()) + self.data['transit']
        else:
            summ = self.data['actual']
        self.data['sum'] = float(format(summ, '.2f'))
        return float(format(summ, '.2f'))

class Dom(KomunItem):
    def __init__(self, data, name='dom'):
        super().__init__(data, name)

    def item_price_sum(self):
        return self.data['actual']
