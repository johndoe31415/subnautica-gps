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

import subprocess
from BaseCommand import BaseCommand

class CommandPlot(BaseCommand):
	def __init__(self, cmdname, args):
		BaseCommand.__init__(self, cmdname, args)

		gpl = [ ]
		gpl += [ "set terminal pngcairo size 900,900" ]
		gpl += [ "set output '%s'" % (self._args.output) ]

		mapsize = 1500
		gpl += [ "set xrange [ %d : %d ]" % (-mapsize, mapsize) ]
		gpl += [ "set yrange [ %d : %d ]" % (-mapsize, mapsize) ]
		gpl += [ "set grid" ]
		gpl += [ "set size square" ]
		gpl += [ "set style line 1 linecolor rgb '#27ae60' pointtype 2" ]
		gpl += [ "set style line 2 linecolor rgb '#2980b9' pointtype 5" ]

		plots = [ ]
		plots += [ "'-' with points linestyle 1 title 'Buoys'" ]
		plots += [ "'-' with labels offset char 0,-0.7 notitle" ]
		plots += [ "'-' with points linestyle 2 title 'Location'" ]
		gpl += [ "plot %s" % (", ".join(plots)) ]

		# Buoys
		for (name, buoy) in self._buoys.items():
			gpl += [ "%.0f %.0f" % (buoy["pos"].x, buoy["pos"].y) ]
		gpl += [ "e", "" ]

		# Location Names
		for (name, location) in self._locations.items():
			(coords, error) = location.calculate_coordinates(self._buoys)
			gpl += [ "%.0f %.0f \"%s\"" % (coords.x, coords.y, name) ]
		gpl += [ "e", "" ]

		# Locations
		for (name, location) in self._locations.items():
			(coords, error) = location.calculate_coordinates(self._buoys)
			gpl += [ "%.0f %.0f" % (coords.x, coords.y) ]
		gpl += [ "e", "" ]

		gpl = "\n".join(gpl) + "\n"
		if self._args.gpl:
			print(gpl)
		else:
			subprocess.check_output([ "gnuplot" ], input = gpl.encode())
