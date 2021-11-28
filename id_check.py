import os, sys
# Translate asset paths to useable format for PyInstaller
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('id_check_on_memory.ui')
from sys import exit
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication

from PyQt5 import uic

form_class = uic.loadUiType(form)[0]

class Id_Check(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

        self.value = self.input.toPlainText()
        self.type = self.comboBox.currentText()
        self.warning_text = ""

        self.btn_exec.clicked.connect(lambda: self.execution())
        self.btn_exec_2.clicked.connect(lambda: self.execution_2())

    def execution(self):
        variable_name = self.lineEdit.text()
        self.value = self.input.toPlainText()
        self.type = self.comboBox.currentText()
        if self.type == 'string':
            value = str(self.value)
        elif self.type == 'integer':
            try:
                value = int(self.value)
            except:
                self.warning_text = f"SORRY, IT's NOT {self.type.upper()} TYPE. YOU SET THE WRONG 'TYPE' ON YOUR INPUT VALUES."
        elif self.type == 'float':
            try:
                value = float(self.value)
            except:
                self.warning_text = f"SORRY, IT's NOT {self.type.upper()} TYPE. YOU SET THE WRONG 'TYPE' ON YOUR INPUT VALUES."
        elif self.type == 'list':
            try:
                value = eval(f"list([{self.value}])")
            except:
                self.warning_text = f"SORRY, IT's NOT {self.type.upper()} TYPE. YOU SET THE WRONG 'TYPE' ON YOUR INPUT VALUES."
        elif self.type == 'tuple':
            try:
                value = eval(f"tuple([{self.value}])")
            except:
                self.warning_text = f"SORRY, IT's NOT {self.type.upper()} TYPE. YOU SET THE WRONG 'TYPE' ON YOUR INPUT VALUES."
        elif self.type == 'set':
            try:
                value = eval(f"set([{self.value}])")
            except:
                self.warning_text = f"SORRY, IT's NOT {self.type.upper()} TYPE. YOU SET THE WRONG 'TYPE' ON YOUR INPUT VALUES."
        elif self.type == 'dictionary':
            try:
                value = eval(f"dict({self.value})")
            except:
                self.warning_text = f"SORRY, IT's NOT {self.type.upper()} TYPE. YOU SET THE WRONG 'TYPE' ON YOUR INPUT VALUES."
        elif self.type == 'variable':
            try:
                value = globals()['{}'.format(self.value)]
            except:
                self.warning_text = f"SORRY, IT's NOT {self.type.upper()} TYPE. YOU SET THE WRONG 'TYPE' ON YOUR INPUT VALUES."
        elif self.type == 'id':
            self.id_result.setText(str(id(globals()['{}'.format(variable_name)])))
            result_line = f"{variable_name} | {type(globals()['{}'.format(variable_name)])} | {globals()['{}'.format(variable_name)]} | {id(globals()['{}'.format(variable_name)])}"
            return self.history.append(result_line)

        self.warning.setText(self.warning_text)
        globals()['{}'.format(variable_name)] = value
        assigned_id = id(globals()['{}'.format(variable_name)])
        self.id_result.setText(str(assigned_id))
        result_line = f"{variable_name} | {type(globals()['{}'.format(variable_name)])} | {globals()['{}'.format(variable_name)]} | {id(globals()['{}'.format(variable_name)])}"
        self.history.append(result_line)

    def execution_2(self):
        variable_name = self.lineEdit.text()
        self.value = self.input.toPlainText()
        variable = [globals()['{}'.format(variable_name)]][0]
        action = self.comboBox_2.currentText()
        divider = "-+-"*25
        result_line = f"BEFORE_EXECUTION : {variable_name} | {type(variable)} | {variable} | {id(variable)}"
        self.history.append(divider)
        self.history.append(result_line)

        if action == 'add item':
            if type(variable) == list:
                variable.extend(eval(f"list([{self.value}])"))
            elif type(variable) == tuple:
                variable += eval(f"tuple([{self.value}])")
            elif type(variable) == set:
                variable.update(eval(f"set([{self.value}])"))

        elif action == 'delete item':
            if type(variable) == list:
                variable.remove(eval(f"list([{self.value}])")[0])
            elif type(variable) == set:
                variable.difference_update(eval(f"set([{self.value}])"))

        assigned_id = id(variable)
        self.id_result.setText(str(assigned_id))
        result_line = f"AFTER_EXECUTION : {variable_name} | {type(variable)} | {variable} | {id(variable)}"
        self.history.append(result_line)

    def initUI(self):
        self.setWindowTitle('파이썬 변수 ID 확인')
        self.resize(800, 600)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Id_Check()
    form.show()
    exit(app.exec_())