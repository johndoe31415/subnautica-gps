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

from .Vector import Vector2D
from .Line import LineSegment

class NoInterceptException(Exception): pass

class Circle(object):
	def __init__(self, midpt, radius):
		assert(radius > 0)
		self._midpt = midpt
		self._radius = radius

	@property
	def midpt(self):
		return self._midpt

	@property
	def r(self):
		return self._radius

	def intersect_circle(self, other):
		D = self.midpt.dist(other.midpt)
		if (self.r + other.r) <= D:
			raise NoInterceptException("Circles do not intersect")

		if D <= abs(self.r - other.r):
			raise NoInterceptException("Circles do not intersect")

		(a, b) = tuple(self.midpt)
		(c, d) = tuple(other.midpt)
		nabla = 1 / 4 * math.sqrt((D + self.r + other.r) * (D + self.r - other.r) * (D - self.r + other.r) * (-D + self.r + other.r))
		x1 = ((a + c) / 2) + (((c - a) * (self.r ** 2 - other.r ** 2)) / (2 * D ** 2)) + (2 * nabla * (b - d) / (D ** 2))
		x2 = ((a + c) / 2) + (((c - a) * (self.r ** 2 - other.r ** 2)) / (2 * D ** 2)) - (2 * nabla * (b - d) / (D ** 2))

		y1 = ((b + d) / 2) + (((d - b) * (self.r ** 2 - other.r ** 2)) / (2 * D ** 2)) - (2 * nabla * (a - c) / (D ** 2))
		y2 = ((b + d) / 2) + (((d - b) * (self.r ** 2 - other.r ** 2)) / (2 * D ** 2)) + (2 * nabla * (a - c) / (D ** 2))
		return (Vector2D(x1, y1), Vector2D(x2, y2))

	@classmethod
	def find_circle_intersection(cls, circles):
		circles = tuple(circles)
		for (i1, i2) in itertools.combinations(range(len(circles)), 2):
			c1 = circles[i1]
			c2 = circles[i2]
			try:
				intersect = c1.intersect_circle(c2)
				return (intersect, [ c for (i, c) in enumerate(circles) if i not in [ i1, i2 ] ])
			except NoInterceptException:
				continue
		raise NoInterceptException("None of the given circles could be made to intercept.")

	def dist(self, point):
		segment = LineSegment(self.midpt, point)
		return abs(segment.length - self.r)

	def __repr__(self):
		return "Circle(M = %s, r = %.2f)" % (self.midpt, self.r)
