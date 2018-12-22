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

import collections

class AngleTools():
	_CompassPoint = collections.namedtuple("CompassPoint", [ "bearing", "coarse_bearing", "compass", "adjust" ])
	_KNOWN_BEARINGS = {
		0:		"N",
		45:		"NE",
		90:		"E",
		135:	"SE",
		180:	"S",
		225:	"SW",
		270:	"W",
		315:	"NW",
		360:	"N",
	}

	@classmethod
	def bearing_to_compass(cls, bearing):
		best_error = None
		best_direction = None
		for (degrees, direction) in cls._KNOWN_BEARINGS.items():
			error = abs(degrees - bearing)
			if (best_error is None) or (error < best_error):
				best_error = error
				best_direction = (degrees, direction)

		return cls._CompassPoint(bearing = bearing, coarse_bearing = best_direction[0], compass = best_direction[1], adjust = bearing - best_direction[0])
