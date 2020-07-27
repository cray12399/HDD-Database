from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import sys
import os
import pandas


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CPR Database")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setMinimumWidth(1000)
        self.central_widget.setMinimumHeight(500)
        self.central_widget.resize(QSize(1100, 600))

        self.create_menu_bar()
        self.create_main_window_layouts()
        self.create_search_ui()
        self.create_table_ui()

        self.create_users_dialog()
        self.create_edit_user_dialog()
        self.create_search_type_dialog()
        self.create_edit_search_type_dialog()
        self.create_filter_window()
        self.create_edit_inventory_dialog()

        self.show()

    def create_menu_bar(self):
        # --- MAIN MENUS --- #
        main_menu = self.menuBar()
        edit_menu = main_menu.addMenu("Edit")

        # --- EDIT SUB MENUS --- #
        user_action = QAction("Users...", self)
        search_types_action = QAction("Search Types...", self)

        user_action.triggered.connect(lambda: self.users_dialog.exec_())
        search_types_action.triggered.connect(lambda: self.search_type_dialog.exec_())

        edit_menu.addAction(user_action)
        edit_menu.addAction(search_types_action)
        edit_menu.addSeparator()

    def create_main_window_layouts(self):
        # --- MAIN LAYOUTS --- #
        main_layout = QVBoxLayout()
        search_layout = QVBoxLayout()
        table_layout = QHBoxLayout()

        main_layout.addLayout(search_layout)
        main_layout.addLayout(table_layout)

        # --- SUB LAYOUTS --- #
        self.search_bar_layout = QHBoxLayout()
        self.search_settings_layout = QHBoxLayout()
        self.table_results_layout = QHBoxLayout()
        self.table_button_layout = QVBoxLayout()

        search_layout.addLayout(self.search_bar_layout)
        search_layout.addLayout(self.search_settings_layout)

        table_layout.addLayout(self.table_results_layout)
        table_layout.addLayout(self.table_button_layout)

        self.table_button_layout.setAlignment(Qt.AlignTop)
        self.search_settings_layout.setAlignment(Qt.AlignRight)

        self.central_widget.setLayout(main_layout)

    def create_search_ui(self):
        # --- FUNCTIONS --- #
        def open_filter_window():
            self.filter_window.close()

            if self.search_type_combo.currentText() != "None":
                self.filter_window.show()
            else:
                QMessageBox.warning(self, "Filter Error", "You create a search type before using filters!",
                                    QMessageBox.Ok)

        self.search_bar = QLineEdit()
        search_btn = QPushButton("Search")
        search_filters_btn = QPushButton("Filters...")
        self.search_type_combo = QComboBox()
        self.username_combo = QComboBox()

        search_filters_btn.clicked.connect(open_filter_window)
        search_btn.clicked.connect(self.do_search)

        self.search_type_combo.setFixedWidth(155)
        self.search_type_combo.currentIndexChanged.connect(self.create_filter_window)

        self.username_combo.setMinimumWidth(155)

        self.search_bar_layout.addWidget(self.search_bar)
        self.search_bar_layout.addWidget(search_btn)
        self.search_bar_layout.addWidget(search_filters_btn)

        self.search_settings_layout.addWidget(QLabel("User: "))
        self.search_settings_layout.addWidget(self.username_combo)
        self.search_settings_layout.addWidget(QLabel("  Search Type: "))
        self.search_settings_layout.addWidget(self.search_type_combo)

    def create_table_ui(self):
        # --- FUNCTIONS --- #
        def check_out():
            if len(self.results_table.selectedItems()) != 0:
                sel_row_data = [self.results_table.selectedItems()[i:i + self.results_table.columnCount()] for i in
                                range(0, len(self.results_table.selectedItems()), self.results_table.columnCount())]
                sel_row_data = [[item.text() for item in sel_row_data[row]] for row in range(len(sel_row_data))]
                # This code block is used to parse out the info from the user's selection and separate it by row

                search_type_data = pandas.read_csv(f"data\\{self.search_type_combo.currentText()}.csv")

                for sel_row in sel_row_data:
                    for row in range(len(search_type_data)):
                        if [str(i) for i in search_type_data.loc[row]] == sel_row:
                            sel_row[-1] = self.username_combo.currentText()
                            search_type_data.loc[row] = sel_row
                            break

                search_type_data.to_csv(f"data\\{self.search_type_combo.currentText()}.csv", index=False)

                self.do_search()  # Does another search to refresh the table widget and show changes
            else:
                QMessageBox.warning(self, "Check Out Error!", "You must select an item to check out!", QMessageBox.Ok)

        def check_in():
            if len(self.results_table.selectedItems()) != 0:
                if len(self.results_table.selectedItems()) != 0:
                    sel_row_data = [self.results_table.selectedItems()[i:i + self.results_table.columnCount()] for i in
                                    range(0, len(self.results_table.selectedItems()), self.results_table.columnCount())]
                    sel_row_data = [[item.text() for item in sel_row_data[row]] for row in range(len(sel_row_data))]

                    search_type_data = pandas.read_csv(f"data\\{self.search_type_combo.currentText()}.csv")

                    for sel_row in sel_row_data:
                        for row in range(len(search_type_data)):
                            if [str(i) for i in search_type_data.loc[row]] == sel_row:
                                sel_row[-1] = "No"
                                search_type_data.loc[row] = sel_row
                                break

                    search_type_data.to_csv(f"data\\{self.search_type_combo.currentText()}.csv", index=False)

                    self.do_search()

            else:
                QMessageBox.warning(self, "Check In Error!", "You must select an item to check in!", QMessageBox.Ok)

        def add_inventory():
            self.create_edit_inventory_dialog()
            if self.search_type_combo.currentText() != "None":
                self.edit_inventory_dialog.setWindowTitle("Add to Inventory")
                self.edit_inventory_dialog.exec_()
            else:
                QMessageBox.warning(self, "Add Error", "You need to create a search type before adding to inventory!",
                                    QMessageBox.Ok)

        def edit_inventory():
            self.create_edit_inventory_dialog()
            if len(self.results_table.selectedItems()) == self.results_table.columnCount() \
                    and self.results_table.columnCount() != 0:

                self.edit_inventory_dialog.setWindowTitle("Edit Inventory Item")

                row_data = [item.text() for item in self.results_table.selectedItems()]

                edits = [self.inventory_parameter_layout.itemAt(i).widget()
                         for i in range(self.inventory_parameter_layout.count())
                         if isinstance(self.inventory_parameter_layout.itemAt(i).widget(), QLineEdit)]

                self.item_name_edit.setText(row_data[0])
                self.item_location_edit.setText(row_data[-2])

                row_data = row_data[1:-2]  # Removes the default parameters and only keeps the custom parameters

                for edit in range(len(edits)):
                    if str(row_data[edit]) != "nan":
                        edits[edit].setText(row_data[edit])

                self.edit_inventory_dialog.exec_()

            elif len(self.results_table.selectedItems()) == 0:
                QMessageBox.warning(self, "Edit Error", "You need to select an item to edit!", QMessageBox.Ok)
            else:
                QMessageBox.warning(self, "Edit Error", "You can only edit one item at a time!", QMessageBox.Ok)

        def remove_inventory():
            if len(self.results_table.selectedItems()) != 0:
                sel_row_data = [self.results_table.selectedItems()[i:i + self.results_table.columnCount()] for i in
                                range(0, len(self.results_table.selectedItems()), self.results_table.columnCount())]
                sel_row_data = [[item.text() for item in sel_row_data[row]] for row in range(len(sel_row_data))]

                index_list = []
                for model_index in self.results_table.selectionModel().selectedRows():
                    index = QPersistentModelIndex(model_index)
                    index_list.append(index)
                for index in index_list:
                    self.results_table.removeRow(index.row())

                search_type_data = pandas.read_csv(f"data\\{self.search_type_combo.currentText()}.csv")

                for sel_row in sel_row_data:
                    for row in range(len(search_type_data)):
                        if [str(item) for item in list(search_type_data.loc[row])] == sel_row:
                            search_type_data.drop(index=search_type_data.index[row], inplace=True)
                            search_type_data.reset_index(drop=True, inplace=True)
                            break

                search_type_data.to_csv(f"data\\{self.search_type_combo.currentText()}.csv", index=False)

            else:
                QMessageBox.warning(self, "Remove Inventory Error!", "You must select an item to remove!",
                                    QMessageBox.Ok)

        # --- UI --- #
        self.results_table = QTableWidget(0, 0)
        self.edit_table_button = QPushButton("Edit...")
        self.add_table_button = QPushButton("Add...")
        self.del_table_button = QPushButton("Remove")
        self.check_in_table_button = QPushButton("Check In")
        self.check_out_table_button = QPushButton("Check Out")

        self.add_table_button.clicked.connect(add_inventory)
        self.del_table_button.clicked.connect(remove_inventory)
        self.edit_table_button.clicked.connect(edit_inventory)
        self.check_in_table_button.clicked.connect(check_in)
        self.check_out_table_button.clicked.connect(check_out)

        self.results_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.results_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.table_results_layout.addWidget(self.results_table)

        self.table_button_layout.addWidget(self.edit_table_button)
        self.table_button_layout.addWidget(self.add_table_button)
        self.table_button_layout.addWidget(self.del_table_button)
        self.table_button_layout.addWidget(self.check_in_table_button)
        self.table_button_layout.addWidget(self.check_out_table_button)

    def create_users_dialog(self):
        # --- FUNCTIONS --- #
        def edit_user():
            self.user_edit.setText(self.users_list.selectedItems()[0].text())
            self.edit_user_dialog.setWindowTitle("Edit User")
            self.edit_user_dialog.exec_()

        def add_user():
            self.user_edit.clear()
            self.edit_user_dialog.setWindowTitle("Add User")
            self.edit_user_dialog.exec_()

        def del_user():
            num_users = len([self.users_list.item(item) for item in range(self.users_list.count())])

            if num_users > 1:
                users = [user.replace("\n", "") for user in open("config\\users.txt").readlines()]
                users.pop(self.users_list.row(self.users_list.selectedItems()[0]))

                open("config\\users.txt", "r+").truncate(0)
                open("config\\users.txt", "w").writelines([f"{user}\n" for user in users])

                self.users_list.takeItem(self.users_list.row(self.users_list.selectedItems()[0]))

                self.username_combo.clear()
                self.username_combo.addItems(users)

            else:
                QMessageBox.warning(self.users_dialog,
                                    "User Error", "You can't delete the last user!", QMessageBox.Ok)

        def close_function():
            self.users_dialog.close()
            self.create_users_dialog()

        def enable_function():
            edit_user_btn.setDisabled(False)
            del_user_btn.setDisabled(False)

            edit_user_btn.setDefault(True)

        def populate_users():
            if not os.path.isdir("config"):
                os.mkdir("config")

            if not os.path.isfile("config\\users.txt"):
                with open("config\\users.txt", "w") as users_file:
                    users_file.write("Default User\n")

            elif len(open("config\\users.txt", "r").readlines()) == 0:
                with open("config\\users.txt", "w") as users_file:
                    users_file.write("Default User\n")

            users = [user.replace("\n", "") for user in open("config\\users.txt", "r").readlines()]

            self.username_combo.clear()
            self.users_list.addItems(users)
            self.username_combo.addItems(users)

        # --- WINDOW --- #
        self.users_dialog = QDialog()
        self.users_dialog.setWindowTitle("Edit User")
        self.users_dialog.setFixedWidth(300)
        self.users_dialog.setFixedHeight(400)
        self.users_dialog.setWindowFlags(Qt.WindowTitleHint)

        # --- LAYOUTS --- #
        main_layout = QVBoxLayout()
        btn_layout = QHBoxLayout()

        # --- UI --- #
        self.users_list = QListWidget()
        edit_user_btn = QPushButton("Edit...")
        add_user_btn = QPushButton("Add...")
        del_user_btn = QPushButton("Remove")
        close_btn = QPushButton("Close")

        add_user_btn.clicked.connect(add_user)
        edit_user_btn.clicked.connect(edit_user)
        del_user_btn.clicked.connect(del_user)
        close_btn.clicked.connect(close_function)

        self.users_list.itemSelectionChanged.connect(enable_function)

        edit_user_btn.setDisabled(True)
        del_user_btn.setDisabled(True)

        close_btn.setDefault(True)

        btn_layout.addWidget(edit_user_btn)
        btn_layout.addWidget(add_user_btn)
        btn_layout.addWidget(del_user_btn)
        btn_layout.addWidget(close_btn)

        main_layout.addWidget(self.users_list)
        main_layout.addLayout(btn_layout)

        self.users_dialog.setLayout(main_layout)

        populate_users()

    def create_edit_user_dialog(self):
        # --- FUNCTIONS --- #
        def confirm_func():
            if self.edit_user_dialog.windowTitle() == "Add User":
                if self.user_edit.text() != "":
                    with open("config\\users.txt", "a+") as file:
                        file.write(f"{self.user_edit.text()}\n")

                    self.users_list.addItem(self.user_edit.text())
                    self.username_combo.addItem(self.user_edit.text())

                    self.edit_user_dialog.close()

                else:
                    QMessageBox.warning(self.edit_user_dialog,
                                        "User Error", "User field cannot be blank!", QMessageBox.Ok)

            elif self.edit_user_dialog.windowTitle() == "Edit User":
                if self.user_edit.text() != "":
                    users = [user.replace("\n", "") for user in open("config\\users.txt").readlines()]
                    users[self.users_list.row(self.users_list.selectedItems()[0])] = self.user_edit.text()

                    open("config\\users.txt", "r+").truncate(0)
                    open("config\\users.txt", "w").writelines([f"{user}\n" for user in users])

                    self.users_list.clear()
                    self.username_combo.clear()

                    self.users_list.addItems(users)
                    self.username_combo.addItems(users)

                    self.edit_user_dialog.close()
                else:
                    QMessageBox.warning(self.edit_user_dialog,
                                        "User Error", "User field cannot be blank!", QMessageBox.Ok)

            self.users_list.setCurrentRow([self.users_list.item(item).text() for item in
                                                 range(self.users_list.count())]
                                                .index(self.user_edit.text()))

        # --- WINDOW --- #
        self.edit_user_dialog = QDialog()
        self.edit_user_dialog.setFixedWidth(250)
        self.edit_user_dialog.setFixedHeight(100)
        self.edit_user_dialog.setWindowFlags(Qt.WindowTitleHint)

        # --- LAYOUTS --- #
        main_layout = QVBoxLayout()
        btn_layout = QHBoxLayout()

        # --- UI --- #
        self.user_edit = QLineEdit()
        btn_confirm = QPushButton("Confirm")
        btn_cancel = QPushButton("Cancel")

        btn_confirm.clicked.connect(confirm_func)
        btn_cancel.clicked.connect(lambda: self.edit_user_dialog.close())

        self.user_edit.setPlaceholderText("User")

        btn_layout.addWidget(btn_confirm)
        btn_layout.addWidget(btn_cancel)

        main_layout.addWidget(self.user_edit)
        main_layout.addLayout(btn_layout)

        self.edit_user_dialog.setLayout(main_layout)

    def create_search_type_dialog(self):
        # --- FUNCTIONS --- #
        def edit_search_type():
            self.create_edit_search_type_dialog()

            sel_search_type = self.search_type_list.selectedItems()[0].text()
            self.prev_search_type_name = sel_search_type  # Used so that the program can find the file to edit later

            parameters = open(f"data\\{sel_search_type}.csv", "r") \
                             .readlines()[0].split(",")[1:-2]

            self.search_type_name_edit.setText(sel_search_type)

            self.parameter_list.addItems(parameters)

            self.edit_search_type_dialog.setWindowTitle("Edit Search Type")

            self.edit_search_type_dialog.move(int(self.search_type_dialog.pos().x() + 50),
                                              int(self.search_type_dialog.pos().y()))

            self.edit_search_type_dialog.exec_()

        def add_search_type():
            self.create_edit_search_type_dialog()

            self.edit_search_type_dialog.setWindowTitle("Add Search Type")

            self.edit_search_type_dialog.move(int(self.search_type_dialog.pos().x() + 50),
                                              int(self.search_type_dialog.pos().y()))

            self.edit_search_type_dialog.exec_()

        def del_search_type():
            delete = QMessageBox.Yes
            sel_search_type = self.search_type_list.selectedItems()[0].text()

            if len(open(f"data\\{sel_search_type}.csv", "r").readlines()) > 1:
                delete = QMessageBox.question(self.search_type_dialog, "Remove search type?",
                                              "Search type contains data! Are you sure you wish to remove?",
                                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if delete == QMessageBox.Yes:
                os.remove(f"data\\{sel_search_type}.csv")

                self.search_type_list.takeItem(self.search_type_list.row(self.search_type_list.selectedItems()[0]))

                self.search_type_combo.clear()
                search_types = [search_type.replace(".csv", "") for search_type in os.listdir("data")
                                if ".csv" in search_type]
                if len(search_types) != 0:
                    self.search_type_combo.addItems(search_types)
                else:
                    self.search_type_combo.addItem("None")

                if len(self.search_type_list.selectedItems()) == 0:
                    edit_search_type_btn.setDisabled(True)
                    del_search_type_btn.setDisabled(True)

                    close_btn.setDefault(True)

                self.results_table.clear()
                self.results_table.setRowCount(0)
                self.results_table.setColumnCount(0)

        def enable_function():
            edit_search_type_btn.setDisabled(False)
            del_search_type_btn.setDisabled(False)

            edit_search_type_btn.setDefault(True)

        def close_function():
            self.search_type_dialog.close()
            self.create_search_type_dialog()

        def populate_search_types():
            if not os.path.isdir("data"):
                os.mkdir("data")

            search_types = [search_type.replace(".csv", "") for search_type in os.listdir("data")
                            if ".csv" in search_type]
            self.search_type_combo.clear()
            if len(search_types) != 0:
                self.search_type_list.addItems(search_types)
                self.search_type_combo.addItems(search_types)
            else:
                self.search_type_combo.addItem("None")

        # --- WINDOW --- #
        self.search_type_dialog = QDialog()
        self.search_type_dialog.setFixedWidth(300)
        self.search_type_dialog.setFixedHeight(400)
        self.search_type_dialog.setWindowTitle("Search Types")
        self.search_type_dialog.setWindowFlags(Qt.WindowTitleHint)

        # --- LAYOUTS --- #
        main_layout = QVBoxLayout()
        list_layout = QVBoxLayout()
        btn_layout = QHBoxLayout()

        # --- UI --- #
        self.search_type_list = QListWidget()
        edit_search_type_btn = QPushButton("Edit...")
        add_search_type_btn = QPushButton("Add...")
        del_search_type_btn = QPushButton("Remove")
        close_btn = QPushButton("Close")

        add_search_type_btn.clicked.connect(add_search_type)
        edit_search_type_btn.clicked.connect(edit_search_type)
        del_search_type_btn.clicked.connect(del_search_type)

        self.search_type_list.itemSelectionChanged.connect(enable_function)

        close_btn.clicked.connect(close_function)

        edit_search_type_btn.setDisabled(True)
        del_search_type_btn.setDisabled(True)

        close_btn.setDefault(True)

        list_layout.addWidget(self.search_type_list)
        btn_layout.addWidget(edit_search_type_btn)
        btn_layout.addWidget(add_search_type_btn)
        btn_layout.addWidget(del_search_type_btn)
        btn_layout.addWidget(close_btn)

        main_layout.addLayout(list_layout)
        main_layout.addLayout(btn_layout)

        self.search_type_dialog.setLayout(main_layout)

        populate_search_types()

    def create_edit_search_type_dialog(self):
        # --- FUNCTIONS --- #
        def up_parameter():
            currentRow = self.parameter_list.currentRow()
            currentItem = self.parameter_list.takeItem(currentRow)

            self.parameter_list.insertItem(currentRow - 1, currentItem)
            self.parameter_list.setCurrentRow(currentRow - 1)

        def down_parameter():
            currentRow = self.parameter_list.currentRow()
            currentItem = self.parameter_list.takeItem(currentRow)

            self.parameter_list.insertItem(currentRow + 1, currentItem)
            self.parameter_list.setCurrentRow(currentRow + 1)

        def confirm_function():
            if self.edit_search_type_dialog.windowTitle() == "Add Search Type":
                if self.search_type_name_edit.text() != "":
                    if f"{self.search_type_name_edit.text()}.csv" not in [file for file in os.listdir("data")]:
                        parameters = [self.parameter_list.item(item).text() for item in
                                      range(self.parameter_list.count())]

                        pandas.DataFrame(columns=(["Name"] + parameters + ["Location", "Checked Out"])) \
                            .to_csv(f"data\\{self.search_type_name_edit.text()}.csv", index=False)

                        search_types = [search_type.replace(".csv", "") for search_type in os.listdir("data")
                                        if ".csv" in search_type]

                        self.search_type_list.clear()
                        self.search_type_combo.clear()

                        self.search_type_list.addItems(search_types)
                        self.search_type_combo.addItems(search_types)

                        self.edit_search_type_dialog.close()

                    else:
                        QMessageBox.warning(self.edit_search_type_dialog, "Search Type Add Error",
                                            "Search type already exists!", QMessageBox.Ok)
                else:
                    QMessageBox.warning(self.edit_search_type_dialog, "Search Type Add Error",
                                        "Search type name field cannot be blank!", QMessageBox.Ok)

            elif self.edit_search_type_dialog.windowTitle() == "Edit Search Type":
                if self.search_type_name_edit.text() != "":
                    prev_search_type_data = pandas.read_csv(f"data\\{self.prev_search_type_name}.csv")
                    parameters = [self.parameter_list.item(item).text() for item in
                                  range(self.parameter_list.count())]

                    new_search_type_parameters = ["Name"] + parameters + ["Location", "Checked Out"]
                    new_search_type_data = pandas.DataFrame(columns=new_search_type_parameters)

                    for column in new_search_type_data:
                        if column in [column for column in prev_search_type_data]:
                            new_search_type_data[column] = prev_search_type_data[column]

                    os.remove(f"data\\{self.prev_search_type_name}.csv")

                    new_search_type_data.to_csv(f"data\\{self.search_type_name_edit.text()}.csv", index=False)

                    search_types = [search_type.replace(".csv", "") for search_type in os.listdir("data")
                                    if ".csv" in search_type]

                    self.search_type_list.clear()
                    self.search_type_combo.clear()

                    self.search_type_list.addItems(search_types)
                    self.search_type_combo.addItems(search_types)

                    self.edit_search_type_dialog.close()

                else:
                    QMessageBox.warning(self.edit_search_type_dialog, "Search Type Add Error",
                                        "Search type name field cannot be blank!", QMessageBox.Ok)

            self.search_type_list.setCurrentRow([self.search_type_list.item(item).text() for item in
                                                 range(self.search_type_list.count())]
                                                .index(self.search_type_name_edit.text()))

        def add_parameter():
            if self.parameter_edit.text() != "":
                parameters = [self.parameter_list.item(item).text() for item in range(self.parameter_list.count())]

                if self.parameter_edit.text() not in parameters:
                    self.parameter_list.addItem(self.parameter_edit.text())
                    self.parameter_edit.clear()

                else:
                    QMessageBox.warning(self.edit_search_type_dialog, "Parameter Error",
                                        "Parameter already exists!", QMessageBox.Ok)

            else:
                QMessageBox.warning(self.edit_search_type_dialog, "Parameter Error",
                                    "Parameter field cannot be blank!", QMessageBox.Ok)

        def del_parameter():
            delete = QMessageBox.Yes

            if len(self.parameter_list.selectedItems()) != 0:
                if self.edit_search_type_dialog.windowTitle() == "Edit Search Type":

                    prev_search_type_data = pandas.read_csv(f"data\\{self.prev_search_type_name}.csv")

                    for item in prev_search_type_data[self.parameter_list.selectedItems()[0].text()]:
                        if str(item) != "nan":
                            delete = QMessageBox.question(
                                self.edit_search_type_dialog, "Remove parameter?",
                                "Parameter contains data! Are you sure you wish to remove?",
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                            break

                    if delete == QMessageBox.Yes:
                        self.parameter_list.takeItem(self.parameter_list.row(self.parameter_list.selectedItems()[0]))

                else:
                    self.parameter_list.takeItem(self.parameter_list.row(self.parameter_list.selectedItems()[0]))

            else:
                QMessageBox.warning(self.edit_search_type_dialog, "Parameter Error",
                                    "You must select a parameter to remove!", QMessageBox.Ok)

        def close_function():
            self.edit_search_type_dialog.close()
            self.create_edit_search_type_dialog()

        # --- WINDOW --- #
        self.edit_search_type_dialog = QDialog()
        self.edit_search_type_dialog.setFixedWidth(300)
        self.edit_search_type_dialog.setFixedHeight(400)
        self.edit_search_type_dialog.setWindowFlags(Qt.WindowTitleHint)

        # --- LAYOUTS --- #
        main_layout = QVBoxLayout()
        move_btn_layout = QVBoxLayout()
        btn_layout = QHBoxLayout()
        list_layout = QHBoxLayout()
        parameter_layout = QHBoxLayout()

        # --- UI --- #
        self.search_type_name_edit = QLineEdit("")
        self.parameter_list = QListWidget()
        self.parameter_edit = QLineEdit("")
        add_parameter_btn = QPushButton("Add")
        del_parameter_btn = QPushButton("Delete")
        confirm_btn = QPushButton("Confirm")
        cancel_btn = QPushButton("Cancel")
        up_btn = QPushButton("↑")
        down_btn = QPushButton("↓")

        up_btn.setFixedWidth(20)
        down_btn.setFixedWidth(20)

        up_btn.setFixedHeight(30)
        down_btn.setFixedHeight(30)

        add_parameter_btn.clicked.connect(add_parameter)
        del_parameter_btn.clicked.connect(del_parameter)
        confirm_btn.clicked.connect(confirm_function)
        cancel_btn.clicked.connect(close_function)
        up_btn.clicked.connect(up_parameter)
        down_btn.clicked.connect(down_parameter)

        add_parameter_btn.setDefault(True)

        self.search_type_name_edit.setPlaceholderText("Search Type Name")
        self.search_type_name_edit.setValidator(QRegExpValidator(QRegExp("^[\w\-. ]+$")))

        self.parameter_edit.setValidator(QRegExpValidator("^[^,]+$"))

        self.parameter_edit.setPlaceholderText("Parameter Name")

        parameter_layout.addWidget(self.parameter_edit)
        parameter_layout.addWidget(add_parameter_btn)
        parameter_layout.addWidget(del_parameter_btn)

        move_btn_layout.addWidget(up_btn)
        move_btn_layout.addWidget(down_btn)
        move_btn_layout.setAlignment(Qt.AlignTop)

        list_layout.addWidget(self.parameter_list)
        list_layout.addLayout(move_btn_layout)

        btn_layout.addWidget(confirm_btn)
        btn_layout.addWidget(cancel_btn)

        main_layout.addWidget(self.search_type_name_edit)
        main_layout.addLayout(parameter_layout)
        main_layout.addLayout(list_layout)
        main_layout.addLayout(btn_layout)

        self.edit_search_type_dialog.setLayout(main_layout)

    def create_filter_window(self):
        # --- FUNCTIONS --- #
        def populate_filters():
            sel_search_type = self.search_type_combo.currentText()

            if self.search_type_combo.currentText() != "None" and self.search_type_combo.currentText() != "":
                parameters = open(f"data\\{sel_search_type}.csv").readlines()[0].split(",")[1:]
                parameters[-1] = parameters[-1].replace("\n", "")  # Remove the \n so it doesnt show up in menus

                for parameter in parameters:
                    self.filter_list.addRow(QLabel(parameter), QLineEdit())

        # --- WINDOW --- #
        self.filter_window = QWidget()
        self.filter_window.setWindowTitle("Filters")
        self.filter_window.setFixedWidth(400)
        self.filter_window.setFixedHeight(550)
        self.filter_window.setWindowFlags(Qt.WindowTitleHint)

        # --- LAYOUTS --- #
        main_layout = QVBoxLayout()
        self.filter_list = QFormLayout()

        # --- UI --- #
        scroll_box = QWidget(self.filter_window)
        scroll_box.setLayout(self.filter_list)
        close_btn = QPushButton("Close")

        close_btn.clicked.connect(lambda: self.filter_window.close())

        scroll = QScrollArea()
        scroll.setWidget(scroll_box)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(500)
        scroll.setMinimumWidth(300)

        main_layout.addWidget(scroll)
        main_layout.addWidget(close_btn)

        self.filter_window.setLayout(main_layout)
        populate_filters()

    def create_edit_inventory_dialog(self):
        # --- FUNCTIONS --- #
        def confirm_function():
            if self.edit_inventory_dialog.windowTitle() == "Add to Inventory":
                if self.item_name_edit.text() != "" and self.item_location_edit.text() != "":
                    parameter_edits = [self.inventory_parameter_layout.itemAt(i).widget()
                                       for i in range(self.inventory_parameter_layout.count())
                                       if isinstance(self.inventory_parameter_layout.itemAt(i).widget(), QLineEdit)]

                    data = [self.item_name_edit.text()] + [edit.text() for edit in parameter_edits] + \
                           [self.item_location_edit.text(), "No"]

                    data_file = pandas.read_csv(f"data\\{self.search_type_combo.currentText()}.csv")

                    data_file.loc[len(data_file)] = data

                    data_file.to_csv(f"data\\{self.search_type_combo.currentText()}.csv", index=False)

                    self.edit_inventory_dialog.close()

                    self.do_search()

                else:
                    QMessageBox.warning(self.edit_inventory_dialog, "Add Item Error",
                                        "Name and/or location field cannot be empty!", QMessageBox.Ok)

            elif self.edit_inventory_dialog.windowTitle() == "Edit Inventory Item":
                parameter_edits = [self.inventory_parameter_layout.itemAt(i).widget()
                                   for i in range(self.inventory_parameter_layout.count())
                                   if isinstance(self.inventory_parameter_layout.itemAt(i).widget(), QLineEdit)]

                prev_row_data = [item.text() for item in self.results_table.selectedItems()]

                self.results_table.selectedItems()[0].setText(self.item_name_edit.text())
                self.results_table.selectedItems()[-2].setText(self.item_location_edit.text())

                for index, edit in enumerate(parameter_edits):
                    [item for item in self.results_table.selectedItems()[1:-2]][index].setText(edit.text())

                new_row_data = [self.item_name_edit.text()] + \
                               [edit.text() for edit in parameter_edits] + \
                               [item.text() for item in self.results_table.selectedItems()[-2:]]

                search_type_data = pandas.read_csv(f"data\\{self.search_type_combo.currentText()}.csv")

                for row in range(len(search_type_data)):
                    if list([str(item) for item in search_type_data.loc[row]]) == prev_row_data:
                        search_type_data.loc[row] = new_row_data
                        break

                search_type_data.to_csv(f"data\\{self.search_type_combo.currentText()}.csv", index=False)

                self.do_search()

                self.edit_inventory_dialog.close()

        def populate_parameters():
            if self.search_type_combo.currentText() != "None" and self.search_type_combo.currentText() != "":
                parameters = open(f"data\\{self.search_type_combo.currentText()}.csv").readlines()[0].split(",")
                parameters[-1] = parameters[-1].replace("\n", "")

                for parameter in parameters[1:-2]:
                    self.inventory_parameter_layout.addRow(QLabel(parameter), QLineEdit())

        # --- WINDOW --- #
        self.edit_inventory_dialog = QDialog()
        self.edit_inventory_dialog.setFixedWidth(425)
        self.edit_inventory_dialog.setFixedHeight(500)
        self.edit_inventory_dialog.setWindowFlags(Qt.WindowTitleHint)

        # --- LAYOUTS --- #
        main_layout = QVBoxLayout()
        btn_layout = QHBoxLayout()
        self.inventory_parameter_layout = QFormLayout()

        # --- UI --- #
        scroll_box = QWidget(self.edit_inventory_dialog)
        scroll_box.setLayout(self.inventory_parameter_layout)
        self.item_name_edit = QLineEdit()
        self.item_location_edit = QLineEdit()
        confirm_btn = QPushButton("Confirm")
        cancel_btn = QPushButton("Cancel")

        confirm_btn.setAutoDefault(False)
        cancel_btn.setAutoDefault(False)

        self.item_name_edit.setPlaceholderText("Item Name")
        self.item_location_edit.setPlaceholderText("Location")

        confirm_btn.clicked.connect(confirm_function)
        cancel_btn.clicked.connect(lambda: self.edit_inventory_dialog.close())

        scroll = QScrollArea()
        scroll.setWidget(scroll_box)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(400)
        scroll.setMinimumWidth(325)

        btn_layout.addWidget(confirm_btn)
        btn_layout.addWidget(cancel_btn)

        main_layout.addWidget(self.item_name_edit)
        main_layout.addWidget(self.item_location_edit)
        main_layout.addWidget(scroll)
        main_layout.addLayout(btn_layout)

        self.edit_inventory_dialog.setLayout(main_layout)

        populate_parameters()

    def do_search(self):
        self.results_table.setColumnCount(0)
        self.results_table.setRowCount(0)
        self.results_table.clear()

        if self.search_type_combo.currentText() != "None":
            filter_widgets = [self.filter_list.itemAt(i).widget()
                             for i in range(self.filter_list.count())]

            filters = {"Name": self.search_bar.text().lower()}

            for widget in range(0, len(filter_widgets), 2):
                filters[filter_widgets[widget].text()] = filter_widgets[widget + 1].text().lower()

            search_results = pandas.read_csv(f"data\\{self.search_type_combo.currentText()}.csv")
            search_results_lower = search_results.apply(lambda x: x.astype(str).str.lower())

            for parameter, _filter in filters.items():
                search_results_lower = search_results_lower[search_results_lower[parameter].str.contains(_filter)]

            for index, row in search_results.iterrows():
                if index not in [i[0] for i in search_results_lower.iterrows()]:
                    search_results.drop(index=index, inplace=True)

            results_header = QHeaderView(Qt.Horizontal, self.results_table)
            results_header.setDefaultAlignment(Qt.AlignTop)
            results_header.show()

            self.results_table.setRowCount(len(search_results))
            self.results_table.setColumnCount(len(search_results.columns))
            self.results_table.setHorizontalHeader(results_header)
            self.results_table.setHorizontalHeaderLabels([column for column in search_results.columns])

            search_results.reset_index(drop=True, inplace=True)

            for row in range(self.results_table.rowCount()):
                for column in range(self.results_table.columnCount()):
                    self.results_table.setItem(row, column, QTableWidgetItem(str(search_results.loc[row][column])))

        else:
            QMessageBox.warning(self, "Search Error!", "You must create a search type before you can search!",
                                QMessageBox.Ok)


def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()
