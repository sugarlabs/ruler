# Copyright 2007 Mitchell N. Charity
# Copyright 2009, 2012 Walter Bender
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

import os
import subprocess
from string import find

import pango
import pangocairo

XO1 = 'xo1'
XO15 = 'xo1.5'
XO175 = 'xo1.75'
UNKNOWN = 'unknown'


def get_hardware():
    """ Determine whether we are using XO 1.0, 1.5, or "unknown" hardware """
    product = _get_dmi('product_name')
    if product is None:
        if os.path.exists('/etc/olpc-release') or \
           os.path.exists('/sys/power/olpc-pm'):
            return XO1
        elif os.path.exists('/sys/devices/platform/lis3lv02d/position'):
            return XO175  # FIXME: temporary check for XO 1.75
        else:
            return UNKNOWN
    if product != 'XO':
        return UNKNOWN
    version = _get_dmi('product_version')
    if version == '1':
        return XO1
    elif version == '1.5':
        return XO15
    else:
        return XO175


def _get_dmi(node):
    ''' The desktop management interface should be a reliable source
    for product and version information. '''
    path = os.path.join('/sys/class/dmi/id', node)
    try:
        return open(path).readline().strip()
    except:
        return None


def mm(dpi, n):
    """ Convert n pixels to units mm """
    return n / 25.40 * dpi


def dimensions_mm(dpi, w, h):
    """ Return screen width, height in units mm """
    return int(w * 25.40 / dpi), int(h * 25.40 / dpi)


def calc_dpi():
    '''Looking for 'dimensions' line in xdpyinfo
       dimensions:    1280x800 pixels (339x212 millimeters)'''
    output = check_output('/usr/bin/xdpyinfo', 'xdpyinfo failed')
    if output is not None:
        strings = output[find(output, 'dimensions:'):].split()
        w = int(strings[1].split('x')[0])  # e.g., 1280x800
        mm = int(strings[3][1:].split('x')[0])  # e.g., (339x212)
        return int((w * 25.4 / mm) + 0.5), True
    else:
        return 96, False


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
    lo.set_text('X')
    extent = [x / pango.SCALE for x in lo.get_extents()[1]]
    ex, ey = extent[2], extent[3]
    baseline_offset = -ey
    if not at_top:
        c.rel_move_to(0, baseline_offset)

    lo = pc.create_layout()
    lo.set_font_description(font)
    lo.set_text(text)
    extent = [x / pango.SCALE for x in lo.get_extents()[1]]
    ex, ey = extent[2], extent[3]
    if centered:
        c.rel_move_to(-ex / 2, 0)
    pc.show_layout(lo)
    c.rel_move_to(ex, 0)

    if not at_top:
        c.rel_move_to(0, -baseline_offset)


def check_output(command, warning):
    ''' Workaround for old systems without subprocess.check_output'''
    if hasattr(subprocess, 'check_output'):
        try:
            output = subprocess.check_output(command)
        except subprocess.CalledProcessError:
            log.warning(warning)
            return None
    else:
        import commands

        cmd = ''
        for c in command:
            cmd += c
            cmd += ' '
        (status, output) = commands.getstatusoutput(cmd)
        if status != 0:
            log.warning(warning)
            return None
    return output
