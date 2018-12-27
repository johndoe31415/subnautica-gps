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
from ImplicitLocation import ImplicitLocation

class CommandTrilaterate(BaseCommand):
	def __init__(self, cmdname, args):
		BaseCommand.__init__(self, cmdname, args)

		location = ImplicitLocation.input_keyboard(self._buoys)
		(coords, error) = location.calculate_coordinates(self._buoys)
		print("Position: %.0f / %.0f depth %.0f (error %.0f)" % (coords.x, coords.y, coords.z, error))

		location_name = input("Location name: ").strip()
		if location_name != "":
			self._save_location(location_name, location, coords)
