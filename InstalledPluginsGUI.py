import os
import csv
from PyQt5 import QtWidgets, QtCore, QtGui
import InstalledPlugins_ForGUI


# Creates a QTable Widget. Primarily to display and handle data to be viewed. Requires row and column upon creation.
class ListView(QtWidgets.QTableWidget):

    def __init__(self, r, c, *args):
        super().__init__(r, c)

        """Creates headers and sets the resize mode. Display total is set to 0."""

        header_labels = [arg for arg in args]
        self.setHorizontalHeaderLabels(header_labels)
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.display_total = 0

        self.show()
    def addItem(self, csv_iterable, append=False, count=0):
        """Populates the table. If append is False, the table is cleared first.
        Count is used to display multiple iterables as it is incremented in the calling function or set
        self.display_total to 0.
        Append allows for multiple calls at different times. Count allows for multiple calls within an iterable.
        self.display_total is incremented.
        """
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

    def addComputerName(self, name):
        # Currently not used.
        """Not sure what this is supposed to do..."""
        print(name)
        row = self.rowCount()
        self.insertRow(row)
        row_content = QtWidgets.QTableWidgetItem(name)
        self.setItem(row, 0, row_content)

    def save_sheet(self):
        """Writes the information in the table to a csv file.
        Iterates over each row then each column and creates a list. This list is written to the csv file.
        """
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

    def clear_all(self):
        # Resets the table to 0 rows, effectively clearing it.
        self.setRowCount(0)
        self.display_total = 0

class InputWindow(QtWidgets.QDialog):
    def __init__(self, window_title):
        super(InputWindow, self).__init__()

        self.text_input = ''

        # Sets the window title and creates the primary layout
        self.setWindowTitle(window_title)
        h_box_layout = QtWidgets.QHBoxLayout()
        self.setLayout(h_box_layout)

        # Text input box
        self.text_input = QtWidgets.QLineEdit()
        self.text_input.setPlaceholderText("Enter text here...")
        self.text_input.setMaximumWidth(200)
        self.text_input.setMinimumWidth(200)
        h_box_layout.addWidget(self.text_input, QtCore.Qt.AlignLeft)

        # Ok and Cancel Buttons
        self.ok_btn = QtWidgets.QPushButton("Ok")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        h_box_layout.addWidget(self.ok_btn, QtCore.Qt.AlignLeft)
        h_box_layout.addWidget(self.cancel_btn, QtCore.Qt.AlignLeft)

        #  Ok and Cancel Buttons method assignment
        self.ok_btn.clicked.connect(self.ok_btn_click)
        self.cancel_btn.clicked.connect(self.cancel_btn_click)

        self.show()

    def ok_btn_click(self):
        self.return_text()
        self.accept()

    def cancel_btn_click(self):
        self.close()

    def return_text(self):
        self.input_text = self.text_input.text()

class ConfirmWindow(QtWidgets.QDialog):
    def __init__(self, message_text):
        super(ConfirmWindow, self).__init__()

        v_box_layout = QtWidgets.QHBoxLayout()
        self.setLayout(v_box_layout)

        self.message = QtWidgets.QLabel(message_text)
        self.ok_btn = QtWidgets.QPushButton("Ok")
        self.ok_btn.clicked.connect(self.ok_btn_click)
        v_box_layout.addWidget(self.message, QtCore.Qt.AlignCenter)
        v_box_layout.addWidget(self.ok_btn, QtCore.Qt.AlignCenter)

    def ok_btn_click(self):
        self.accept()

