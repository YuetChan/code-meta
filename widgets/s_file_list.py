from PyQt5.QtCore import pyqtSignal, QModelIndex
from PyQt5.QtWidgets import QListView

# This is a custom list view widget for displaying files. 

# It emits a custom signal when a file is clicked.
class s_file_list(QListView):

    file_clicked = pyqtSignal(dict)

    def __init__(
            self, 
            model,
            parent=None
            ):
        super(s_file_list, self).__init__(parent)

        self.src_model = model
        self.setModel(model)

        self.selected_fpath = None

        self.clicked.connect(self._on_file_clicked)


    def update_model(
            self, 
            model
            ):
        self.src_model = model
        self.setModel(model)


    def click_first_file(self):
        root_idx = self.model().index(0, 0, QModelIndex())
        self.click_file_by_index(root_idx)


    def click_file_by_index(
            self, 
            idx
            ):
        self.clicked.emit(idx)
        self.setCurrentIndex(idx)


    def _on_file_clicked(
            self, 
            idx
            ):
        print(self.model().data(idx))
        self.selected_fpath = self.model().data(idx)

        self.file_clicked.emit({
            'file_path': self.selected_fpath,
            })

