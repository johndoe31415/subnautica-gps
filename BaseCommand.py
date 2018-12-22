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
import collections
import time

class BaseCommand():
	def __init__(self, cmdname, args):
		self._cmdname = cmdname
		self._args = args

		with open(self._args.buoys_file) as f:
			buoys = json.load(f)

		self._buoys = collections.OrderedDict()
		for buoy in buoys:
			name = buoy["name"]
			self._buoys[name] = buoy
			buoy["2d"] = geo.Vector2D(buoy["coords"][0], buoy["coords"][1])
			buoy["3d"] = geo.Vector3D(buoy["coords"][0], buoy["coords"][1], buoy["coords"][2])

		self._locations = { name: geo.Vector3D(data["coords"][0], data["coords"][1], data["coords"][2]) for (name, data) in self._load_location_file().items() }

	def _read_coords(self, msg):
		data = input(msg).strip()
		if data == ".":
			data = "Liferaft"
		if data in self._buoys:
			return self._buoys[data]["2d"]

		if data in self._locations:
			return self._locations[data]

		coords = data.replace("/", "").split()
		if len(coords) == 2:
			return geo.Vector2D(float(coords[0]), float(coords[1]))
		elif len(coords) == 3:
			return geo.Vector2D(float(coords[0]), float(coords[1]), float(coords[2]))
		else:
			raise ValueError("Cannot parse coordinate form '%s'." % (data))

	def _load_location_file(self):
		try:
			with open("locations.json") as f:
				locations = json.load(f)
		except (FileNotFoundError, json.decoder.JSONDecodeError):
			locations = { }
		return locations

	def _save_location_file(self, locations):
		with open("locations.json", "w") as f:
			json.dump(locations, f, sort_keys = True, indent = 4)
			print(file = f)

	def _save_location(self, name, vector, method = None):
		locations = self._load_location_file()
		locations[name] = {
			"method":		method,
		}
		if vector.dim == 2:
			locations[name]["coords"] = [ vector.x, vector.y, 0 ]
		else:
			locations[name]["coords"] = list(vector)
		locations[name]["added_ts"] = time.time()
		self._save_location_file(locations)
