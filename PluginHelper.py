import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import InstalledPlugins_ForGUI
import InstalledPluginsGUI

def main():
    app = QtWidgets.QApplication(sys.argv)

    loading_window = InstalledPluginsGUI.Ui_LoadingBar()
    loading_window.show()

    categories, all_dicts = InstalledPlugins_ForGUI.get_plugins()
    main_window = InstalledPluginsGUI.Window(categories, all_dicts, loading_window=loading_window)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()