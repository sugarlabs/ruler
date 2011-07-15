# Copyright (c) 2007 Mitchell N. Charity
# Copyright (c) 2009-2011 Walter Bender
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

import pygtk
pygtk.require('2.0')
import gtk
import gobject

import cairo

import os.path

import sugar
from sugar.activity import activity
try:  # 0.86+ toolbar widgets
    from sugar.graphics.toolbarbox import ToolbarBox
    HAS_TOOLARBOX = True
except ImportError:
    HAS_TOOLARBOX = False

if HAS_TOOLARBOX:
    from sugar.bundle.activitybundle import ActivityBundle
    from sugar.activity.widgets import ActivityToolbarButton
    from sugar.activity.widgets import StopButton
    from sugar.graphics.toolbarbox import ToolbarButton

from sugar.graphics.radiotoolbutton import RadioToolButton
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.menuitem import MenuItem
from sugar.graphics.icon import Icon
from sugar.datastore import datastore
try:
    from sugar.graphics import style
    GRID_CELL_SIZE = style.GRID_CELL_SIZE
except ImportError:
    GRID_CELL_SIZE = 0

import logging
_logger = logging.getLogger("ruler-activity")

from gettext import gettext as _

from util import get_hardware
import show_rulers
import show_grids
import show_checkers
import show_angles


class MyCanvas(gtk.DrawingArea):
    ''' Create a GTK+ widget on which we will draw using Cairo '''

    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self._draw_ruler = False
        self._object = None
        self.connect('expose-event', self.__expose_event_cb)
        self.dpi = 200

    def __expose_event_cb(self, drawing_area, event):
        cr = self.window.cairo_create()

        if self._draw_ruler:
            self._object.draw(cr, self._dpi)

        # Restrict Cairo to the exposed area; avoid extra work
        cr.rectangle(event.area.x, event.area.y,
                     event.area.width, event.area.height)
        cr.clip()

    def add_a_ruler(self, r):
        self._draw_ruler = True
        self._object = r
        self.queue_draw()

    def get_dpi(self):
        return self._dpi

    def set_dpi(self, dpi):
        self._dpi = dpi


