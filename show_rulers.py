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

def subactivity_init(api):
    api.declare_subactivity('ruler', ScreenOfRulers())

class ScreenOfRulers(paper.Drawing):
    def draw(self,c):
        self.set_background_color('white')

        c.set_antialias(cairo.ANTIALIAS_GRAY)

        self.draw_ruler_pair(c,mm(20))

        offset_of_xo_side_from_screen = mm(-38.5) #XXX needs checking
        c.move_to(offset_of_xo_side_from_screen, mm(65))
        self.draw_cm_ruler(c,180)
            
        offset_of_molding_from_screen = mm(-0.4) #XXX +- 0.2 ??
        c.move_to(offset_of_molding_from_screen, mm(100))
        self.draw_cm_ruler(c,150)

    def draw_ruler_pair(self,c,y):

        c.move_to(mm(10),y)
        self.connect_rulers(c)

        c.move_to(mm(10),y)
        self.draw_cm_ruler(c)

        c.move_to(mm(10),y+mm(10))
        self.draw_mm_ruler(c)
        
    def connect_rulers(self,c):
        c.save()
        c.set_line_cap(cairo.LINE_CAP_SQUARE)
        c.translate(*c.get_current_point())

        c.set_line_width(1)
        for xm in range(0,130+1,10):
            c.move_to(mm(xm),0)
            c.rel_line_to(0,mm(10))
        c.stroke()

        c.set_line_width(2)
        c.move_to(0,0)
        c.rel_line_to(0,mm(10))
        c.stroke()

        c.restore()

    def draw_cm_ruler(self,c,width=130):

        c.save()
        c.set_line_cap(cairo.LINE_CAP_SQUARE)
        c.translate(*c.get_current_point())

        c.set_line_width(5)
        c.move_to(0,0)
        c.line_to(mm(width),0)
        for x in [mm(xm) for xm in range(0,width+1,10)]:
            c.move_to(x,0)
            c.rel_line_to(0,mm(-3))
        c.stroke()

        self.set_font('helvetica bold 12')
        self.set_fontsize(mm(2.5))

        for x,xm in [(mm(xm),xm) for xm in range(0,width+1,10)]:
            n = xm/10
            c.move_to(x,mm(-4))
            self.write("%d" % n,centered=True)
            
        self.set_font('helvetica 12')
        self.set_fontsize(mm(2))

        c.move_to(mm(1.5),mm(-4))
        self.write("cm")

        c.restore()

    def draw_mm_ruler(self,c,width=130):

        c.save()
        c.set_line_cap(cairo.LINE_CAP_SQUARE)
        c.translate(*c.get_current_point())

        c.move_to(0,0)
        c.set_line_width(4)
        c.line_to(mm(width),0)
        for x in [mm(xm) for xm in range(0,width+1,10)]:
            c.move_to(x,0)
            c.rel_line_to(0,mm(3))
        c.stroke()

        c.set_line_width(3)
        for x in [mm(xm) for xm in range(0,width,5)]:
            c.move_to(x,0)
            c.rel_line_to(0,mm(2.2))
        for x in [mm(xm) for xm in range(0,width,1)]:
            c.move_to(x,0)
            c.rel_line_to(0,mm(2))
        c.stroke()

        self.set_font('helvetica 12')
        self.set_fontsize(mm(2))

        base = mm(7)
        for x,xm in [(mm(xm),xm) for xm in range(0,width+1,10)]:
            c.move_to(x,base)
            self.write("%d" % xm,centered=True)
            
        self.set_font('helvetica 12')
        self.set_fontsize(mm(1.5))

        c.move_to(mm(1.2),base)
        self.write("mm")

        c.restore()

