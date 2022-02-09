import json
import os
import subprocess
import sys

from PySide2 import QtCore, QtGui, QtWidgets

appVersion = "1.7"
appName = "Change Device"

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

        #about_ = menu.addAction("About")
        #about_.triggered.connect(self.showabout)

        self.setContextMenu(menu)
        self.activated.connect(self.onTrayIconActivated)

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
        msg.setStyleSheet("QLabel{min-width: 150px;}");
        msg.exec_()

    def change_device(self):
        """
        this function will change default sound device and r/w config.json
        :return:
        """
        filesize = os.stat("config.json").st_size
        handle = open("config.json","r+")
        if filesize == 0:
            handle.write(json.dumps({
                "current": "Headset",
                "list": [
                    "Speakers",
                    "Headset"
                ],
                "alerts": True
            }, sort_keys=True, indent=4))
            handle.close()
        else:
            data = json.load(handle)
            handle.close()
            
            newcurr = data["list"].index(data["current"])+1
            if newcurr >= len(data["list"]):
                newcurr = 0
            data["current"] = data["list"][newcurr]
            cmd = "nircmd setdefaultsounddevice " + data["current"] + " 1 & nircmd setdefaultsounddevice " + data["current"] + " 2"
            subprocess.call(cmd, shell=True)
            if data["alerts"]:
                self.showMessage("Device Changed",data["current"],QtGui.QIcon("assets/"+data["current"]+".png"))
            handle = open("config.json","w+")
            handle.write(json.dumps(data, sort_keys=True, indent=4))
            handle.close()
            

def main():
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon("assets/icon.png"), widget)
    tray_icon.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
