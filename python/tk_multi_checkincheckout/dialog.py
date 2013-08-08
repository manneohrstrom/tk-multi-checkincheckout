# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import tank
import os
import sys
import threading

from tank.platform.qt import QtCore, QtGui
from .ui.dialog import Ui_Dialog

class AppDialog(QtGui.QWidget):

    
    def __init__(self, app):
        QtGui.QWidget.__init__(self)
        
        # set up the UI
        self.ui = Ui_Dialog() 
        self.ui.setupUi(self)

        self._app = app
        
        
        # set up the browsers
        self.ui.left_browser.set_app(self._app)
        self.ui.right_browser.set_app(self._app)

            
        self.ui.left_browser.set_label("Publishes")
        self.ui.right_browser.set_label("Files")
        
                
        self.ui.left_browser.selection_changed.connect( self.setup_publish_list )
        self.ui.left_browser.selection_changed.connect( self.setup_publish_list )
        
        self.ui.right_browser.action_requested.connect( self.load_item )
        
        self.ui.left_browser.selection_changed.connect( self.toggle_load_button_enabled )
        self.ui.middle_browser.selection_changed.connect( self.toggle_load_button_enabled )
        self.ui.right_browser.selection_changed.connect( self.toggle_load_button_enabled )
                
        # load data from shotgun
        # this qsettings stuff seems super flaky on different platforms
        prev_selection = {}
        try:            
            type_key = "%s/curr_entity_type" % self._app.get_setting("menu_name")
            id_key = "%s/curr_entity_id" % self._app.get_setting("menu_name")
            entity_id = self._settings.value(id_key)
            entity_type = str(self._settings.value(type_key))
            prev_selection = {"type": entity_type, "id": entity_id}
        except Exception, e:
            self._app.log_warning("Cannot restore previous task state: %s" % e)
        
        self.setup_entity_list(prev_selection)
        
    ########################################################################################
    # make sure we trap when the dialog is closed so that we can shut down 
    # our threads. Nuke does not do proper cleanup on exit.
    
    def closeEvent(self, event):
        self.ui.left_browser.destroy()
        self.ui.right_browser.destroy()
        # okay to close!
        event.accept()
        
    ########################################################################################
    # basic business logic        
        
    def toggle_load_button_enabled(self):
        """
        Control the enabled state of the load button
        """
        curr_selection = self.ui.right_browser.get_selected_item()
        if curr_selection is None:
            self.ui.load_selected.setEnabled(False)
        else:
            self.ui.load_selected.setEnabled(True)

    def toggle_show_only_context(self):
        self.ui.left_browser.set_show_only_current(self.ui.show_current_checkbox.isChecked())
        self.ui.left_browser.clear()
        self.ui.middle_browser.clear()
        self.ui.right_browser.clear()
        d = { "prev_selection": self._app.context.entity}
        self.ui.left_browser.load(d)
        
        
    def setup_entity_list(self, prev_selection): 
        self.ui.left_browser.clear()
        self.ui.middle_browser.clear()
        self.ui.right_browser.clear()
        d = { "prev_selection": prev_selection}
        self.ui.left_browser.load(d)
        
    def setup_publish_list(self):
        
        self.ui.middle_browser.clear()
        self.ui.right_browser.clear()
        
        curr_selection = self.ui.left_browser.get_selected_item()
        if curr_selection is None:
            return
        
        # save selection
        type_key = "%s/curr_entity_type" % self._app.get_setting("menu_name")
        id_key = "%s/curr_entity_id" % self._app.get_setting("menu_name")
        self._settings.setValue(type_key, curr_selection.sg_data["type"])
        self._settings.setValue(id_key, curr_selection.sg_data["id"])
        
        d = {}
        d["entity"] = curr_selection.sg_data
        self.ui.middle_browser.load(d)
        
    def setup_version_list(self):
        
        self.ui.right_browser.clear()
        
        entity_selection = self.ui.left_browser.get_selected_item()
        if entity_selection is None:
            return
        
        publish_selection = self.ui.middle_browser.get_selected_item()
        if publish_selection is None:
            return
        
        d = {}
        d["entity"] = entity_selection.sg_data
        d["publish"] = publish_selection.sg_data
        self.ui.right_browser.load(d)
        
    def load_item(self):
        """
        Load something into the scene
        """
        curr_selection = self.ui.right_browser.get_selected_item()
        if curr_selection is None:
            return
        
        local_path = curr_selection.sg_data.get("path").get("local_path")

        if local_path is None:
            QtGui.QMessageBox.critical(self, 
                                       "No path!", 
                                       "This publish does not have a path associated!")
            return
        
        # call out to our hook for loading.
        self._app.log_debug("Calling scene load hook for %s - %s" % (local_path, curr_selection.sg_data))
        self._app.execute_hook("hook_add_file_to_scene", 
                               engine_name=self._app.engine.name, 
                               file_path=local_path, 
                               shotgun_data=curr_selection.sg_data)

        if self._app.get_setting("single_select", True):
            # single select mode!
            self.close()
        
        