#
# Sugar activity
#
class RulerActivity(activity.Activity):

    def __init__(self, handle):
        super(RulerActivity, self).__init__(handle)

        self.button_dict = {}
        self.callback_dict = {}
        self._ready = False

        _font = 'helvetica 12'
        _font_bold = 'helvetica bold 12'

        #
        # We need a canvas
        #
        self._canvas = MyCanvas()
        self.set_canvas(self._canvas)
        self._canvas.show()

        _width = gtk.gdk.screen_width()
        _height = gtk.gdk.screen_height() - GRID_CELL_SIZE

        # Read the dpi from the Journal
        if get_hardware()[0:2] == 'XO':
            self._canvas.set_dpi(200)  # OLPC XO
            self.known_dpi = True
        else:
            self.known_dpi = False
            try:
                dpi = self.metadata['dpi']
                _logger.debug("Read dpi: " + str(dpi))
                self._canvas.set_dpi(int(dpi))
            except KeyError:
                self._canvas.set_dpi(96)  # Just a guess

        # Create instances of our graphics
        self._r = show_rulers.ScreenOfRulers(_font, _font_bold, _width,
                                             _height)
        self._gcm = show_grids.ScreenGrid_cm(_font, _font_bold, _width,
                                             _height)
        self._gmm = show_grids.ScreenGrid_mm(_font, _font_bold, _width,
                                             _height)
        self._a90 = show_angles.Angles90(_font, _font_bold, _width, _height)
        self._a360 = show_angles.Angles360(_font, _font_bold, _width, _height)
        self._c = show_checkers.ScreenOfCircles(_font, _font_bold, _width,
                                                _height)

        # start with a ruler
        self._current = self._r
        self._canvas.add_a_ruler(self._current)

        # other settings
        self._grids_mode = "cm"
        self._angles_mode = "90"

        #
        # We need some toolbars
        #
        self.max_participants = 1

        if HAS_TOOLARBOX:
            # Use 0.86 toolbar design
            toolbar_box = ToolbarBox()

            # Buttons added to the Activity toolbar
            activity_button = ActivityToolbarButton(self)
            toolbar_box.toolbar.insert(activity_button, 0)
            activity_button.show()

            self.rulers = MyButton(self, 'ruler',
                                   icon_name='ruler',
                                   callback=self._rulers_cb,
                                   tooltip=_('Ruler'))
            toolbar_box.toolbar.insert(self.rulers, -1)

            self.grids = MyButton(self, 'grids',
                                  icon_name='grid-a',
                                  callback=self._grids_cb,
                                  tooltip=_('Grid'),
                                  group=self.rulers)
            toolbar_box.toolbar.insert(self.grids, -1)

            self.angles = MyButton(self, 'angles',
                                   icon_name='angles-90',
                                   callback=self._angles_cb,
                                   tooltip=_('Angles'),
                                   group=self.rulers)
            toolbar_box.toolbar.insert(self.angles, -1)

            self.checker = MyButton(self, 'checker',
                                    icon_name='checker',
                                    callback=self._checker_cb,
                                    tooltip=_('Checker'),
                                    group=self.rulers)
            toolbar_box.toolbar.insert(self.checker, -1)

            if not self.known_dpi:
                separator = gtk.SeparatorToolItem()
                separator.show()
                toolbar_box.toolbar.insert(separator, -1)

                dpi = self._canvas.get_dpi()
                self._dpi_spin_adj = gtk.Adjustment(dpi, 72, 200, 2, 32, 0)
                self._dpi_spin = gtk.SpinButton(self._dpi_spin_adj, 0, 0)
                self._dpi_spin_id = self._dpi_spin.connect('value-changed',
                                                           self._dpi_spin_cb)
                self._dpi_spin.set_numeric(True)
                self._dpi_spin.show()
                self.tool_item_dpi = gtk.ToolItem()
                self.tool_item_dpi.add(self._dpi_spin)
                toolbar_box.toolbar.insert(self.tool_item_dpi, -1)
                self.tool_item_dpi.show()

            separator = gtk.SeparatorToolItem()
            separator.props.draw = False
            separator.set_expand(True)
            separator.show()
            toolbar_box.toolbar.insert(separator, -1)

            # The ever-present Stop Button
            stop_button = StopButton(self)
            stop_button.props.accelerator = '<Ctrl>Q'
            toolbar_box.toolbar.insert(stop_button, -1)
            stop_button.show()

            self.set_toolbar_box(toolbar_box)
            toolbar_box.show()

        else:
            # Use pre-0.86 toolbar design
            toolbox = activity.ActivityToolbox(self)
            self.set_toolbox(toolbox)

            self.projectToolbar = ProjectToolbar(self)
            toolbox.add_toolbar(_('Rulers'), self.projectToolbar)

            toolbox.show()
            toolbox.set_current_toolbar(1)

        self.show_all()

        # Restore state if previously saved
        self._ready = True
        if 'ruler' in self.metadata and \
           self.metadata['ruler'] in self.button_dict:
            _logger.debug('restoring %s', self.metadata['ruler'])
            if HAS_TOOLARBOX:
                self.button_dict[self.metadata['ruler']].set_active(True)
            self.callback_dict[self.metadata['ruler']]
        else:
            self._rulers_cb()
            if HAS_TOOLARBOX:
                self.rulers.set_active(True)

    #
    # Button callbacks
    #
    def _rulers_cb(self, button=None):
        if self._ready:
            self._current = self._r
            self._canvas.add_a_ruler(self._current)
            _logger.debug('selecting ruler')
            self.metadata['ruler'] = 'ruler'
        return False

    def _grids_cb(self, button=None):
        if self._ready:
            if self._grids_mode == "cm":
                self._current = self._gcm
                if hasattr(self, 'grids'):
                    self.grids.set_icon("grid-c")
                self._grids_mode = "mm"
            else:
                self._current = self._gmm
                if hasattr(self, 'grids'):
                    self.grids.set_icon("grid-a")
                self._grids_mode = "cm"
            self._canvas.add_a_ruler(self._current)
            _logger.debug('selecting grids')
            self.metadata['ruler'] = 'grids'
        return False

    def _angles_cb(self, button=None):
        if self._ready:
            if self._angles_mode == "90":
                self._current = self._a90
                if hasattr(self, 'angles'):
                    self.angles.set_icon("angles-360")
                    self._angles_mode = "360"
            else:
                self._current = self._a360
                if hasattr(self, 'angles'):
                    self.angles.set_icon("angles-90")
                    self._angles_mode = "90"
            self._canvas.add_a_ruler(self._current)
            _logger.debug('selecting angles')
            self.metadata['ruler'] = 'angles'
        return False

    def _checker_cb(self, button=None):
        if self._ready:
            self._current = self._c
            self._canvas.add_a_ruler(self._current)
            _logger.debug('selecting checker')
            self.metadata['ruler'] = 'checker'
        return False

    def _dpi_spin_cb(self, button):
        self._canvas.set_dpi(self._dpi_spin.get_value_as_int())
        self._canvas.add_a_ruler(self._current)
        return

    def write_file(self, file_path):
        ''' Write the dpi to the Journal '''
        dpi = self._canvas.get_dpi()
        _logger.debug("Write dpi: " + str(dpi))
        self.metadata['dpi'] = str(dpi)


