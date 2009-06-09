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
import paper
import cairo
from util import mm
from math import pi

def subactivity_init(api):
    api.declare_subactivity('checker', ScreenOfCircles())

class ScreenOfCircles(paper.Drawing):
    def draw(self,c):
        self.set_background_color('white')
        c.set_antialias(cairo.ANTIALIAS_GRAY)

        def sq(x,y):
            c.rectangle(x,y,mm(10),mm(10))
            c.fill()
        
        w=100
        h=100
        for xm in range(0,w,20):
            for ym in range(0,h,20):
                sq(mm(xm),mm(ym))
        for xm in range(10,w,20):
            for ym in range(10,h,20):
                sq(mm(xm),mm(ym))

        c.set_line_width(1)
        c.move_to(mm(100),0)
        c.rel_line_to(0,mm(100))
        c.rel_line_to(mm(-100),0)
        c.stroke()

        c.set_line_width(3)
        v = 0.5
        c.set_source_rgb(v,v,v)
        c.move_to(mm(50),0)
        c.rel_line_to(0,mm(100))
        c.move_to(0,mm(50))
        c.rel_line_to(mm(100),0)
        c.stroke()
