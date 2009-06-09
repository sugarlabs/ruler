# Copyright 2007 Mitchell N. Charity
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

from __future__ import division
import gtk
import pango
import pangocairo

class Drawing(gtk.DrawingArea):

    __gsignals__ = { "expose-event": "override" }

    def __init__(self):
        getattr(gtk.DrawingArea, '__init__', lambda x: None)(self)
        self._c = None
        self.font = None
        self.set_font('helvetica 12')

    def do_expose_event(self, event):

        c = self.window.cairo_create()
        c.rectangle(event.area.x, event.area.y,
                    event.area.width, event.area.height)
        c.clip()
        self._c = c
        self.draw(c)
        self._c = None


    def set_background_color(self,name):

        c = self._c
        w,h = self.window.get_size()
        c.save()
        c.rectangle(0,0,w,h)
        c.set_source_color(gtk.gdk.color_parse('white'))
        c.fill()
        c.restore()

    def set_color(self,name):

        c = self._c
        c.set_source_color(gtk.gdk.color_parse(name))


    def set_font(self,name):
        self.font = pango.FontDescription(name)

    def set_fontsize(self,size):
        self.font.set_size(int(round(size*pango.SCALE)))

    def write(self,text,centered=False,at_top=False):
        c = self._c
        pc = pangocairo.CairoContext(c)

        baseline_offset = - self.width_and_height_of_text("X")[1]
        if not at_top:
            c.rel_move_to(0,baseline_offset)

        lo = pc.create_layout()
        lo.set_font_description(self.font)
        lo.set_text(text)
        extent =[x/pango.SCALE for x in lo.get_extents()[1]]
        ex,ey = extent[2],extent[3]
        if centered:
            c.rel_move_to(-ex/2,0)
        pc.show_layout(lo)
        c.rel_move_to(ex,0)

        if not at_top:
            c.rel_move_to(0,-baseline_offset)

    #XX TODO switch to text_extent()
    def width_and_height_of_text(self,text):
        c = self._c
        pc = pangocairo.CairoContext(c)
        lo = pc.create_layout()
        lo.set_font_description(self.font)
        lo.set_text("X")
        extent = [x/pango.SCALE for x in lo.get_extents()[1]]
        ex,ey = extent[2],extent[3]
        return ex,ey
