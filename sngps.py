#!/usr/bin/env python3
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

with open("known.json") as f:
	known_points = json.load(f)
points_by_name = { point["name"] : point for point in known_points }
for (name, data) in points_by_name.items():
	data["2d"] = geo.Vector2D(data["coords"][0], data["coords"][1])
	data["3d"] = geo.Vector3D(data["coords"][0], data["coords"][1], data["coords"][2])

distances = { }
#	"Liferaft":		1000,
#	"NAV N 1k":		3,
#	"NAV N 1k":		2004,
#	"NAV W 1k":		1414,

for known_point in known_points:
	name = known_point["name"]
	if name in distances:
		continue

	try:
		dist_to_pt = int(input("Distance to %s: " % (name)).strip())
	except ValueError:
		continue

	distances[name] = dist_to_pt
	if len(distances) == 3:
		break

if len(distances) < 2:
	print("Need at least two distances to calculate.")
else:
	circles = { name: geo.Circle(points_by_name[name]["2d"], distances[name]) for (name, radius) in distances.items() }
	(intersection, remaining) = geo.Circle.find_circle_intersection(circles.values())

	(i1, i2) = intersection
	if len(remaining) == 0:
		print("Coordinates are one of (distance between options %.0f):" % (i1.dist(i2)))
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
		print("Coordinates are: %.0f / %.0f (distance from prediction %.0f)" % (i.x, i.y, c3.dist(i)))
