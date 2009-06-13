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
import os
import subprocess
import re
import subactivity

def full_path(*args):
    return os.path.join(sugar.activity.activity.get_bundle_path(),*args)

def image_from_file(filename):
    img = gtk.Image()
    fn = full_path(filename)
    img.set_from_file(fn)
    return img

def toolbutton_from_image(img):
    button = sugar.graphics.toolbutton.ToolButton('go-next') #X
    button.set_icon_widget(img)
    img.show()
    button.show()
    return button

def mm(n):
    return n / 25.40 * subactivity.dpi

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

