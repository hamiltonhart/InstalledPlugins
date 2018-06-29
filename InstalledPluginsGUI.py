import os
import csv
from PyQt5 import QtWidgets, QtCore, QtGui
import InstalledPlugins_ForGUI


# Creates a QTable Widget. Primarily to display and handle data to be viewed. Requires row and column upon creation.
class ListView(QtWidgets.QTableWidget):
    def __init__(self, r, c, *args):
        super().__init__(r, c)

        header_labels = [arg for arg in args]
        self.setHorizontalHeaderLabels(header_labels)
        self.display_total = 0

        self.show()

    # Populates the table. If append is False, the table is cleared first. Count is incremented if multiple iterables
    #  are to be displayed.
    def addItem(self, csv_iterable, append=False, count=0):
        if not append and count == 0:
            self.setRowCount(0)
            self.display_total = 0

        for row_item in csv_iterable:
            row = self.rowCount()
            self.insertRow(row)
            row_contents = [item for item in row_item.split(',')]
            for column, row_content in enumerate(row_contents):
                row_content = QtWidgets.QTableWidgetItem(row_content)
                self.setItem(row, column, row_content)
            self.display_total += 1

    # Writes the information in the table to a csv file.
    def save_sheet(self):
        path = QtWidgets.QFileDialog.getSaveFileName(self, "Save CSV", os.getenv("HOME"), "CSV.csv")
        if path[0] != "":
            with open(path[0] + '.csv', "w") as csv_file:
                writer = csv.writer(csv_file, dialect="excel")
                for row in range(self.rowCount()):
                    row_data = []
                    for column in range(self.columnCount()):
                        item = self.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append("")
                    writer.writerow(row_data)

    # Resets the table to 0 rows, effectively clearing it.
    def clear_all(self):
        self.setRowCount(0)
        self.display_total = 0


