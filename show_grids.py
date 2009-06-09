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
import cairo
import paper
from util import mm

def subactivity_init(api):

    api.declare_subactivity("grid-a", ScreenGrid_cm())
    api.declare_subactivity("grid-c", ScreenGrid_mm())


class ScreenGrid_mm(paper.Drawing):

    def draw(self,c):
        self.set_background_color('white')
        #c.set_antialias(cairo.ANTIALIAS_GRAY)
        draw_numbers(self,c,10,"mm")
        draw_grid(c,1,1)
        draw_grid(c,10,2)
        draw_grid(c,100,3.5)

class ScreenGrid_cm(paper.Drawing):

    def draw(self,c):
        self.set_background_color('white')
        c.set_antialias(cairo.ANTIALIAS_GRAY)
        draw_numbers(self,c)
        draw_grid(c,10,2)
        draw_grid(c,100,3.5)


def draw_numbers(p,c,m=1,unit="cm"):
    c.save()
    fh = mm(4)
    p.set_font('helvetica bold 12')
    p.set_fontsize(fh)
    v = 0.7
    c.set_source_rgb(v,v,v)
    for n in range(1,11):
        c.move_to(mm(n*10),mm(n*10))
        c.rel_move_to(mm(0),mm(3))
        p.write("%d" % (n*m),centered=True)
        if n == 1:
            c.rel_move_to(mm(-0.5),mm(-0.5))
            p.set_fontsize(mm(3))
            p.write(" "+unit)
            p.set_fontsize(fh)
    c.restore()


def draw_grid(c,step,stroke):

    c.save()
    c.set_line_width(stroke)
    lay_mm_grid(c,step_mm=step)
    c.stroke()
    c.restore()


def lay_mm_grid(c,width_mm=152,height_mm=114,step_mm=1):

    c.save()
    z = mm(1)
    c.scale(z,z)
    for x in range(0,width_mm,step_mm):
        c.move_to(x,0)
        c.rel_line_to(0,height_mm)
    for y in range(0,height_mm,step_mm):
        c.move_to(0,y)
        c.rel_line_to(width_mm,0)
    c.restore()
