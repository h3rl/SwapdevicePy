import json
import os
import subprocess
import sys

from PySide2 import QtCore, QtGui, QtWidgets

appVersion = "2.1"
appName = "Change Device"


#   TODO
#   * closes after about is pressed
#

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    """
    CREATE A SYSTEM TRAY ICON CLASS AND ADD MENU
    """
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip(f'ChangeSound')
        menu = QtWidgets.QMenu(parent)
        change_device = menu.addAction("Change Device")
        change_device.triggered.connect(self.change_device)

        menu.addSeparator()

        exit_ = menu.addAction("Exit")
        exit_.triggered.connect(lambda: sys.exit())

        about_ = menu.addAction("About")
        about_.triggered.connect(self.showabout)

        self.setContextMenu(menu)
        self.activated.connect(self.onTrayIconActivated)
        
        self.loadConfig()

    def onTrayIconActivated(self, reason):
        """
        This function will trigger function on double click
        :param reason:
        :return:
        """
        if reason == self.DoubleClick:
            self.change_device()

    def showabout(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("\nMade by H3rl\nver "+appVersion)
        msg.setWindowTitle("About "+appName)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        #msg.setStyleSheet("QLabel{min-width: 150px;}")
        msg.exec_()

    
    def loadConfig(self):
        exists = os.path.exists("./config.json")
        if not exists:
            self.data = {
                "current": "Headset",
                "list": ["Speakers", "Headset"],
                "alerts":True
            }
        else:
            handle = open("config.json","r")
            self.data = json.load(handle)
            handle.close()

    def change_device(self):
        self.loadConfig()
        list = self.data["list"]
        current = self.data["current"]
        alerts = self.data["alerts"]

        newcurr = list.index(current) + 1
        if newcurr >= len(list):
            newcurr = 0
        current = list[newcurr]
        subprocess.call(f"nircmd setdefaultsounddevice {current} 1 & nircmd setdefaultsounddevice {current} 2", shell=True)

        if alerts:
            self.showMessage("Device Changed",current,QtGui.QIcon("assets/"+current+".png"))
        
        self.data["current"] = current

        print(self.data)
        self.saveConfig()

    def saveConfig(self):
        handle = open("config.json","w+")
        stringified = json.dumps(self.data, sort_keys=True, indent=4)
        handle.write(stringified)
        handle.close()
            

def main():
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon("assets/icon.png"), widget)
    tray_icon.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
