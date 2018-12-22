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

		vector = target - pos
		compass = AngleTools.bearing_to_compass(vector.bearing)
		# One subnautica compass tick is 7.5°
		ticks = compass.adjust / 7.5
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		print("Distance to target: %.0f" % (vector.length))
		print("Bearing           : %.0f°" % (compass.bearing))
		print("Direction         : %s %+.1f" % (compass.compass, ticks))

