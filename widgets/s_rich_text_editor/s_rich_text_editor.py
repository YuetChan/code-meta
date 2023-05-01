from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

from widgets.s_rich_text_editor.s_rich_text_tool_bar import s_rich_text_tool_bar
from widgets.s_rich_text_editor.s_rich_text_area import s_rich_text_area

# This class is a text editor that utilizes the s_rich_text_area and s_rich_text_tool_bar classes to provide its features. 

# It allows the user to set a label, toggle bullet points, disable or default all actions, set read-only mode, 
# connect to a text changed signal, 
# set HTML content, and convert to HTML or plain text.
class s_rich_text_editor(QWidget):

    def __init__(
            self,
            parent=None
            ):
        super(s_rich_text_editor, self).__init__(parent)

        self.rich_text_editor_label = QLabel('')

        self.rich_text_area = s_rich_text_area()

        self.rich_text_tool_bar = s_rich_text_tool_bar(self.rich_text_area)

        v_box = QVBoxLayout()

        v_box.addWidget(self.rich_text_editor_label)
        v_box.addWidget(self.rich_text_tool_bar)

        v_box.addWidget(self.rich_text_area)

        self.setLayout(v_box)


    def set_label(
            self, 
            label
            ):
        self.rich_text_editor_label.setText(label)


    def is_bullet_point_checked(self):
        return self.rich_text_tool_bar.action_map['bullet_action'].isChecked()
    

    def toggle_bullet_point(
            self, 
            checked
            ):
        self.rich_text_tool_bar.action_map['bullet_action'].setChecked(checked)


    def disable_all_actions(self):
        for action in self.rich_text_tool_bar.action_map.values():
            action.setEnabled(False)
            action.setChecked(False)


    def default_all_actions(self):
        for action in self.rich_text_tool_bar.action_map.values():
            action.setEnabled(True)
            action.setChecked(False)


        self.rich_text_tool_bar.action_map['left_align_action'].setChecked(True)


    def connect_text_changed(
            self, 
            l_func
            ):
        self.rich_text_area.text_changed.connect(
            lambda data : self._on_text_changed(l_func, data) 
            )   

    
    def set_read_only(self):
        self.rich_text_area.setReadOnly(True)
        self.rich_text_area.setStyleSheet("background-color: #f0f0f0;")

        self.rich_text_tool_bar.disable_all_actions()

        
    def set_default_setting(self):    
        self.rich_text_area.setReadOnly(False)
        self.rich_text_area.setStyleSheet("background-color: #FFFFFF;")  

        self.rich_text_tool_bar.default_all_actions()

    
    def set_html(
            self, 
            html
            ):
        self.rich_text_area.setHtml(html)


    def to_html(self):
        return self.rich_text_area.toHtml()
    

    def to_plain_text(self):
        return self.rich_text_area.toPlainText()
    

    def _on_text_changed(
            self, 
            l_func,
            data
            ):
        l_func(data)

