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

class CommandTrilaterate(BaseCommand):
	def __init__(self, cmdname, args):
		BaseCommand.__init__(self, cmdname, args)

		known_distances = 0
#		self._buoys["Liferaft"]["dist"] = 1000
#		self._buoys["NAV N 1k"]["dist"] = 5
#		self._buoys["NAV W 1k"]["dist"] = 1414
		for (name, buoy) in self._buoys.items():
			if "dist" in buoy:
				known_distances += 1
				continue

			try:
				dist_to_pt = int(input("Distance to %s: " % (name)).strip())
			except ValueError:
				continue

			buoy["dist"] = dist_to_pt
			known_distances += 1
			if known_distances == 3:
				break

		if known_distances < 2:
			print("Need at least two distances to calculate.")
		else:
			points = { name: buoy for (name, buoy) in self._buoys.items() if "dist" in buoy }
			circles = { name: geo.Circle(buoy["2d"], buoy["dist"]) for (name, buoy) in points.items() }
			(intersection, remaining) = geo.Circle.find_circle_intersection(circles.values())

			(i1, i2) = intersection
			if len(remaining) == 0:
				print("Current coordinates are one of (distance between options %.0f):" % (i1.dist(i2)))
				print("    %.0f / %.0f" % (i1.x, i1.y))
				print("    %.0f / %.0f" % (i2.x, i2.y))
			else:
				c3 = remaining[0]
				d1 = c3.dist(i1)
				d2 = c3.dist(i2)
				if d1 < d2:
					i = i1
				else:
					i = i2
				print("Current coordinates are: %.0f / %.0f (distance from prediction %.0f)" % (i.x, i.y, c3.dist(i)))
				name = input("Save this location as: ").strip()
				if name != "":
					self._save_location(name, i, method = "trilateration/2d")
