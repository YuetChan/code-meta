import Levenshtein

from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtWidgets import QWidget, QVBoxLayout

class levenshtein_sort_proxy_model(QSortFilterProxyModel):
    
    def lessThan(
            self, 
            left_idx, 
            right_idx
            ):
        return Levenshtein.ratio(
            self.sourceModel().data(left_idx), 
            self.filterRegExp().pattern()) < Levenshtein.ratio(
            self.sourceModel().data(right_idx), 
            self.filterRegExp().pattern())


class s_file_searcher(QWidget):

    def __init__(
            self,
            search_title,
            search_bar,
            file_list,
            parent=None
            ):
        super(s_file_searcher, self).__init__(parent)

        self.search_title = search_title
        
        self.search_bar = search_bar
        self.file_list = file_list

        self.selected_fpath = self.file_list.selected_fpath

        self._init_file_list_sort_model()

        self.search_bar.connect_text_changed(
            lambda text: self.file_list.model().setFilterRegExp(text)
            )

        self._init_ui()


    def update_file_list(
            self, 
            file_list
            ):
        self.file_list = file_list

        self.selected_fpath = self.file_list.selected_fpath

        self._init_file_list_sort_model()
        # more?


    def get_file_count(self):
        return self.file_list.model().rowCount()


    def click_first_file(self):
        self.file_list.click_first_file()


    def has_selection(self):
        return self.file_list.selectionModel().hasSelection()


    def remove_selected_file(self):
        idx = self.file_list.currentIndex()
        self.file_list.model().removeRow(idx.row())


    def clear_selection(self):
        self.file_list.clearSelection()


    def connect_file_clicked(
            self, 
            l_func
            ):
        self.file_list.file_clicked.connect(
            lambda data: self._on_file_clicked(l_func, data)
        )


    def _on_file_clicked(
            self, 
            l_func,
            data
            ):
        self.selected_fpath = data['file_path']
        l_func(data)


    def _init_ui(self):
        v_box = QVBoxLayout()

        v_box.addWidget(self.search_title)
        v_box.addWidget(self.search_bar)

        v_box.addWidget(self.file_list)

        self.setLayout(v_box)


    def _init_file_list_sort_model(self):
        model = levenshtein_sort_proxy_model()

        model.setSourceModel(self.file_list.src_model)
        model.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self.file_list.setModel(model)
    
