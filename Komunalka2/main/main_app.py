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
        self.isCheckLich = False

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

        # встановлюємо в лейбли минулі значення показників
        self.ui.elektro_last.setText(str(int(self.allItems.get_prev_json()['electro']['actual'])))
        self.ui.elektro_tarif_min.setText(str(self.tarifs.get_tarifs_from_name('electro')['min']))
        self.ui.elekttro_tarif_max.setText(str(self.tarifs.get_tarifs_from_name('electro')['max']))
        self.ui.voda_last.setText(str(int(self.allItems.get_prev_json()['voda']['actual'])))
        self.ui.voda_tarif.setText(str(self.tarifs.get_tarifs_from_name('voda')['tarif']))
        self.ui.islich.stateChanged.connect(self.isLich_checked)

        # кнопки вкладки розрахунки
        self.ui.sum_btn.clicked.connect(self.rozrahuvat_btn)
        self.ui.scrin_to_telega_btn.clicked.connect(self.screen_to_telega)
        self.ui.save_all_btn.clicked.connect(self.save_new_all_to_json)

        self.new_obj = {
            'electro': None,
            'voda': None,
            'gaz': None,
            'dom': None
        }
        self.gaz_r = 0

    def save_new_all_to_json(self):
        nob = self.new_obj
        oob = self.allItems.get_json()
        def func():
            oob.append ( nob )
            self.allItems.write_all_to_json ( oob )
            self.allItems = alls.AllItems ()
            self.mess.information ( self, "Збережено!", "Вітаю! Завдання виконано! Все збережено!" )

        if (nob['electro']) and (nob['voda']) and (nob['gaz']) and (nob['dom']):
            if (nob['date'] == oob[-1]['date']) and (nob['electro']['actual'] == oob[-1]['electro']['actual']):
                m = self.mess.information(self, 'Увага', "Схоже ці результати вже збережені! Всеодно зберегти?",
                                          QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
                if m == QtWidgets.QMessageBox.Yes:
                    func()
            else:
                func()
        else:
            self.mess.information(self, 'Не збережено!',
                                  'Не зміг зберегти, бо не все заповнено! Я зберігаю лише повністю заповнені результати, а так можеш і скрін зробити!')

    def rozrahuvat_btn(self):
        self.new_obj = {
            'electro': self.set_electro_field(),
            'voda': self.set_voda_field(),
            'gaz': self.set_gaz_field(),
            'dom': self.set_dom_field()
        }
        sum_list = [
            self.new_obj['electro']['sum'] if self.new_obj['electro'] else 0,
            self.new_obj['voda']['sum'] if self.new_obj['voda'] else 0,
            self.new_obj['gaz']['sum'] if self.new_obj['gaz'] else 0,
            self.new_obj['dom']['actual'] if self.new_obj['dom'] else 0
        ]

        self.new_obj['allSum'] = float(format(sum(sum_list), '.2f'))
        self.new_obj['date'] = self.ui.date_new.text()

        self.ui.sum_label.setText(str(self.new_obj['allSum']))

    def set_electro_field(self):
        prev = self.allItems.get_prev_json()['electro']
        el_p = self.ui.elektro_pok.text()
        el_t_min = self.ui.elektro_tarif_min.text()
        el_t_max = self.ui.elekttro_tarif_max.text()

        if el_p and (float(el_p) > prev['actual']):
            if el_t_min and el_t_max:
                el = alls.Electro(data={
                    'min': float(el_t_min),
                    'max': float(el_t_max),
                    'limit': self.tarifs.get_tarifs_from_name('electro')['limit'],
                    'actual': float(el_p),
                    'prev': prev['actual'],
                    'sum': None,
                    'raznica': None
                })
                self.ui.elektro_res.setText(str(el.raznica()))
                self.ui.electro_sum.setText(str(el.item_price_sum()))
                return el.get_data()
            else:
                self.mess.information(self, "Електроенергія!", 'Введіть тарифи')
        else:
            self.mess.information(self, "Електроенергія!", 'Некоректний ввід показників')

    def set_voda_field(self):
        pok = self.ui.voda_pok.text().replace(',', '.')
        last = float(self.ui.voda_last.text())
        tarif = float(self.ui.voda_tarif.text().replace(',', '.'))

        if pok and (float(pok) > last):
            if tarif:
                voda = alls.Voda({
                    'actual': float(pok),
                    'prev': last,
                    'tarif': tarif,
                    'sum': None,
                    'raznica': None
                })

                self.ui.voda_res.setText(str(voda.raznica()))
                self.ui.voda_sum.setText(str(voda.item_price_sum()))

                return voda.get_data()
            else:
                self.mess.information(self, "Вода!", 'Введіть тарифи')
        else:
            self.mess.information(self, "Вода!", 'Некореектний ввід показників')

    def set_gaz_field(self):
        pok = self.ui.gaz_pok.text().replace(',', '.')
        prev = self.allItems.get_prev_json()['gaz']['actual']
        tarif = self.tarifs.get_tarifs_from_name('gaz')['tarif']

        if pok and (float(pok) > prev):
            if tarif:
                gaz = alls.Gaz({
                    'isLich': self.isCheckLich,
                    'actual': float(pok),
                    'prev': prev,
                    'tarif': tarif,
                    'transit': self.tarifs.get_tarifs_from_name('gaz')['transit'],
                    'sum': None,
                    'raznica': None
                })

                self.gaz_r = gaz.raznica()
                self.ui.gaz_sum.setText(str(gaz.item_price_sum(self.isCheckLich)))
                return gaz.get_data()
            else:
                self.mess.information(self, "Газ!", 'Введіть тарифи')
        else:
            self.mess.information(self, "Газ!", 'Некореектний ввід показників')

    def set_dom_field(self):
        pok = self.ui.dom_pok.text().replace(',', '.')
        if pok:
            dom = alls.Dom({
                'actual': float(pok)
            })
            self.ui.dom_sum.setText(str(dom.item_price_sum()))
            return dom.get_data()
        else:
            self.mess.information(self, "Дом!", 'Некореектний ввід показників')

    def isLich_checked(self):
        if self.ui.islich.isChecked():
            self.ui.gaz_pok.setPlaceholderText('показники')
            self.ui.gaz_last.setText(str(int(self.allItems.get_prev_json()['gaz']['actual'])))
            self.ui.gaz_tarif.setText(str( self.tarifs.get_tarifs_from_name('gaz')['tarif']))
            self.isCheckLich = self.ui.islich.isChecked()
            self.ui.gaz_res.setText(str(self.gaz_r))
        else:
            self.ui.gaz_pok.setPlaceholderText('грн')
            self.ui.gaz_last.setText('')
            self.ui.gaz_tarif.setText('')
            self.isCheckLich = self.ui.islich.isChecked()
            self.ui.gaz_res.setText('')

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
        min_tar = self.ui.new_el_min.text()
        max_tar = self.ui.new_el_max.text()
        limit = self.ui.new_limit.text()
        if min_tar and max_tar and limit:
            ob = {
                'min': float(min_tar.replace(',', '.')),
                'max': float(max_tar.replace(',', '.')),
                'limit': float(limit.replace(',', '.'))
            }

            self.ui.elektro_tarif_min.setText(str(ob['min']))
            self.ui.elekttro_tarif_max.setText(str(ob['max']))

            self.tarifs.set_new_tarif_item('electro', ob)
            self.tarifs = Tarifs()
        else:
            self.mess.information(self, 'Увага!', "Некоректний ввід тарифів на електроенергію!")

    def save_voda_tar_btn(self):
        if self.ui.new_voda.text():
            tar = float(self.ui.new_voda.text().replace(',', '.'))
            ob = {'tarif': tar}

            self.ui.voda_tarif.setText(str(ob['tarif']))

            self.tarifs.set_new_tarif_item('voda', ob)
            self.tarifs = Tarifs()
        else:
            self.mess.information(self, 'Увага!', "Некоректний ввід тарифу на воду!")

    def save_gaz_tar_btn(self):
        if self.ui.new_gaz.text() and self.ui.new_gaz_tranzit.text():
            tar = float(self.ui.new_gaz.text().replace(',', '.'))
            tran = float(self.ui.new_gaz_tranzit.text().replace(',', '.'))
            ob = {'tarif': tar, 'transit': tran}

            self.ui.gaz_tarif.setText(str(ob['tarif']))

            self.tarifs.set_new_tarif_item('gaz', ob)
            self.tarifs = Tarifs()
        else:
            self.mess.information(self, 'Увага!', "Некоректний ввід тарифу та вартості тарифу на газ!")

    def save_old_all_pok_btn(self):
        ob = self.allItems.get_json()
        old_el = self.ui.el_old_pok.text().replace(',', '.')
        old_voda = self.ui.old_voda_pok.text().replace(',', '.')
        old_gaz = self.ui.old_gaz_pok.text().replace(',', '.')
        flag = self.isCheckLich
        new_ob = {
            'electro': {
                'actual': 'actual',
                'sum': 'test'
            },
            'voda': {
                'actual': 'actual',
                'sum': 'test'
            },
            'gaz': {
                'actual': 1,
                'isLich': False,
                'sum': 'test'
            },
            'dom': {
                'actual': 'test'
            },
            'date': datetime.datetime.today().strftime('%d-%m-%Y'),
            'allSum': 'test'
        }
        if old_el and old_voda:
            if flag and not old_gaz:
                self.mess.information(self, 'Увага', "Введіть минулі показники газу!")
            elif flag and old_gaz:
                new_ob['gaz']['actual'] = float(old_gaz)
                self.ui.gaz_last.setText(str(new_ob['gaz']['actual']))

            new_ob['electro']['actual'] = float(old_el)
            new_ob['voda']['actual'] = float(old_voda)

            self.ui.elektro_last.setText(old_el)
            self.ui.voda_last.setText(old_voda)

            if ob[-1]['date'] == new_ob['date']:
                ob.pop()
                ob.append(new_ob)
                self.allItems.write_all_to_json(ob)
            else:
                ob.append(new_ob)
                self.allItems.write_all_to_json(ob)
            self.allItems = alls.AllItems()
        else:
            self.mess.information( self, 'Увага', 'Введіть минулі показники лічильників електроенергії та води!' )

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