# Defines the main window
class Window(QtWidgets.QWidget):
    def __init__(self, categories, all_dicts, loading_window=None):
        super(Window, self).__init__()

        if loading_window != None:
            loading_window.close()
        else:
            print("No loading window")
        self.categories = categories
        self.all_dicts = all_dicts

        self.init_ui()

    def init_ui(self):
        # Name and dimension of the window are defined.
        self.setWindowTitle("Plugins")
        self.setMaximumWidth(700)
        self.setMinimumWidth(450)
        self.setMinimumHeight(500)

        # Various layouts are defined
        v_box_main = QtWidgets.QVBoxLayout()
        h_box_top = QtWidgets.QHBoxLayout()
        h_box_mid_1 = QtWidgets.QHBoxLayout()
        # h_box_mid_1.addStretch()
        v_box_1_h_mid_1 = QtWidgets.QVBoxLayout()
        h_box_1_v_box_1 = QtWidgets.QHBoxLayout()
        v_box_2_h_mid_1 = QtWidgets.QVBoxLayout()
        v_box_checkboxes = QtWidgets.QVBoxLayout()
        h_box_buttons = QtWidgets.QHBoxLayout()
        h_box_search = QtWidgets.QHBoxLayout()
        v_box_chk_btns = QtWidgets.QVBoxLayout()
        h_box_chk_options = QtWidgets.QHBoxLayout()
        h_box_view_options = QtWidgets.QHBoxLayout()

        # Layouts are added together accordingly
        self.setLayout(v_box_main)
        v_box_main.addLayout(h_box_top)
        v_box_main.addLayout(h_box_mid_1)
        v_box_chk_btns.addLayout(h_box_buttons)
        v_box_chk_btns.addLayout(h_box_chk_options)
        v_box_chk_btns.addLayout(h_box_search)
        v_box_chk_btns.addLayout(h_box_view_options)

        h_box_top.addLayout(v_box_checkboxes)
        h_box_top.addLayout(v_box_chk_btns)
        h_box_top.addStretch(1)
        h_box_mid_1.addLayout(v_box_1_h_mid_1)
        h_box_mid_1.addLayout(v_box_2_h_mid_1)

        # Plugin type checkboxes are created. The categories dictionary keys created by class plugins from below are
        # used for the labels.
        self.checkbox_labels = [x for x in self.categories.keys()]
        self.checkboxes = {}
        for chk_label in self.checkbox_labels:
            self.chk_label = chk_label
            self.checkboxes[chk_label] = QtWidgets.QCheckBox(self.chk_label)
            v_box_checkboxes.addWidget(self.checkboxes[chk_label])

        # Sets the All Plugins checkbox to default checked.
        for label in self.checkbox_labels[:-1]:
            self.checkboxes[label].clicked.connect(self.uncheck_allplugins_box)
        self.checkboxes["All Plugins"].setChecked(True)

        # Sets primary buttons. Other buttons may be added? Create a buttons class?
        btn_labels = ["View", "Export"]
        btns = {}
        for btn_label in btn_labels:
            self.btn_label = btn_label
            btns[btn_label] = QtWidgets.QPushButton(self.btn_label)
            h_box_buttons.addWidget(btns[btn_label], 0, QtCore.Qt.AlignBottom)

        # Options checkboxes are created. Needed tooltips are created
        self.export_sep_files = QtWidgets.QCheckBox("Export Categories")
        self.export_sep_files.setChecked(True)
        self.export_sep_files.setToolTip("Exports the selected plugin types/locations into separate files. "
                                         "Type/location will be appended to the filename supplied for clarity.")
        self.append_check = QtWidgets.QCheckBox("Append")

        self.export_displayed_button = QtWidgets.QCheckBox("Export Displayed")
        self.export_displayed_button.setToolTip("Exports only what is displayed in the box below regardless of "
                                                "selection on the left.")

        h_box_chk_options.addWidget(self.export_sep_files, 0, QtCore.Qt.AlignTop)
        h_box_chk_options.addWidget(self.export_displayed_button, 0, QtCore.Qt.AlignTop)

        # Instance of the table view is created. Header labels are defined.
        self.text_display = ListView(0, 3, "Plugin", "Version", "Type")
        self.display_total = QtWidgets.QLabel("Total Displayed: " + str(self.text_display.display_total))

        # Search button, bar and clear button are created. When ENTER is pressed, search button activates
        self.search_box = QtWidgets.QLineEdit()
        self.search_box.setPlaceholderText("Enter plugin to search...")
        self.search_btn = QtWidgets.QPushButton("Search")
        self.clear_btn = QtWidgets.QPushButton("Clear")
        self.search_box.returnPressed.connect(self.search_box_input)
        v_box_1_h_mid_1.addWidget(self.search_box)
        v_box_1_h_mid_1.addLayout(h_box_1_v_box_1)
        h_box_1_v_box_1.addWidget(self.append_check)
        h_box_1_v_box_1.addSpacing(50)
        h_box_1_v_box_1.addWidget(self.display_total)
        h_box_1_v_box_1.addStretch(1)
        v_box_2_h_mid_1.addWidget(self.search_btn)
        v_box_2_h_mid_1.addWidget(self.clear_btn)

        v_box_main.addWidget(self.text_display)

        self.search_btn.clicked.connect(self.search_box_input)
        self.clear_btn.clicked.connect(self.clear_button_click)

        btns["Export"].clicked.connect(lambda: self.text_display.save_sheet() if self.export_displayed_button.isChecked()
                                       else self.export_button_click())
        btns["View"].clicked.connect(self.view_button_click)
        self.checkboxes["All Plugins"].clicked.connect(self.all_plugins_checked)

        self.show()

    def search_box_input(self):
        append = False
        if self.append_check.isChecked():
            append = True
        text_results = [x.gui_output() for x in InstalledPlugins_ForGUI.search_dicts(self.search_box.text().lower(),
                                                                            self.all_dicts)]
        self.text_display.addItem(text_results, append=append)
        self.show_view_total()

    def view_button_click(self):
        append = False
        if self.append_check.isChecked():
            append = True
        search_categories = [cat for cat in self.categories.keys()]
        if self.checkboxes["All Plugins"].isChecked():
            count = 0
            for category in search_categories[:-1]:
                text_results = InstalledPlugins_ForGUI.list_dicts(self.categories[category])
                self.text_display.addItem(text_results, append=append, count=count)
                count += 1

        else:
            count = 0
            for item in search_categories[:-1]:
                if self.checkboxes[item].isChecked():
                    text_results = InstalledPlugins_ForGUI.list_dicts(self.categories[item])
                    self.text_display.addItem(text_results, append=append, count=count)
                    count += 1

        self.show_view_total()

    def export_button_click(self):  # Needs updating?
        path = QtWidgets.QFileDialog.getSaveFileName(self, "Save CSV", os.getenv("HOME"), "CSV.csv")
        if path != '':
            if self.checkboxes["All Plugins"].isChecked() and self.export_sep_files.isChecked():
                InstalledPlugins_ForGUI.export_plugins_list(path[0], self.all_dicts, [x for x in
                                                                     self.categories.keys()],sep_files=True)
            elif self.checkboxes["All Plugins"].isChecked():
                InstalledPlugins_ForGUI.export_plugins_list(path[0], self.all_dicts, [x for x in
                                                                                      self.categories.keys()])
            elif not self.export_sep_files.isChecked():
                to_export = []
                for item in self.categories:
                    if self.checkboxes[item].isChecked():
                        to_export.append(self.categories[item])
                InstalledPlugins_ForGUI.export_plugins_list(path[0], to_export, [x for x in self.categories.keys()],
                                                            all_plugins=False)
            else:
                for i, item in enumerate(self.categories):
                    if self.checkboxes[item].isChecked():
                        InstalledPlugins_ForGUI.export_plugins_list(path[0], self.categories[item], item,
                                                                    all_plugins=False,
                                                                    sep_files=True)

    def clear_button_click(self):
        self.text_display.clear_all()
        self.show_view_total()


    def all_plugins_checked(self):
        for label in self.checkbox_labels:
            if label == "All Plugins":
                pass
            else:
                self.checkboxes[label].setChecked(False)

    def uncheck_allplugins_box(self):
        if self.checkboxes["All Plugins"].isChecked():
            self.checkboxes["All Plugins"].setChecked(False)

    def show_view_total(self):
        if self.text_display.display_total == 0:
            total = "0"
        else:
            total = str(self.text_display.display_total)

        self.display_total.setText("Total Displayed: {}".format(total))

