from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout

# This class takes in a s_text_area widget as input 
# and provides the ability to search for a text string within its contents.

# search_text method performs the actual search 
# and updates the match count and highlights the matching text.

# It uses a highlight function to indicate the location of the search results 
# and allows to navigate through the results by finding the next match.
class s_find_dialog(QDialog):

    def __init__(
            self, 
            text_area,
            parent=None
            ):
        super(s_find_dialog, self).__init__(parent)

        self.text_area = text_area

        self.match_count = 0
        self.init_pos = 0

        self._init_ui()


    def search_text(self):
        cursor = self.text_area.textCursor()

        if cursor.hasSelection():
            cursor.clearSelection()


        search_text = self.search_field.text()

        self.match_counts_label.setText(
            f"Match count: {self.text_area.get_match_count(search_text)}"
            )
        match = self.text_area.find_next_match(self.init_pos, search_text)

        if match != None:
            start_pos = match.position() - len(search_text)
            end_pos = match.position()

            self.text_area.highlight_selection(cursor, start_pos, end_pos)

            self.init_pos = end_pos

        else:
            self.init_pos = 0
            match = self.text_area.find_next_match(self.init_pos, search_text)
 
            if match != None:
                start_pos = match.position() - len(search_text)
                end_pos = match.position()

                self.text_area.highlight_selection(cursor, start_pos, end_pos)

                self.init_pos = end_pos


    def _init_ui(self):
        self.setWindowTitle("Find")
        
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Search for:"))

        self.search_field = QLineEdit()

        layout.addWidget(self.search_field)
        
        find_button = QPushButton("Find Next")

        find_button.clicked.connect(self.search_text)
        layout.addWidget(find_button)
        
        cancel_button = QPushButton("Cancel")

        cancel_button.clicked.connect(self.reject)
        layout.addWidget(cancel_button)
    
        self.match_counts_label = QLabel("Match count:")
        layout.addWidget(self.match_counts_label)        

    