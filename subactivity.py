# Copyright 2007 Mitchell N. Charity
# Copyright 2009 Walter Bender
#
# This file is part of Ruler.
#
# Ruler is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ruler is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ruler.  If not, see <http://www.gnu.org/licenses/>

import gtk
import sugar
from util import calc_dpi
from sugar.activity import activity
from gettext import gettext as _

dpi = 96 # reasonable default

class Activity(activity.Activity):

    def __init__(self, handle, browser=None):
        activity.Activity.__init__(self, handle)

        toolbox = activity.ActivityToolbox(self)
        toolbox.show()
        self.set_toolbox(toolbox)

        tab_text = _(sugar.activity.activity.get_bundle_name())
        self.toolbar = gtk.Toolbar()
        self.toolbar.show()
        toolbox.add_toolbar(tab_text,self.toolbar)

        self._page_box = gtk.VBox()
        self._page_box.show()
        self.set_canvas(self._page_box)
        self.page = None

        dpi = calc_dpi()
        self._init_api = SubActivityInitApi(self)
        self.configure_subactivities()

    def set_page(self,widget):

        for w in self._page_box.get_children():
            self._page_box.remove(w)

        self._page_box.pack_start(widget, True,True)
        widget.show()
        
        self.page = widget

    def add_subactivity(self,module_name):

        d = {'api': self._init_api}
        code = ("import "+module_name+"\n"+
                ""+module_name+".subactivity_init(api)\n")
        exec code in d


class SubActivityInitApi:

    def __init__(self,activity):
        self.activity = activity

    def declare_subactivity(self,icon,page,toolbar=None):

        button = sugar.graphics.toolbutton.ToolButton(icon)
        button.connect('clicked',self._cb_set_page,page)
        button.show()
        
        self.activity.toolbar.insert(button,-1)

        if not self.activity.page:
            self.activity.set_page(page)

    def _cb_set_page(self,button,page):
        self.activity.set_page(page)
        self.activity.queue_draw()
