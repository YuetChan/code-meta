from PyQt5.QtCore import Qt, pyqtSignal, QModelIndex
from PyQt5.QtWidgets import QTreeView
from PyQt5.QtGui import QBrush, QColor

# This is a custom tree view widget for files and directories.

# It emits a custom signal when a file or directory is clicked.

# It also has methods for highlighting a model of items, 
# based on a list of file paths to highlight and a decorator function.
class s_file_tree(QTreeView):

    file_clicked = pyqtSignal(dict)

    def __init__(
            self, 
            hl_fpaths,
            hl_decorator,
            parent=None
            ):
        super(s_file_tree, self).__init__(parent)

        self.selected_fpath = None
        self.is_dir_selected = None

        self.selected_item = None

        self.hl_fpaths = hl_fpaths
        self.hl_decorator = hl_decorator

        self.default_decorator = lambda item: item.setForeground(QBrush(QColor('black')))
        
        self.clicked.connect(self._on_file_clicked)


    def setModel(
            self, 
            model
            ):
        super().setModel(model)
        
        self.selected_item = self.model().invisibleRootItem().child(0, 0)

        self._unhighlight_model(self.model().invisibleRootItem().child(0, 0))
        self._highlight_model(self.model().invisibleRootItem().child(0, 0))


    def click_root_file(self):
        root_idx = self.model().index(0, 0, QModelIndex())

        self.clicked.emit(root_idx)
        self.setCurrentIndex(root_idx)


    def highlight_selected_file(self):
        self._highlight_item(self.selected_item)


    def unhighlight_selected_file(self):
        self._unhighlight_item(self.selected_item)


    def _highlight_item(
            self, 
            item
            ):
        self.hl_decorator(item)


    def _unhighlight_item(
            self,
            item
            ):
        self.default_decorator(item)
        

    def _highlight_model(
            self, 
            item
            ):
        fpath = item.data(Qt.UserRole)[0]

        if fpath in self.hl_fpaths:
            self._highlight_item(item)
        
        
        if item.hasChildren():
            for row in range(item.rowCount()):
                child = item.child(row)
                self._highlight_model(child)

    
    def _unhighlight_model(
            self, 
            item
            ):
        fpath = item.data(Qt.UserRole)[0]

        self._unhighlight_item(item)
            
        if item.hasChildren():
            for row in range(item.rowCount()):
                child = item.child(row)
                self._unhighlight_model(child)


    def set_highlight_file_paths(self, hl_fpaths):
        self.hl_fpaths = hl_fpaths

        self.setModel(self.model())


    def _on_file_clicked(
            self, 
            index
            ):
        self.selected_item = self.model().itemFromIndex(index)
        
        labels = self.selected_item.data(Qt.UserRole)

        self.selected_fpath = labels[0]
        self.is_dir_selected = labels[1]

        self.file_clicked.emit({
            'file_path': self.selected_fpath,
            'is_dir': self.is_dir_selected
        })

