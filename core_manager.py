from PyQt5.QtWidgets import QMessageBox

class core_manager:
  
    def __init__(
            self,
            file_tree,
            file_searcher,
            rich_text_editor,
            core_helper
            ):
        self.file_tree = file_tree
        self.file_searcher = file_searcher
        
        self.rich_text_editor = rich_text_editor

        self.core_helper = core_helper

        self.file_tree.file_clicked.connect(
            lambda data : self._on_file_tree_file_clicked(data['file_path'], data['is_dir'])
            )
    
        self.file_searcher.connect_file_clicked(
            lambda data : self._on_file_searcher_file_clicked(data['file_path'])
            )

        self.rich_text_editor.connect_text_changed(
            lambda data : self._auto_save_note(data)
            )

        self.file_tree.expand(self.file_tree.model().index(0, 0))
        self.file_tree.click_root_file()

        self.auto_delete_msg_box = QMessageBox()

        self.auto_delete_msg_box.setText("Would you like to add a placeholder to prevent the automatic deletion of an empty dangling note")
        self.auto_delete_msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        self.auto_delete_placeholder = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"><html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; }</style></head><body style=" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;"><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">placeholder</p></body></html>'


    def update(
            self, 
            file_tree,
            file_searcher,
            rich_text_editor, 
            core_helper
            ):
            self.file_tree = file_tree
            self.file_searcher = file_searcher
        
            self.rich_text_editor = rich_text_editor

            self.core_helper = core_helper

            self.file_tree.file_clicked.connect(
                lambda data: self._on_file_tree_file_clicked(data['file_path'], data['is_dir'])
            )
    
            self.file_searcher.connect_file_clicked(
                lambda data: self._on_file_searcher_file_clicked(data['file_path'])
            )

            self.rich_text_editor.connect_text_changed(
                lambda data: self._auto_save_note(data)
            )
            
            self.file_tree.expand(self.file_tree.model().index(0, 0))
            self.file_tree.click_root_file()


    def _on_file_tree_file_clicked(
            self, 
            fpath, 
            is_dir
            ):
        self.file_searcher.clear_selection()
        self._open_note(fpath, is_dir)


    def _on_file_searcher_file_clicked(
            self, 
            fpath
            ):
        print('fpath', fpath)

        self.file_tree.clearSelection()
        self._open_note(fpath, False)


    def _open_note(
            self, 
            fpath, 
            is_dir
            ):
        self.rich_text_editor.set_label(f"Directory :  {fpath}" if is_dir else f"File :  {fpath}")

        note = self.core_helper.select_note_by_filepath(fpath)

        if note != None:
            self.rich_text_editor.set_html(note['note'])
            self.rich_text_editor.set_default_setting()
            
        else:
            self.rich_text_editor.set_html('')
            self.rich_text_editor.set_default_setting()


        return


    def _auto_save_note(
            self, 
            data
            ): 
        if self.file_tree.selectionModel().hasSelection():
            self._auto_highlight_file_tree_file()
            self._save_note(self.file_tree.selected_fpath)

        elif self.file_searcher.has_selection():
            if self.rich_text_editor.to_plain_text() == '':
                self._auto_remove_n_save_file_searcher_empty_file()

            else:
                self._save_note(self.file_searcher.selected_fpath)


    def _auto_highlight_file_tree_file(self):
        if self.rich_text_editor.to_plain_text() != '':
            self.file_tree.highlight_selected_file()

        else:
            self.file_tree.unhighlight_selected_file()


    def _auto_remove_n_save_file_searcher_empty_file(self):
        result = self._prompt_placeholder_dialog()
            
        if result == QMessageBox.Yes:
            self.rich_text_editor.set_html(self.auto_delete_placeholder)
            self._save_note(self.file_searcher.selected_fpath)

        else:
            self.file_searcher.remove_selected_file()
            self._save_note(self.file_searcher.selected_fpath)
  
            if self.file_searcher.get_file_count() > 0:
                self.file_searcher.click_first_file()

            else:
                self.file_tree.click_root_file()


    def _save_note(
            self, 
            fpath
            ):
        self.core_helper.add_note_by_filepath(
            self.rich_text_editor.to_html(), 
            self.rich_text_editor.to_plain_text(),
            fpath
            )
        

    def _prompt_placeholder_dialog(self):
        return self.auto_delete_msg_box.exec_()

