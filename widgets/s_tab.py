from PyQt5.QtWidgets import QTabWidget

class s_tab(QTabWidget):

    def __init__(
            self, 
            parent=None
            ):
        super(s_tab, self).__init__(parent)


    def connect_tab_changed(
            self, 
            l_func
            ):
        self.currentChanged.connect(
            lambda idx: l_func(idx)
            )   


    def connect_tab_closed(
            self, 
            l_func
            ):
         self.tabCloseRequested.connect(
             lambda idx : l_func(idx)
             )


    # Each insert/remove will refresh the components on main window.
    # The upsert imple should be optimized in the future ...
    def upsert_widget_by_label(
            self, 
            widget, 
            label
            ):
        tab_idx = self._get_tab_index_by_label(label)

        if tab_idx >= 0:
            self.removeTab(tab_idx)
            self.insertTab(tab_idx, widget, label)
            tab_idx = self._get_tab_index_by_label(label)

        else:
            self.addTab(widget, label)
            tab_idx = self._get_tab_index_by_label(label)


        self.setCurrentIndex(tab_idx)
  

    def _get_tab_index_by_label(
            self, 
            label
            ):
        idx = -1

        for i in range(self.count()):
            if self.tabBar().tabText(i) == label:
                idx = i

                break

    
        return idx
    
