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

import dbus
from os import path

import pango
import pangocairo


def get_hardware():
    """ Determine whether we are using XO 1.0, 1.5, or "unknown" hardware """
    bus = dbus.SystemBus()

    comp_obj = bus.get_object('org.freedesktop.Hal',
                              '/org/freedesktop/Hal/devices/computer')
    dev = dbus.Interface(comp_obj, 'org.freedesktop.Hal.Device')
    if dev.PropertyExists('system.hardware.vendor') and \
            dev.PropertyExists('system.hardware.version'):
        if dev.GetProperty('system.hardware.vendor') == 'OLPC':
            if dev.GetProperty('system.hardware.version') == '1.5':
                return 'XO15'
            else:
                return 'XO1'
        else:
            return 'UNKNOWN'
    elif path.exists('/etc/olpc-release') or \
         path.exists('/sys/power/olpc-pm'):
        return 'XO1'
    else:
        return 'UNKNOWN'


def mm(dpi, n):
    """ Convert n pixels to units mm """
    return n / 25.40 * dpi


def dimensions_mm(dpi, w, h):
    """ Return screen width, height in units mm """
    return int(w * 25.40 / dpi), int(h * 25.40 / dpi)

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
def set_background_color(c, w, h):
    c.save()
    c.rectangle(0, 0, w, h)
    c.set_source_color(gtk.gdk.color_parse('white'))
    c.fill()
    c.restore()


def set_color(c, name):
    c.set_source_color(gtk.gdk.color_parse(name))


def write(c, text, name, size, centered=False, at_top=False):
    pc = pangocairo.CairoContext(c)

    font = pango.FontDescription(name)
    font.set_size(int(round(size * pango.SCALE)))
    lo = pc.create_layout()
    lo.set_font_description(font)
    lo.set_text("X")
    extent = [x/pango.SCALE for x in lo.get_extents()[1]]
    ex, ey = extent[2], extent[3]
    baseline_offset = -ey
    if not at_top:
        c.rel_move_to(0, baseline_offset)

    lo = pc.create_layout()
    lo.set_font_description(font)
    lo.set_text(text)
    extent =[x/pango.SCALE for x in lo.get_extents()[1]]
    ex, ey = extent[2], extent[3]
    if centered:
        c.rel_move_to(-ex / 2, 0)
    pc.show_layout(lo)
    c.rel_move_to(ex, 0)

    if not at_top:
        c.rel_move_to(0, -baseline_offset)
