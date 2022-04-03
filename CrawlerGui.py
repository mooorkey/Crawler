from cgitb import text
import os
from random import randint
import sys
from time import process_time_ns
from tkinter import dialog
from tkinter.font import BOLD, NORMAL
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Crawler'
        self.width = 800
        self.height = 650
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width ,self.height)

        # Move window to center of the screen
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        
        self.table_widget = MainTable(self)
        self.setCentralWidget(self.table_widget)
        
        self.show()
    
class MainTable(QWidget):
    
   def __init__(self, parent):
      super(QWidget, self).__init__(parent)
      self.layout = QVBoxLayout()
      
      # Initialize tab screen
      self.tabs = QTabWidget()
      self.twitter_tab = twitter_tab(self)
      self.web_crawling_tab = web_crawling_tab(self)
      self.tabs.resize(300,200)
      
      # Add tabs
      self.tabs.addTab(self.twitter_tab,"TwitterAPI Crawling")
      self.tabs.addTab(self.web_crawling_tab,"Web Crawling")

      # Useful
      self.twitter_tab.get_info_button.clicked.connect(self.get_info_on_click)
      self.twitter_tab.twitter_table.horizontalHeader().sectionClicked.connect(self.get_info_on_click)
      self.twitter_tab.twitter_table.verticalHeader().sectionClicked.connect(self.get_info_on_click)

      # Add tabs to widget
      self.layout.addWidget(self.tabs)
      self.setLayout(self.layout)

   @pyqtSlot()
   def get_info_on_click(self):
      text = self.twitter_tab.twitter_input_box.textfield.text()
      self.twitter_tab.twitter_table.setRowCount(100)
      self.twitter_tab.twitter_table.setColumnCount(100)
      for i in range(100):
         for j in range(100):
            self.twitter_tab.twitter_table.setItem(i,j,QTableWidgetItem(text))
      QMessageBox.about(self,"test",f"input {text}")
            
class InputForm(QWidget):
   def __init__(self, parent, text):
       super(QWidget, self).__init__(parent)
       self.layout = QFormLayout(self)
       self.textfield = QLineEdit(self)
       #self.textfield.setStyleSheet("QLineEdit { background-color: #92a8d1; border-style: outset;}")
       self.textfield.setPlaceholderText("enter some hashtag !")

       self.layout.addRow(text, self.textfield)
       self.setLayout(self.layout)

class twitter_tab(QWidget):
   def __init__(self, parent):
      super().__init__(parent)
      # Twitter tab 
      self.layout = QGridLayout(self)
      self.twitter_input_form_layout = QHBoxLayout()
      self.twitter_datetime_picker_layout = QGridLayout()
      self.get_info_button = QPushButton(parent=self,text="Get Info.")
      self.twitter_input_box = InputForm(parent=self, text="Hashtag")
      self.twitter_table = QTableWidget(parent=self)

      # Date picker
      self.datepicker_start_label = QLabel("Start date")
      self.datepicker_start_label.setStyleSheet("font-weight: bold")
      self.datepicker_start = QDateEdit()
      self.datepicker_start.setCalendarPopup(True)
      self.datepicker_start.setDateTime(QDateTime.currentDateTime())

      self.datepicker_end_label = QLabel("End date")
      self.datepicker_end_label.setStyleSheet("font-weight: bold")
      self.datepicker_end = QDateEdit()
      self.datepicker_end.setCalendarPopup(True)
      self.datepicker_end.setDateTime(QDateTime.currentDateTime().addDays(1))    

      # Add sub layout to main layout
      self.twitter_input_form_layout.addWidget(self.twitter_input_box)
      self.twitter_input_form_layout.addWidget(self.get_info_button)

      self.twitter_datetime_picker_layout.addWidget(self.datepicker_start_label, 0, 0, Qt.AlignmentFlag.AlignCenter)
      self.twitter_datetime_picker_layout.addWidget(self.datepicker_start, 1, 0, Qt.AlignmentFlag.AlignCenter)
      self.twitter_datetime_picker_layout.addWidget(self.datepicker_end_label, 0, 1, Qt.AlignmentFlag.AlignCenter)
      self.twitter_datetime_picker_layout.addWidget(self.datepicker_end, 1, 1, Qt.AlignmentFlag.AlignCenter)

      self.layout.addLayout(self.twitter_input_form_layout, 0, 0, Qt.AlignmentFlag.AlignTop)
      self.layout.addLayout(self.twitter_datetime_picker_layout, 1, 0)
      self.layout.addWidget(self.twitter_table, 2, 0)
      self.setLayout(self.layout)