# Defines the main window
class Window(QtWidgets.QWidget):
    def __init__(self, categories, computername=None, loading_window=None):
        super(Window, self).__init__()

        if loading_window != None:
            loading_window.close()
        else:
            print("No loading window")
        self.categories = categories
        self.all_systems = {computername: self.categories}
        self.sep_files = True
        self.export_all = True
        self.all_checked = True
        self.init_ui()

    def init_ui(self):
        # Name and dimension of the window are defined.
        self.setWindowTitle("Plugins")
        self.setMaximumWidth(700)
        self.setMinimumWidth(545)
        self.setMinimumHeight(600)

        # Various layouts are defined
        v_box_main = QtWidgets.QVBoxLayout()
        h_box_top = QtWidgets.QHBoxLayout()
        h_box_mid_1 = QtWidgets.QHBoxLayout()
        v_box_1_h_mid_1 = QtWidgets.QVBoxLayout()
        h_box_1_v_box_1 = QtWidgets.QHBoxLayout()
        v_box_2_h_mid_1 = QtWidgets.QVBoxLayout()
        v_box_checkboxes = QtWidgets.QVBoxLayout()
        h_box_buttons = QtWidgets.QHBoxLayout()
        h_box_search = QtWidgets.QHBoxLayout()
        v_box_chk_btns = QtWidgets.QVBoxLayout()
        h_box_chk_options = QtWidgets.QHBoxLayout()
        h_box_view_options = QtWidgets.QHBoxLayout()
        room_box_layout = QtWidgets.QHBoxLayout()
        add_room_layout = QtWidgets.QHBoxLayout()

        # Layouts are added together accordingly
        self.setLayout(v_box_main)
        v_box_main.addLayout(h_box_top)
        v_box_main.addLayout(h_box_mid_1)
        v_box_chk_btns.addLayout(room_box_layout)
        v_box_chk_btns.addLayout(add_room_layout)
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
        for checkbox_label in self.checkbox_labels:
            self.chk_label = checkbox_label
            self.checkboxes[checkbox_label] = QtWidgets.QCheckBox(self.chk_label)
            v_box_checkboxes.addWidget(self.checkboxes[checkbox_label])

        # Sets the All Plugins checkbox to default checked.
        for label in self.checkbox_labels[:-1]:
            self.checkboxes[label].clicked.connect(self.uncheck_allplugins_box)
        self.checkboxes["All Plugins"].setChecked(True)
        self.checkboxes["All Plugins"].clicked.connect(self.all_plugins_checked)

        # Creates assigns methods to and adds to room_box_layout for room_selection ComboBox and Rename Button
        self.room_selection = QtWidgets.QComboBox()
        self.room_selection.currentTextChanged.connect(self.change_current_dict)
        for key in self.all_systems.keys():
            self.room_selection.addItem(key)
        room_box_layout.addWidget(self.room_selection)

        self.rename_system_btn = QtWidgets.QPushButton("Rename")
        self.rename_system_btn.setMaximumWidth(100)
        self.rename_system_btn.setMinimumWidth(100)
        self.rename_system_btn.clicked.connect(self.rename_system)
        room_box_layout.addWidget(self.rename_system_btn, QtCore.Qt.AlignRight)

        # Creates assigns methods to and adds to room_box_layout for Add Room button and room name box
        self.enter_room_name_box = QtWidgets.QLineEdit()
        self.enter_room_name_box.setPlaceholderText("Enter New Room Name...")
        self.enter_room_name_box.returnPressed.connect(self.add_room)
        add_room_layout.addWidget(self.enter_room_name_box)

        self.add_room_btn = QtWidgets.QPushButton("Add Room")
        self.add_room_btn.setToolTip("In Finder: Connect to a server 'Command + K'\n Click 'Add Room' and point to "
                                     "the remote hard disk.")
        self.add_room_btn.clicked.connect(self.add_room)
        add_room_layout.addWidget(self.add_room_btn)

        # Sets View and Export Buttons, assigns methods and adds to layout
        btn_labels = ["View", "Export"]
        btns = {}
        for btn_label in btn_labels:
            self.btn_label = btn_label
            btns[btn_label] = QtWidgets.QPushButton(self.btn_label)
            h_box_buttons.addWidget(btns[btn_label], 0, QtCore.Qt.AlignBottom)

        btns["Export"].clicked.connect(
            lambda: self.text_display.save_sheet() if self.export_displayed_button.isChecked()
            else self.export_button_click())
        btns["View"].clicked.connect(self.view_button_click)

        # Options checkboxes are created. Needed tooltips are created.
        self.export_sep_files = QtWidgets.QCheckBox("Export As Type")
        self.export_sep_files.setChecked(True)
        self.export_sep_files.setToolTip("Exports the selected plugin types/locations into separate files. "
                                         "Type/location will be appended to the filename supplied for clarity.")
        self.export_sep_files.clicked.connect(self.sep_files_checked)
        h_box_chk_options.addWidget(self.export_sep_files, 0, QtCore.Qt.AlignTop)

        self.export_displayed_button = QtWidgets.QCheckBox("Export Displayed")
        self.export_displayed_button.setToolTip("Exports only what is displayed in the box below regardless of "
                                                "selection on the left.")
        h_box_chk_options.addWidget(self.export_displayed_button, 0, QtCore.Qt.AlignTop)

        self.export_all_systems_button = QtWidgets.QCheckBox("Export All Systems")
        self.export_all_systems_button.setToolTip("Exports all plugins from all loaded systems.")
        self.export_all_systems_button.setChecked(True)
        self.export_all_systems_button.clicked.connect(self.export_all_systems)
        h_box_chk_options.addWidget(self.export_all_systems_button, 0, QtCore.Qt.AlignTop)

        # Search button, bar and clear button are created. When ENTER is pressed, search button activates
        self.search_box = QtWidgets.QLineEdit()
        self.search_box.setPlaceholderText("Enter plugin to search...")
        v_box_1_h_mid_1.addWidget(self.search_box)

        self.search_btn = QtWidgets.QPushButton("Search")
        self.search_btn.clicked.connect(self.search_box_input)
        self.search_box.returnPressed.connect(self.search_box_input)
        v_box_2_h_mid_1.addWidget(self.search_btn)

        self.clear_btn = QtWidgets.QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_button_click)
        v_box_2_h_mid_1.addWidget(self.clear_btn)

        v_box_1_h_mid_1.addLayout(h_box_1_v_box_1)

        self.append_check = QtWidgets.QCheckBox("Append")
        h_box_1_v_box_1.addWidget(self.append_check)
        h_box_1_v_box_1.addSpacing(50)

        # Instance of the table view is created. Header labels are defined.
        self.text_display = ListView(0, 3, "Plugin", "Version", "Type")
        v_box_main.addWidget(self.text_display)

        self.display_total = QtWidgets.QLabel("Total Displayed: " + str(self.text_display.display_total))
        h_box_1_v_box_1.addWidget(self.display_total)
        h_box_1_v_box_1.addStretch(1)

        self.show()

    def change_current_dict(self):
        """Changes the self.categories attribute to the dictionary value in self.all_systems matching the current system
    selected.
        """
        try:
            self.categories = self.all_systems[self.room_selection.currentText()]
            self.text_display.clear_all()
            self.view_button_click()
        except KeyError:
            pass

        except AttributeError:
            pass

    def clear_reorder_room_selection(self, active_room):
        """Clears the self.room_selection box entries. Sorts the self.all_systems keys and assigns them in sorted
        order to the self.room_selection box. The active entry is set to the 'active room' arg.
     """
        self.room_selection.clear()
        for room in sorted(self.all_systems.keys()):
            self.room_selection.addItem(room)
        self.room_selection.setCurrentText(active_room)

    def add_room(self):
        """
        Appends "New Room (+ number of systems)" if no room name is specified
        Asks for the user to point to a directory
        Runs the get plugins function passing the external path kwarg
        """
        if self.enter_room_name_box.text() != '':
            new_room_name = self.enter_room_name_box.text()
        else:
            new_room_name = "New Room {}".format(str(len(self.all_systems) + 1))

        new_room = QtWidgets.QFileDialog.getExistingDirectory()

        if new_room != "":
            categories = InstalledPlugins_ForGUI.get_plugins(external_path=new_room)
            self.all_systems[new_room_name] = categories
            self.clear_reorder_room_selection(new_room_name)
            confirm_window = ConfirmWindow("Plug-Ins for {} have been loaded.".format(new_room_name))
            confirm_window.exec_()
            # self.text_display.clear_all()
            self.enter_room_name_box.setText("")
            self.text_display.clear_all()
            self.checkboxes["All Plugins"].setChecked(True)
            self.all_plugins_checked()
            self.view_button_click()

    def search_box_input(self):
        """
        Checks if self.append is checked.
        Passes the text contents of self.search_box to the InstalledPlugins_ForGUI method which returns a list.
        A list of tuples is created for each item in the returned list.
        That list is passed to the addItem method for the self.text display along with the append boolean.
        Calls self.show_view_total.
        """
        append = False
        if self.append_check.isChecked():
            append = True
        text_results = [x.gui_output() for x in InstalledPlugins_ForGUI.search_dicts(self.search_box.text().lower(),
                                                                                     self.categories["All Plugins"])]
        self.text_display.addItem(text_results, append=append)
        self.show_view_total()

    def view_button_click(self):
        """Checks if self.append is checked and creates a boolean assignment.
        Variable search_categories contains a list of self.category keys (different plugin categories)
        If the "All Plugins" box is checked, all categories are iterated over and an output list is returned,
        the count is incremented.
        That output list, append boolean and count value are used to display information.
        If "All Plugins" is not checked, only the categories checked have lists returned and displayed.
        """
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
            for category in search_categories[:-1]:
                if self.checkboxes[category].isChecked():
                    text_results = InstalledPlugins_ForGUI.list_dicts(self.categories[category])
                    self.text_display.addItem(text_results, append=append, count=count)
                    count += 1

        self.show_view_total()

    def export_button_click(self):  # Needs updating?
        """
        Opens dialog for save location.
        If "All Plugins" is checked, the export_all_systems method is called.
        The InstalledPlugins_ForGUI.export_plugins_list function is called with the correct dictionary(s)
        """
        path = QtWidgets.QFileDialog.getSaveFileName(self, "Save CSV", os.getenv("HOME"), "CSV.csv", )
        if self.export_all:
            self.export_all_systems_option(path[0])

        elif path != '':
            write_path = "_".join(path[0].split(" "))
            if self.checkboxes["All Plugins"].isChecked():
                InstalledPlugins_ForGUI.export_plugins_list(write_path, self.categories["All Plugins"], [x for x in
                                                            self.categories.keys()],
                                                            all_plugins=self.all_checked,
                                                            sep_files=self.sep_files)

            elif not self.export_sep_files.isChecked():
                to_export = []
                for item in self.categories:
                    if self.checkboxes[item].isChecked():
                        to_export.append(self.categories[item])
                InstalledPlugins_ForGUI.export_plugins_list(write_path, to_export, [x for x in self.categories.keys()],
                                                            all_plugins=False)
            else:
                for i, item in enumerate(self.categories):
                    if self.checkboxes[item].isChecked():
                        InstalledPlugins_ForGUI.export_plugins_list(write_path, self.categories[item], item,
                                                                    all_plugins=False,
                                                                    sep_files=True)

    def export_all_systems_option(self, original_path):
        """Similar to the export_button_click method except this creates a parent directory for potentially multiple
        exports. The user input makes the directory which is added to the path. Same otherwise."""
        if original_path != '':
            original_path = "_".join(original_path.split(" "))
            os.system("mkdir {}".format(original_path))

            for system in self.all_systems.keys():
                rename_system = "_".join(system.split(" "))
                new_path = os.path.join(original_path, rename_system)
                self.categories = self.all_systems[system]
                if self.checkboxes["All Plugins"].isChecked():
                    InstalledPlugins_ForGUI.export_plugins_list(new_path, self.categories["All Plugins"], [x for x in
                                                                self.categories.keys()],
                                                                all_plugins=self.all_checked,
                                                                sep_files=self.sep_files)

                elif not self.export_sep_files.isChecked():
                    to_export = []
                    for item in self.categories:
                        if self.checkboxes[item].isChecked():
                            to_export.append(self.categories[item])
                    InstalledPlugins_ForGUI.export_plugins_list(new_path, to_export, [x for x in self.categories.keys()],
                                                                all_plugins=False)
                else:
                    for i, item in enumerate(self.categories):
                        if self.checkboxes[item].isChecked():
                            InstalledPlugins_ForGUI.export_plugins_list(new_path, self.categories[item], item,
                                                                        all_plugins=False,
                                                                        sep_files=True)

    def clear_button_click(self):
        self.text_display.clear_all()
        self.show_view_total()

    def rename_system(self):
        # Opens a text input window which replaces the key of the system dictionary selected.
        rename_dialog_box = InputWindow("Rename System")
        rename_dialog_box.exec_()
        try:
            if rename_dialog_box.input_text != '':
                self.all_systems[rename_dialog_box.input_text] = self.all_systems.pop(self.room_selection.currentText())
            self.clear_reorder_room_selection(rename_dialog_box.input_text)
        except AttributeError:
            pass

    def all_plugins_checked(self):
        # Unchecks other categories if All Plugins is checked.
        for label in self.checkbox_labels:
            if label == "All Plugins":
                pass
            else:
                self.checkboxes[label].setChecked(False)
        self.all_checked = True

    def uncheck_allplugins_box(self):
        if self.checkboxes["All Plugins"].isChecked():
            self.checkboxes["All Plugins"].setChecked(False)

    def sep_files_checked(self):
        if self.sep_files == True:
            self.sep_files = False
        else:
            self.sep_files = True

    def export_all_systems(self):
        if self.export_all == True:
            self.export_all = False
        else:
            self.export_all = True

    def show_view_total(self):
        self.display_total.setText("Total Displayed: {}".format(str(self.text_display.display_total)))

