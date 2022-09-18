from PyQt5 import QtWidgets
from PyQt5.QtGui import QDoubleValidator, QValidator
from main.modules.MainForm import Ui_MainForm
import sys
import datetime
from main.modules.tarifs_proc import Tarifs
import main.modules.komun_items as alls
from main.modules.telega_bot import send_to_bot

class Kommunalka(QtWidgets.QMainWindow):
    def __init__(self):
        super(Kommunalka, self).__init__()
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)
        self.mess = QtWidgets.QMessageBox

        self.allItems = alls.AllItems()
        self.tarifs = Tarifs()

        if self.tarifs.get_tarifs()['electro']['limit']:
            ob = self.tarifs.get_tarifs()['electro']['limit']
            self.ui.elektro_tarif_min.setPlaceholderText('< ' + str(ob))
            self.ui.elekttro_tarif_max.setPlaceholderText('> ' + str(ob))

        # всі поля вводу тексту з валідатором для вводу тільки чисел

        self.ui.new_el_min.editingFinished.connect(lambda: self.value_validating(self.ui.new_el_min))
        self.ui.new_el_max.editingFinished.connect(lambda: self.value_validating(self.ui.new_el_max))
        self.ui.new_limit.editingFinished.connect(lambda: self.value_validating(self.ui.new_limit))
        self.ui.new_voda.editingFinished.connect(lambda: self.value_validating(self.ui.new_voda))
        self.ui.new_gaz.editingFinished.connect(lambda: self.value_validating(self.ui.new_gaz))
        self.ui.new_gaz_tranzit.editingFinished.connect(lambda: self.value_validating(self.ui.new_gaz_tranzit))
        self.ui.el_old_pok.editingFinished.connect(lambda: self.value_validating(self.ui.el_old_pok))
        self.ui.old_voda_pok.editingFinished.connect(lambda: self.value_validating(self.ui.old_voda_pok))
        self.ui.old_gaz_pok.editingFinished.connect(lambda: self.value_validating(self.ui.old_gaz_pok))
        self.ui.elektro_pok.editingFinished.connect(lambda: self.value_validating(self.ui.elektro_pok))
        self.ui.elektro_tarif_min.editingFinished.connect(lambda: self.value_validating(self.ui.elektro_tarif_min))
        self.ui.elekttro_tarif_max.editingFinished.connect(lambda: self.value_validating(self.ui.elekttro_tarif_max))
        self.ui.voda_pok.editingFinished.connect(lambda: self.value_validating(self.ui.voda_pok))
        self.ui.voda_tarif.editingFinished.connect(lambda: self.value_validating(self.ui.voda_tarif))
        self.ui.gaz_pok.editingFinished.connect(lambda: self.value_validating(self.ui.gaz_pok))
        self.ui.gaz_tarif.editingFinished.connect(lambda: self.value_validating(self.ui.gaz_tarif))
        self.ui.dom_pok.editingFinished.connect(lambda: self.value_validating(self.ui.dom_pok))

        # дата
        self.ui.date_new.setText(datetime.datetime.today().strftime('%d-%m-%Y'))

        # кнопки вкладки опції
        self.ui.save_new_el_btn.clicked.connect(self.save_electro_tar_btn)
        self.ui.save_new_voda_btn.clicked.connect(self.save_voda_tar_btn)
        self.ui.save_new_gas_btn.clicked.connect(self.save_gaz_tar_btn)
        self.ui.save_old_pok_btn.clicked.connect(self.save_old_all_pok_btn)
        self.ui.story_date_Box.addItems([item['date'] for item in self.allItems.get_json()])
        self.ui.story_date_Box.textActivated.connect(self.show_history_from_date)
        self.ui.scrin_to_telega_btn.clicked.connect(self.screen_to_telega)

    def screen_to_telega(self):
        screen = QtWidgets.QApplication.primaryScreen()
        wind = self.ui.rozrah_tab
        screenshot = screen.grabWindow(wind.winId(), width=770, height=400)
        screenshot.save('screen/shot.jpg', 'jpg')
        send_to_bot()

    def show_history_from_date(self):
        str_date = self.ui.story_date_Box.currentText()
        item = list(filter( lambda i: i['date'] == str_date, self.allItems.get_json()))[0]
        self.ui.el_story_pok.setText(str(item['electro']['actual']))
        self.ui.el_story_sum.setText(str(item['electro']['sum']))
        self.ui.voda_story_pok.setText(str(item['voda']['actual']))
        self.ui.voda_story_sum.setText(str(item['voda']['sum']))
        self.ui.gaz_story_pok.setText(str(item['gaz']['actual']))
        self.ui.gaz_story_sum.setText(str(item['gaz']['sum']))
        self.ui.dom_story_sum.setText(str(item['dom']['actual']))
        self.ui.all_sum_story.setText(str(item['allSum']))


    def save_electro_tar_btn(self):
        min_tar = float(self.ui.new_el_min.text().replace(',', '.'))
        max_tar = float(self.ui.new_el_max.text().replace(',', '.'))
        limit = float(self.ui.new_limit.text().replace(',', '.'))
        ob = {'min': min_tar, 'max': max_tar, 'limit': limit}

        self.ui.elektro_tarif_min.setText(str(ob['min']))
        self.ui.elekttro_tarif_max.setText(str(ob['max']))

        self.tarifs.set_new_tarif_item('electro', ob)

    def save_voda_tar_btn(self):
        tar = float(self.ui.new_voda.text().replace(',', '.'))
        ob = {'tarif': tar}

        self.ui.voda_tarif.setText(str(ob['tarif']))

        self.tarifs.set_new_tarif_item('voda', ob)

    def save_gaz_tar_btn(self):
        tar = float(self.ui.new_gaz.text().replace(',', '.'))
        tran = float(self.ui.new_gaz_tranzit.text().replace(',', '.'))
        ob = {'tarif': tar, 'transit': tran}

        self.ui.gaz_tarif.setText(str(ob['tarif']))

        self.tarifs.set_new_tarif_item('gaz', ob)

    def save_old_all_pok_btn(self):
        ob = self.allItems.get_json()
        new_ob = {
            'electro': {
                'actual': float(self.ui.el_old_pok.text().replace(',', '.')) if self.ui.el_old_pok.text() else ob[-1]['electro']['actual'],
                'sum': 'test'
            },
            'voda': {
                'actual': float(self.ui.old_voda_pok.text().replace(',', '.')) if self.ui.old_voda_pok.text() else ob[-1]['voda']['actual'],
                'sum': 'test'
            },
            'gaz': {
                'actual': float(self.ui.old_gaz_pok.text().replace(',', '.')) if self.ui.old_gaz_pok.text() else ob[-1]['gaz']['actual'],
                'isLich': bool(self.ui.islich.isChecked()),
                'sum': 'test'
            },
            'dom': {
                'actual': 'test'
            },
            'date': datetime.datetime.today().strftime('%d-%m-%Y'),
            'allSum': 'test'
        }

        self.ui.elektro_last.setText(str(new_ob['electro']['actual']))\
            if new_ob['electro']['actual'] \
            else self.mess.information(self, 'Увага', 'Введіть минулі показники лічильника електроенергії!')
        self.ui.voda_last.setText(str(new_ob['voda']['actual'])) \
            if new_ob['voda']['actual'] \
            else self.mess.information(self, 'Увага', 'Введіть минулі показники лічильника води!')
        if new_ob['gaz']['isLich']:
            if not new_ob['gaz']['actual']:
                self.mess.information(self, 'Увага', 'Введіть минулі показники лічильника газу!')
            else:
                self.ui.gaz_last.setText(str(new_ob['gaz']['actual']))
        if ob[-1]['date'] == new_ob['date']:
            ob.pop()
            ob.append(new_ob)
            self.allItems.write_all_to_json(ob)
        else:
            ob.append(new_ob)
            self.allItems.write_all_to_json(ob)
        self.allItems = alls.AllItems()

    def value_validating(self, el) -> None:
        val_rule = QDoubleValidator(0.00001, 1000000, 4)
        if val_rule.validate(el.text(), 14)[0] == QValidator.Acceptable:
            el.text().replace(',', '.')
            el.setFocus()
        else:
            el.setText('')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = Kommunalka()
    window.show()

    sys.exit(app.exec_())
