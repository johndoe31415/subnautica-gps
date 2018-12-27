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

import math
import itertools

from .Vector import Vector3D
from .Line import LineSegment

class NoInterceptException(Exception): pass

class Sphere(object):
	def __init__(self, midpt, radius):
		assert(radius > 0)
		assert(midpt.dim == 3)
		self._midpt = midpt
		self._radius = radius

	@property
	def midpt(self):
		return self._midpt

	@property
	def r(self):
		return self._radius

	def nearest_point(self, point):
		segment = LineSegment(self.midpt, point)
		if segment.length == 0:
			# Choose any point
			nearest_point = self._midpt + (self._radius * Vector3D(1, 0, 0))
		else:
			tau = self.r / segment.length
			nearest_point = segment.line(tau)
		return nearest_point

	def __repr__(self):
		return "Sphere(M = %s, r = %.2f)" % (self.midpt, self.r)
