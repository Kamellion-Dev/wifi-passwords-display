#--------------------- APP-1 ---------------------#

from pickle import GLOBAL
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow,QDialog, QApplication
import subprocess
import re

class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        loadUi('Wifi_Cloak.ui', self)
        
        # ~~---------- Ui Logic -------------~~
        
        # set the page base settings
        self.setWindowTitle("Wifi Cloak")
        self.setFixedSize(800, 504)
        width = 160
        self.tableWidget.setColumnWidth(0, width)
        self.tableWidget.setColumnWidth(1, width)
        self.tableWidget.setColumnWidth(2, width)
        
        # Scanning Button + Function
        self.pushButton1.clicked.connect(lambda:self.show_profiles())

        # TODO : Search Button
        self.pushButton2.clicked.connect(lambda:self.search_profiles())
    
    def search_profiles(self):
        search_value = self.searchText.toPlainText()
        if search_value != "":
            self.find_profile(search_value)
    
    def find_profile(self, find_value):
        # Clear Previous Data
        self.tableWidget.setRowCount(0)
        self.rowCount = 0 
        
        # Get the data from the table
        command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()
        profile_names = (re.findall("All User Profile     : (.*)\r", command_output))
        wifi_list = []
        
        # Working on the List of Profiles
        if len(profile_names) != 0:
            for name in profile_names:
                #    Every wifi connection will need its own dictionary which 
                #    will be appended to the variable wifi_list.
                wifi_profile = {}

                profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
                if re.search("Security key           : Absent", profile_info):
                    continue
                else:
                    # ~~~---------- Getting the SSID -------------~~
                    wifi_profile["ssid"] = name
                    profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
                    
                    # ~~~---------- Getting the Password -------------~~
                    password = re.search("Key Content            : (.*)\r", profile_info_pass)
                    if password == None:
                        wifi_profile["password"] = None
                    else:
                        wifi_profile["password"] = password[1]
                        
                    # ~~~---------- Getting the Password -------------~~
                    encryption_type = re.search("Authentication         : (.*)\r", profile_info_pass)
                    if encryption_type == None:
                        wifi_profile["encryption"] = None
                    else:
                        wifi_profile["encryption"] = encryption_type[1]
                    
                    wifi_list.append(wifi_profile) 
            
            for x in range(len(wifi_list)):
                # if find_value.lower().search(wifi_list[x]["ssid"].lower()):
                if re.search(find_value.lower(), wifi_list[x]["ssid"].lower()):
                    # print that matched value to the table
                    self.loadData(wifi_list[x]["ssid"], wifi_list[x]["encryption"] ,wifi_list[x]["password"])
      
    def show_profiles(self):
        # Clear Previous Data
        self.tableWidget.setRowCount(0)
        self.rowCount = 0 
        
        # Get the data from the table
        command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()
        profile_names = (re.findall("All User Profile     : (.*)\r", command_output))
        wifi_list = []
        
        # Working on the List of Profiles
        if len(profile_names) != 0:
            for name in profile_names:
                #    Every wifi connection will need its own dictionary which 
                #    will be appended to the variable wifi_list.
                wifi_profile = {}

                profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
                if re.search("Security key           : Absent", profile_info):
                    continue
                else:
                    # ~~~---------- Getting the SSID -------------~~
                    wifi_profile["ssid"] = name
                    profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
                    
                    # ~~~---------- Getting the Password -------------~~
                    password = re.search("Key Content            : (.*)\r", profile_info_pass)
                    if password == None:
                        wifi_profile["password"] = None
                    else:
                        wifi_profile["password"] = password[1]
                        
                    # ~~~---------- Getting the Password -------------~~
                    encryption_type = re.search("Authentication         : (.*)\r", profile_info_pass)
                    if encryption_type == None:
                        wifi_profile["encryption"] = None
                    else:
                        wifi_profile["encryption"] = encryption_type[1]
                    
                    wifi_list.append(wifi_profile) 
            
            for x in range(len(wifi_list)):
                # print(wifi_list[x]["ssid"]+wifi_list[x]["password"])
                self.loadData(wifi_list[x]["ssid"], wifi_list[x]["encryption"] ,wifi_list[x]["password"])
    
    # Storing Row Count in a variable
    rowCount = 0      
    def loadData(self, ssid = None, encryption = None , password = None):
        m_query=[{
            "wifi_name": ssid,
            "wifi_encryption": encryption,
            "wifi_password": password
        }]
        self.tableWidget.setRowCount(self.rowCount+1)
        
        for profile in m_query:
            self.tableWidget.setItem(self.rowCount, 0, QtWidgets.QTableWidgetItem(profile["wifi_name"]))
            self.tableWidget.setItem(self.rowCount, 1, QtWidgets.QTableWidgetItem(str(profile["wifi_encryption"])))
            self.tableWidget.setItem(self.rowCount, 2, QtWidgets.QTableWidgetItem(profile["wifi_password"]))
        self.rowCount=self.rowCount+1
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Main()
    ui.show()
    app.exec_() 