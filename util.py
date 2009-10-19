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

import pygtk
pygtk.require('2.0')
import gtk
import gobject
import pango
import pangocairo

def mm(dpi,n):
    return n / 25.40 * dpi

"""
def calc_dpmm():
    return 1.0*gtk.gdk.screen_width()/gtk.gdk.screen_width_mm()

def calc_dpi():
# will use xrdb query to get dpi
# $ xdpyinfo
# looking for something similar to "  resolution:    96x96 dots per inch"

    cmd = "/usr/bin/xdpyinfo"
    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        xrdb_output = re.split("\n",proc.communicate()[0])
        for i in xrdb_output:
            if i != "":
                a = re.split(":",i)
                if a[0] == '  resolution':
                    for b in re.split("\s",a[1]):
                        if b != "":
                            c = re.split("x",b)
                            if len(c) > 1:
                                print "looking up dpi: " + c[0]
                                return(int(c[0]))
    except:
        # just in case the above fails
        print "defaulting to 96 dpi"
        return(96)
"""

#
# Cairo-related utilities
#
def set_background_color(c,w,h):
    c.save()
    c.rectangle(0,0,w,h)
    c.set_source_color(gtk.gdk.color_parse('white'))
    c.fill()
    c.restore()

def set_color(c,name):
    c.set_source_color(gtk.gdk.color_parse(name))

def write(c,text,name,size,centered=False,at_top=False):
    pc = pangocairo.CairoContext(c)

    font = pango.FontDescription(name)
    font.set_size(int(round(size*pango.SCALE)))
    lo = pc.create_layout()
    lo.set_font_description(font)
    lo.set_text("X")
    extent = [x/pango.SCALE for x in lo.get_extents()[1]]
    ex,ey = extent[2],extent[3]
    baseline_offset = -ey
    if not at_top:
        c.rel_move_to(0,baseline_offset)

    lo = pc.create_layout()
    lo.set_font_description(font)
    lo.set_text(text)
    extent =[x/pango.SCALE for x in lo.get_extents()[1]]
    ex,ey = extent[2],extent[3]
    if centered:
        c.rel_move_to(-ex/2,0)
    pc.show_layout(lo)
    c.rel_move_to(ex,0)

    if not at_top:
        c.rel_move_to(0,-baseline_offset)