class ProjectToolbar(gtk.Toolbar):
    ''' Project toolbar for pre-0.86 toolbars '''

    def __init__(self, pc):
        gtk.Toolbar.__init__(self)
        self.activity = pc

        # Ruler
        self.activity.rulers = ToolButton("ruler")
        self.activity.rulers.set_tooltip(_('Ruler'))
        self.activity.rulers.props.sensitive = True
        self.activity.rulers.connect('clicked', self.activity._rulers_cb)
        self.insert(self.activity.rulers, -1)
        self.activity.rulers.show()

        # Grid
        self.activity.grids = ToolButton("grid-a")
        self.activity.grids.set_tooltip(_('Grid'))
        self.activity.grids.props.sensitive = True
        self.activity.grids.connect('clicked', self.activity._grids_cb)
        self.insert(self.activity.grids, -1)
        self.activity.grids.show()

        # Angles
        self.activity.angles = ToolButton("angles-90")
        self.activity.angles.set_tooltip(_('Angles'))
        self.activity.angles.props.sensitive = True
        self.activity.angles.connect('clicked', self.activity._angles_cb)
        self.insert(self.activity.angles, -1)
        self.activity.angles.show()

        # Checker
        self.activity.checker = ToolButton("checker")
        self.activity.checker.set_tooltip(_('Checker'))
        self.activity.checker.props.sensitive = True
        self.activity.checker.connect('clicked', self.activity._checker_cb)
        self.insert(self.activity.checker, -1)
        self.activity.checker.show()

        if not self.activity.known_dpi:
            separator = gtk.SeparatorToolItem()
            separator.set_draw(True)
            self.insert(separator, -1)
            separator.show()

            dpi = self.activity._canvas.get_dpi()
            self.activity._dpi_spin_adj = gtk.Adjustment(
                dpi, 72, 200, 2, 32, 0)
            self.activity._dpi_spin = \
                gtk.SpinButton(self.activity._dpi_spin_adj, 0, 0)
            self.activity._dpi_spin_id = self.activity._dpi_spin.connect(
                'value-changed', self.activity._dpi_spin_cb)
            self.activity._dpi_spin.set_numeric(True)
            self.activity._dpi_spin.show()
            self.activity.tool_item_dpi = gtk.ToolItem()
            self.activity.tool_item_dpi.add(self.activity._dpi_spin)
            self.insert(self.activity.tool_item_dpi, -1)
            self.activity.tool_item_dpi.show()


class MyButton(RadioToolButton):

    def __init__(self, parent, name, icon_name='', callback=None,
                 tooltip=None, group=None):
        RadioToolButton.__init__(self)

        if icon_name == '':
            icon_name = 'computer-xo'
        icon = Icon(icon_name=icon_name,
                    icon_size=gtk.ICON_SIZE_LARGE_TOOLBAR)
        self.set_icon_widget(icon)
        icon.show()
        if tooltip is not None:
            self.set_tooltip(tooltip)
        self.props.sensitive = True
        self.connect('clicked', callback)
        self.set_group(group)
        self.show()

        parent.button_dict[name] = self
        parent.callback_dict[name] = callback

    def set_icon(self, name):
        icon = Icon(icon_name=name,
                    icon_size=gtk.ICON_SIZE_LARGE_TOOLBAR)
        self.set_icon_widget(icon)
        icon.show()
