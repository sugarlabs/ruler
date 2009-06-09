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

import gtk
import os
#import sugar

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
    return n / 25.40 * 200
