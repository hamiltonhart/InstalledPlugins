import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import InstalledPlugins_ForGUI
import InstalledPluginsGUI

def main():
    app = QtWidgets.QApplication(sys.argv)

    categories = InstalledPlugins_ForGUI.get_plugins()
    name = InstalledPlugins_ForGUI.get_computername()
    main_window = InstalledPluginsGUI.Window(categories, computername=name, loading_window=None)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()