class Ui_LoadingBar(QtWidgets.QDialog):
    def __init__(self, source_class, new_room, new_room_name):
        super(Ui_LoadingBar, self).__init__()

        self.source_class = source_class
        self.new_room = new_room
        self.new_room_name = new_room_name
        self.setupUi()

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

    # def add_room(self):
    #     categories = InstalledPlugins_ForGUI.get_plugins(external_path=self.new_room)
    #     self.source_class.all_systems[self.new_room_name] = categories
    #     confirm_window = ConfirmWindow("Plugins for {} have been loaded.".format(self.new_room_name), self)
    #     confirm_window.exec_()

"""Creates a list (all_dicts) from the return of the function call.
Creates a list (category_item) from the keys of a dictionary in the imported module. The dictionary the keys are
derived from is iterated over to get the return of create_new_classes().
Creates a categories dictionary from the above lists using the category_item list as the key and all_dicts as the 
value.
Finally, the all_dicts list is added to the categories dictionary.
"""
# def main():
#     pass
#
# if __name__ == "__main__":
#     main()

# if new_room != "":

        #     categories = InstalledPlugins_ForGUI.get_plugins(external_path=new_room)
        #     self.all_systems[new_room_name] = categories
        #     self.clear_reorder_room_selection(new_room_name)
        # self.text_display.clear_all()
        # self.enter_room_name_box.setText("")