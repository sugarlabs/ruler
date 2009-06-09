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
from math import pi,sin,cos

from colorsys import * #XXX

def d2r(d):
    return d/180*pi

def subactivity_init(api):
    api.declare_subactivity('angles-360', Angles360())
    api.declare_subactivity('angles-90', Angles90())
    #api.declare_subactivity('angles-180', Angles90())

class Angles90(paper.Drawing):
    def draw(self,c):
        self.set_background_color('white')

        c.set_antialias(True)

        ox = mm(0)
        oy = mm(99)
        d = mm(90)
        def xy(angle,m=d):
            return cos(-angle)*m+ox,sin(-angle)*m+oy
        def ray(angle,r0=0,r1=d):
            c.move_to(*xy(angle,r0))
            c.line_to(*xy(angle,r1))

        lw = 6
        c.set_line_width(lw)
        c.move_to(ox,oy+lw/2)
        c.line_to(*xy(pi/2))
        ray(0)
        c.stroke()

        c.save()
        c.set_line_width(3)
        c.set_dash([mm(5)])
        ray(pi/4)
        c.stroke()
        c.restore()

        c.set_line_width(4)
        for a in range(10,81,10):
            ray(d2r(a),mm(10),mm(85))
        c.stroke()
        c.set_line_width(2)
        for a in range(10,81,10):
            ray(d2r(a),mm(3),mm(20))
        c.stroke()

        c.set_line_width(2)
        for a in range(1,90,1):
            ray(d2r(a),mm(70),mm(80))
        c.stroke()
        c.set_line_width(2)
        for a in range(0,90,5):
            ray(d2r(a),mm(20),mm(81))
        c.stroke()

class Angles360(paper.Drawing):
    def draw(self,c):
        self.set_background_color('white')
        c.set_antialias(True)

        ox = mm(75)
        oy = mm(50)
        d = mm(44)
        def xy(angle,m=d):
            return cos(-angle)*m+ox,sin(-angle)*m+oy
        def ray(angle,r0=0,r1=d):
            c.move_to(*xy(angle,r0))
            c.line_to(*xy(angle,r1))
        def annulus(a0,a1,r0,r1):
            c.move_to(*xy(a0,r0))
            c.arc_to(ox,oy,r0,a0,a1)
            c.rel_line_to(*xy(a1,r1))
            c.arc_to(ox,oy,r1,a1,a0)
            c.close_path()

        def rays(step,r0=0,r1=d,w=1):
            c.save()
            c.set_line_width(w)
            for a in range(0,360,step):
                ray(d2r(a),r0,r1)
            c.stroke()
            c.restore()

        rays(1,mm(35),w=2,r1=mm(43))
        rays(5,mm(10),w=2)
        rays(10,mm(10),w=4)
#        rays(10,mm(3),mm(20),w=2)
        c.save()
        #c.set_dash([mm(5)])
        self.set_color('dark gray')
        rays(45,0,mm(45),w=6)
        c.restore()
        rays(90,0,mm(45),w=6)