class Ui_LoadingBar(QtWidgets.QWidget):
   def __init__(self):
       super(Ui_LoadingBar, self).__init__()

       self.setupUi()
       # self.show()

   def setupUi(self):
       self.setObjectName("LoadingBar")
       self.resize(598, 107)
       self.setMinimumSize(QtCore.QSize(598, 107))
       self.setMaximumSize(QtCore.QSize(598, 107))
       self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
       self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
       self.verticalLayout_2.setObjectName("verticalLayout_2")
       self.v_layout_top = QtWidgets.QVBoxLayout()
       self.v_layout_top.setObjectName("v_layout_top")
       self.label = QtWidgets.QLabel(self)
       self.label.setObjectName("label")
       self.v_layout_top.addWidget(self.label, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
       self.verticalLayout_2.addLayout(self.v_layout_top)
       self.v_layout_btm = QtWidgets.QVBoxLayout()
       self.v_layout_btm.setObjectName("v_layout_btm")
       self.progressBar = QtWidgets.QProgressBar(self)
       self.progressBar.setMinimumSize(QtCore.QSize(572, 20))
       self.progressBar.setMaximumSize(QtCore.QSize(572, 20))
       self.progressBar.setProperty("value", 24)
       self.progressBar.setObjectName("progressBar")
       self.v_layout_btm.addWidget(self.progressBar, 0, QtCore.Qt.AlignTop)
       self.verticalLayout_2.addLayout(self.v_layout_btm)

       self.retranslateUi()
       QtCore.QMetaObject.connectSlotsByName(self)

   def retranslateUi(self):
       _translate = QtCore.QCoreApplication.translate
       self.setWindowTitle(_translate("LoadingBar", "Plugin Progress"))
       self.label.setText(_translate("LoadingBar", "<html><head/><body><p>"
                                                   "<span style=\" font-size:18pt; font-weight:600;\">"
                                                   "Loading Plugins...</span></p></body></html>"))


"""Creates a list (all_dicts) from the return of the function call.
Creates a list (category_item) from the keys of a dictionary in the imported module. The dictionary the keys are
derived from is iterated over to get the return of create_new_classes().
Creates a categories dictionary from the above lists using the category_item list as the key and all_dicts as the 
value.
Finally, the all_dicts list is added to the categories dictionary.
"""
def main():
    pass

if __name__ == "__main__":
    main()