class web_crawling_tab(QWidget):
   def __init__(self, parent):
      super().__init__(parent)
      jan = 'Janaury'
      feb = 'February'
      mar = 'March'
      apr = 'April'
      may = 'May'
      jun = 'June'

      self.layout = QGridLayout(self)
      self.button_layout = QHBoxLayout()
      self.web_list_layout = QGridLayout()
      self.depth_spinbox_layout = QHBoxLayout()

      self.web_list = QListWidget(self)
      self.add_url_button = QPushButton("Add URL")
      self.remove_url_button = QPushButton("Remove URL")
      self.scrap_button = QPushButton("Scrap")
      self.content_table = QTableWidget(self)

      self.depth_label = QLabel("Depth")
      self.depth_spinbox = QSpinBox(self)

      self.web_list.addItems([jan,feb,mar,apr,may,jun])
      self.web_list.setFixedSize(400,50)

      self.content_table.setFixedSize(700,400)

      self.add_url_button.clicked.connect(self.add_item)
      self.remove_url_button.clicked.connect(self.remove_item)
      self.scrap_button.clicked.connect(self.scrap_action)
      self.web_list.currentItemChanged.connect(self.item_changed)

      # Sub layout
      self.button_layout.addWidget(self.add_url_button)
      self.button_layout.addWidget(self.remove_url_button)

      self.depth_spinbox_layout.addWidget(self.depth_label)
      self.depth_spinbox_layout.addWidget(self.depth_spinbox)

      self.web_list_layout.addWidget(self.web_list,0,0)
      self.web_list_layout.addWidget(self.scrap_button,2,0)

      # Main layout
      self.layout.addLayout(self.button_layout,0,0,Qt.AlignmentFlag.AlignCenter)
      self.layout.addLayout(self.depth_spinbox_layout,1,0,Qt.AlignmentFlag.AlignCenter)
      self.layout.addLayout(self.web_list_layout,2,0,Qt.AlignmentFlag.AlignCenter)
      self.layout.addWidget(self.content_table,3,0,Qt.AlignmentFlag.AlignCenter)
      self.setLayout(self.layout)

   @pyqtSlot()
   def add_item(self):
      self.dialog = QInputDialog(self)
      self.dialog.setInputMode(QInputDialog.TextInput)
      self.dialog.setWindowTitle('Add URL')
      self.dialog.setLabelText('Enter URL')
      self.dialog.setWindowFlag(Qt.WindowContextHelpButtonHint,False)
      lineEdit = self.dialog.findChild(QLineEdit)
      lineEdit.setPlaceholderText('e.g. https://www.imdb.com/')
      if self.dialog.exec_():
         text = self.dialog.textValue() 
         if text.startswith("https"):
            self.web_list.addItem(self.dialog.textValue())
         else:
            QMessageBox.critical(self,"Error","URL must start with https !")
            self.add_item()
   
   def remove_item(self):
      # Check if there is selected item
      print(self.web_list.currentRow())
      if self.web_list.currentRow() == -1:
         QMessageBox.critical(self,"Error","Select item before remove !")
      else:
         self.web_list.takeItem(self.web_list.currentRow())
         
   def item_changed(self):
      print("item changed!")

   def scrap_action(self):
      print("hi")
      self.content_table.setRowCount(100)
      self.content_table.setColumnCount(100)
      for i in range(100):
         for j in range(100):
            self.content_table.setItem(i,j,QTableWidgetItem(f"test {randint(0,100)}"))
      
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
