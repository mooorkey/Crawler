from calendar import calendar
from cgitb import text
from random import randrange
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Crawler'
        self.width = 500
        self.height = 500
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width ,self.height)
        self.move(0, 0)
        
        self.table_widget = MainTable(self)
        self.setCentralWidget(self.table_widget)
        
        self.show()
    
class MainTable(QWidget):
    
   def __init__(self, parent):
      super(QWidget, self).__init__(parent)
      self.layout = QVBoxLayout()
      
      # Initialize tab screen
      self.tabs = QTabWidget()
      self.twitter_tab = QWidget()
      self.tab2 = QWidget()
      self.tabs.resize(300,200)
      
      # Add tabs
      self.tabs.addTab(self.twitter_tab,"TwitterAPI Crawling")
      self.tabs.addTab(self.tab2,"Web Crawling")
       
      # Twitter tab 
      self.twitter_tab.layout = QGridLayout(self)
      self.twitter_input_form_layout = QHBoxLayout()
      self.twitter_datetime_picker_layout = QGridLayout()
      self.get_info_button = QPushButton(parent=self.twitter_tab,text="Get Info.")
      self.twitter_input_box = InputForm(parent=self.twitter_tab)
      self.twitter_table = QTableWidget(parent=self.twitter_tab)

      self.datepicker_start_label = QLabel("Start date")
      self.datepicker_start = QDateEdit(calendarPopup=True)
      self.datepicker_start.setDateTime(QDateTime.currentDateTime())
      self.datepicker_end_label = QLabel("End date")
      self.datepicker_end = QDateEdit(calendarPopup=True)
      self.datepicker_end.setDateTime(QDateTime.currentDateTime().addDays(1))
      

      self.twitter_input_form_layout.addWidget(self.twitter_input_box)
      self.twitter_input_form_layout.addWidget(self.get_info_button)

      self.twitter_datetime_picker_layout.addWidget(self.datepicker_start_label, 0, 0, Qt.AlignmentFlag.AlignCenter)
      self.twitter_datetime_picker_layout.addWidget(self.datepicker_start, 1, 0, Qt.AlignmentFlag.AlignCenter)
      self.twitter_datetime_picker_layout.addWidget(self.datepicker_end_label, 0, 1, Qt.AlignmentFlag.AlignCenter)
      self.twitter_datetime_picker_layout.addWidget(self.datepicker_end, 1, 1, Qt.AlignmentFlag.AlignCenter)

      self.twitter_tab.layout.addLayout(self.twitter_input_form_layout, 0, 0, Qt.AlignmentFlag.AlignTop)
      self.twitter_tab.layout.addLayout(self.twitter_datetime_picker_layout, 1, 0)
      self.twitter_tab.layout.addWidget(self.twitter_table, 2, 0)
      self.twitter_tab.setLayout(self.twitter_tab.layout)

      # Useful
      self.get_info_button.clicked.connect(self.get_info_on_click)
      self.twitter_table.horizontalHeader().sectionClicked.connect(self.get_info_on_click)
      self.twitter_table.verticalHeader().sectionClicked.connect(self.get_info_on_click)

      # Add tabs to widget
      self.layout.addWidget(self.tabs)
      self.setLayout(self.layout)

   @pyqtSlot()
   def get_info_on_click(self):
      text = self.twitter_input_box.textfield.text()
      self.twitter_table.setRowCount(100)
      self.twitter_table.setColumnCount(100)
      for i in range(100):
         for j in range(100):
            self.twitter_table.setItem(i,j,QTableWidgetItem(text))
      QMessageBox.about(self,"test",f"input {text}")
            
class InputForm(QWidget):
   def __init__(self, parent):
       super(QWidget, self).__init__(parent)
       self.layout = QFormLayout(self)
       self.textfield = QLineEdit(self)
       #self.textfield.setStyleSheet("QLineEdit { background-color: #92a8d1; border-style: outset;}")
       self.textfield.setPlaceholderText("enter some hashtag !")

       self.layout.addRow("HashTag", self.textfield)
       self.setLayout(self.layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
