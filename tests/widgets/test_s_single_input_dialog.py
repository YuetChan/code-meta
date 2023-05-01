import sys
import os
import unittest

from PyQt5.QtWidgets import QApplication

# Add the parent directory of 'widgets' to the Python system path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..'))
sys.path.append(parent_dir)

from widgets.s_single_input_dialog import s_single_input_dialog

class test_s_single_input_dialog(unittest.TestCase):

    def setUp(self):
        self.app = QApplication([])

        self.dialog = s_single_input_dialog({
            'dialog_title': 'New Project',
            'dialog_var_1': 'project_name',
            'dialog_var_2': 'user',
            'dialog_msg_1': 'Enter a project name',
            'dialog_msg_2': 'Enter an username',
        })


    def tearDown(self):
        self.app.quit()

    
    def test_get_config_should_return_corresponded_config(self):
        self.dialog.line_edit.setText('test')
        
        self.assertEqual(self.dialog.get_config()['project_name'], 'test')

