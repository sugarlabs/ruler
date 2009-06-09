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

import subactivity

class RulerActivity(subactivity.Activity):

    def configure_subactivities(self):

        self.add_subactivity('show_rulers')
        self.add_subactivity('show_grids')
        self.add_subactivity('show_checkers')
        self.add_subactivity('show_angles')
