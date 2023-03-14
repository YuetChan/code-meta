from bs4 import BeautifulSoup
import hashlib

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent, QTextListFormat, QTextCursor, QKeySequence
from PyQt5.QtWidgets import QTextEdit, QApplication

from widgets.s_find_dialog import s_find_dialog

class s_text_edit_area(QTextEdit):

    def __init__(
            self, 
            parent=None
            ):
        super(s_text_edit_area, self).__init__(parent)

        self.qt_clipbrd_cache = { }

        self.cursorPositionChanged.connect(self.on_cursor_position_changed)


    def set_tool_bar(
            self, 
            tool_bar
            ):
        self.tool_bar = tool_bar


    def keyPressEvent(
            self, 
            event: QKeyEvent
            ):
        clipbrd = QApplication.clipboard()

        cursor = self.textCursor()

        tool_bar = self.tool_bar

        if self.is_delete_key(event):
            if self.is_delete_on_empty_line(cursor) and self.is_list_above(cursor):
                super().keyPressEvent(event)

                self.create_empty_list(cursor)
                tool_bar.toggle_bullet_pt(True) 

            elif self.is_delete_on_empty_list(cursor):
                super().keyPressEvent(event)

                was_in_bullet_pt = not self.is_list(cursor) and tool_bar.is_bullet_pt_checked()

                if was_in_bullet_pt:
                    self.reset_indent(cursor)
                    tool_bar.toggle_bullet_pt(False) 


            else:
                super().keyPressEvent(event)


        elif self.is_copy_key(event) or self.is_cut_key(event):
            # copy / cut the htnl to clipbrd first
            # by default, qt makes small adjustment to clipbrd html 
            super().keyPressEvent(event)

            cursor = self.textCursor()
            
            clipbrd_html = clipbrd.mimeData().html()
            stripped_html = clipbrd_html

            if self.is_list(cursor) and self.is_start_of_line(cursor) and not self.is_on_first_line(cursor):
                stripped_html = self.strip_first_p_tag(stripped_html)

            
            stripped_html = self.strip_qt_start_and_end_segments_tags(stripped_html)

            new_cache = { }
            new_cache[self.get_hash_of_str(clipbrd_html)] = stripped_html 

            self.set_qt_clipboard_cache(new_cache)

        elif self.is_paste_key(event):
            clipbrd_html = clipbrd.mimeData().html()
            hashed_html = self.get_hash_of_str(clipbrd_html)

            html = ''

            if self.is_the_same_qt_clipboard_cache(hashed_html):
                cursor = self.textCursor()
                html = self.qt_clipbrd_cache[hashed_html]
                
            else:
                html = self.sanitize_tags(clipbrd_html)

            
            cursor.insertHtml(html)

        elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_F:
            self.show_search_dialog()

        else:
            super().keyPressEvent(event)


    def show_search_dialog(self):
        search_dialog = s_find_dialog(self)
        search_dialog.exec_()


    def on_cursor_position_changed(self):
        cursor = self.textCursor()

        block_format = cursor.blockFormat()

        font = cursor.charFormat().font()

        action_map = self.tool_bar.action_map

        action_map['bold_action'].setChecked(True if font.bold() else False)
        action_map['italic_action'].setChecked(True if font.italic() else False)
        action_map['underline_action'].setChecked(True if font.underline() else False)

        action_map['bullet_action'].setChecked(True if cursor.currentList() else False)

        action_map['left_align_action'].setChecked(True if block_format.alignment() == Qt.AlignLeft else False)
        action_map['center_align_action'].setChecked(True if block_format.alignment() == Qt.AlignCenter else False)
        action_map['right_align_action'].setChecked(True if block_format.alignment() == Qt.AlignRight else False)


    def is_copy_key(
            self, 
            event
            ):
        return event.matches(QKeySequence.Copy)        


    def is_cut_key(
            self, 
            event
            ):
        return event.matches(QKeySequence.Cut) 


    def is_paste_key(
            self, 
            event
            ):
        return event.matches(QKeySequence.Paste)  


    def is_delete_key(
            self, 
            event
            ):
        return event.key() == Qt.Key_Backspace


    def is_delete_on_empty_line(
            self, 
            cursor
            ):
        return self.is_start_of_line(cursor) and not self.is_list(cursor)


    def is_delete_on_empty_list(
            self, 
            cursor
            ):
        return self.is_start_of_line(cursor) and self.is_list(cursor)


    def is_on_first_line(
            self, 
            cursor
            ):    
        return cursor.blockNumber() == 0


    def is_start_of_line(
            self, 
            cursor
            ):
        return cursor.positionInBlock() == 0


    def is_list(
            self, 
            cursor
            ):
        return cursor.currentList() != None


    def is_list_above(
            self, 
            cursor
            ):
        cursor.movePosition(QTextCursor.Up)
        is_list_above = cursor.currentList() != None
        
        cursor.movePosition(QTextCursor.Down)

        return is_list_above
    

    def create_empty_list(
            self, 
            cursor
            ):
        list_format = QTextListFormat()
        list_format.setStyle(QTextListFormat.ListDisc)

        cursor.createList(list_format)


    def reset_indent(
            self, 
            cursor
            ):
        block_format = cursor.blockFormat()
        block_format.setIndent(0)

        cursor.setBlockFormat(block_format)
           
        self.setTextCursor(cursor)


    def sanitize_tags(
            self, 
            html
            ):
        soup = BeautifulSoup(html, 'html.parser')

        allowed_tags = ['p', 'ul', 'li', '!DOCTYPE', 'body', 'html', 'style', 'br', 'span', 'b', 'i', 'u', 'div']

        for tag in soup.findAll(True):
            if tag.name not in allowed_tags:
                tag.extract()


        return str(soup)
    

    def set_qt_clipboard_cache(
            self, 
            cache
            ):
        self.qt_clipbrd_cache = cache


    def is_the_same_qt_clipboard_cache(
            self, 
            key
            ):
        return  self.qt_clipbrd_cache.get(key) != None


    # remove <!--StartFragment--> and <!--EndFragment--> 
    # becuase they are sometimes inserted inproperly
    def strip_qt_start_and_end_segments_tags(
            self, 
            html
            ):
        html = html.replace('<!--StartFragment-->', '')
        html = html.replace('<!--EndFragment-->', '')

        return html
    

    def strip_first_p_tag(
            self, 
            html
            ):
        soup = BeautifulSoup(html, "html.parser")

        # extract first p tag to remove newline char at the start of line
        first_p = soup.find("p")

        if first_p != None:
            first_p.extract()
            return str(soup)
        

        return html


    def get_hash_of_str(
            self,
            _str
            ):
        hash_object = hashlib.sha256()

        hash_object.update(_str.encode())

        hex_digest = hash_object.hexdigest()

        return str(int(hex_digest, 16))
    

    def highlight_selection(
            self, 
            cursor, 
            start_pos, 
            end_pos
            ):
        cursor.setPosition(start_pos)
        cursor.setPosition(end_pos, QTextCursor.KeepAnchor)
        
        self.setTextCursor(cursor)
        
