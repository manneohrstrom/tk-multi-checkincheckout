
"""
Check in and out files.
"""

import tank
import sys
import os

class MultiCheckinCheckout(tank.platform.Application):
    
    def init_app(self):
        """
        Called as the application is being initialized
        """
        tk_multi_loader = self.import_module("tk_multi_checkincheckout")
        cb = lambda : tk_multi_loader.show_dialog(self)
        
        # add stuff to main menu
        self.engine.register_command("Checkin Checkout", cb)

