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

import sys
from MultiCommand import MultiCommand
from CommandTrilaterate import CommandTrilaterate
from CommandGoto import CommandGoto
from CommandRecalculate import CommandRecalculate
from CommandPlot import CommandPlot

mc = MultiCommand()

def genparser(parser):
	parser.add_argument("--buoys-file", metavar = "filename", type = str, default = "known.json", help = "Specifies the file of the known buoy location. Defaults to %(default)s.")
	parser.add_argument("--verbose", action = "store_true", help = "Increase verbosity.")
mc.register("whereami", "Determine current observer position by trilateration", genparser, action = CommandTrilaterate, aliases = [ "trilaterate" ])

def genparser(parser):
	parser.add_argument("--buoys-file", metavar = "filename", type = str, default = "known.json", help = "Specifies the file of the known buoy location. Defaults to %(default)s.")
	parser.add_argument("--verbose", action = "store_true", help = "Increase verbosity.")
mc.register("goto", "Get the bearing from a given target", genparser, action = CommandGoto)

def genparser(parser):
	parser.add_argument("--buoys-file", metavar = "filename", type = str, default = "known.json", help = "Specifies the file of the known buoy location. Defaults to %(default)s.")
	parser.add_argument("--verbose", action = "store_true", help = "Increase verbosity.")
mc.register("recalculate", "Update all locations from the sources by recalculating", genparser, action = CommandRecalculate)

def genparser(parser):
	parser.add_argument("-o", "--output", metavar = "filename", type = str, default = "map.png", help = "When plotting to a PNG file, specifies the filename. Defaults to %(default)s.")
	parser.add_argument("--gpl", action = "store_true", help = "Instead of plotting, print the gnuPlot source to stdout.")
	parser.add_argument("--buoys-file", metavar = "filename", type = str, default = "known.json", help = "Specifies the file of the known buoy location. Defaults to %(default)s.")
	parser.add_argument("--verbose", action = "store_true", help = "Increase verbosity.")
mc.register("plot", "Plot all locations", genparser, action = CommandPlot)

mc.run(sys.argv[1:])
