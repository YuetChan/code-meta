from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QDialogButtonBox, QVBoxLayout, QFileDialog, QPushButton, QWidget

class s_single_input_dialog(QDialog):

    def __init__(
            self, 
            input_map,
            parent=None
            ):
        super().__init__(parent)
        
        self.setFixedWidth(240)
        self.input_map = input_map

        self._init_ui()
        

    def get_config(self): 
        return {
            self.input_map['dialog_var_1']: self.line_edit_1.text(),
            self.input_map['dialog_var_2']: self.line_edit_2.text(),
            self.input_map['dialog_var_3']: self.dirpath
        }


    def _init_ui(self):
        self.setWindowTitle(self.input_map['dialog_title'])
        
        self.choose_file = QPushButton('Choose')

        self.choose_file.setGeometry(50, 50, 200, 30)
        self.choose_file.clicked.connect(self.show_dir_dialog)

        self.label_1 = QLabel(self.input_map['dialog_msg_1'])
        self.label_2 = QLabel(self.input_map['dialog_msg_2'])
        self.label_3 = QLabel(self.input_map['dialog_msg_3'])
        self.label_4 = QLabel('Directory:  ')

        self.label_4.setWordWrap(True)
        self.label_4.adjustSize()

        self.line_edit_1 = QLineEdit()
        self.line_edit_2 = QLineEdit()

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        
        layout = QVBoxLayout()

        layout.addWidget(self.label_1)
        layout.addWidget(self.line_edit_1)

        layout.addWidget(self.label_2)
        layout.addWidget(self.line_edit_2)

        layout.addWidget(self.label_3)
        layout.addWidget(self.choose_file)

        file_choose_layout = QVBoxLayout()

        file_choose_layout.addWidget(self.label_4)
        file_choose_layout.addStretch(1)
        file_choose_layout.addWidget(self.button_box)

        file_choose_widget = QWidget()

        file_choose_widget.setFixedHeight(100)
        file_choose_widget.setLayout(file_choose_layout)

        layout.addWidget(file_choose_widget)

        self.setLayout(layout)


    def show_dir_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        self.dirpath = QFileDialog.getExistingDirectory(self, 'Choose a directory', '', options=options)

        self.label_4.setText(f"Directory:  {self.dirpath}")

