#	subnautica-gps - GPS geolocation for Subnautica
#	Copyright (C) 2018-2018 Johannes Bauer
#
#	This file is part of subnautica-gps.
#
#	subnautica-gps is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	subnautica-gps is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with subnautica-gps; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>

import json
import geo
from BaseCommand import BaseCommand
from Tools import AngleTools

class CommandGoto(BaseCommand):
	def __init__(self, cmdname, args):
		BaseCommand.__init__(self, cmdname, args)

		pos = self._read_coords("Current position: ")
		target = self._read_coords("Target          : ")
		far = input("How far    [1.0]: ").strip()
		if far == "":
			far = 1.0
		else:
			far = float(far)

		path = geo.Line.through(pt1 = pos, pt2 = target)
		target = path(far)

		vector = target - pos
		proj_vector = geo.Vector2D(vector.x, vector.y)
		compass = AngleTools.bearing_to_compass(proj_vector.bearing)

		# One subnautica compass tick is 7.5°
		ticks = compass.adjust / 7.5
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		print("Position          : %.0f / %.0f depth %.0f" % (pos.x, pos.y, pos.z))
		print("Target            : %.0f / %.0f depth %.0f" % (target.x, target.y, target.z))
		print("Distance to target: %.0f" % (vector.length))
		print("Bearing           : %.0f°" % (round(compass.bearing) % 360))
		print("Direction         : %s %+.0f° (%+.1f ticks)" % (compass.compass, compass.adjust, ticks))
		print("Depth difference  : %.0f" % (target.z -  pos.z))
