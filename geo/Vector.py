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

class Vector(object):
	def __init__(self, components):
		self._components = components

	@property
	def x(self):
		return self._components[0]

	@property
	def y(self):
		return self._components[1]

	@property
	def z(self):
		return self._components[2]

	@property
	def length(self):
		return math.sqrt(sum((x ** 2) for x in self._components))

	@property
	def norm(self):
		return self / self.length

	@property
	def dim(self):
		return len(self._components)

	def dist(self, vec):
		return (self - vec).length

	def __eq__(self, other):
		epsilon = 1e-6
		return (self.dim == other.dim) and all(abs(c1 - c2) < epsilon for (c1, c2) in zip(self, other))

	def __neq__(self, other):
		return not (self == other)

	def __neg__(self):
		return self.__class__(*(-c for c in self._components))

	def __add__(self, vec):
		assert(self.dim == vec.dim)
		return self.__class__(*(c1 + c2 for (c1, c2) in zip(self, vec)))

	def __sub__(self, vec):
		return self + (-vec)

	def __mul__(self, scalar):
		return self.__class__(*(c * scalar for c in self._components))

	def __rmul__(self, scalar):
		return self * scalar

	def __truediv__(self, quotient):
		return self * (1 / quotient)

	def __iter__(self):
		return iter(self._components)

	def __repr__(self):
		return "<%s>" % (", ".join("%.2f" % (x) for x in self._components))

class Vector2D(Vector):
	def __init__(self, x, y):
		Vector.__init__(self, (x, y))

	@property
	def z(self):
		raise NotImplementedError("A 2D vector has no Z component.")

	@property
	def angle(self):
		return math.atan2(self.y, self.x)

	@property
	def bearing(self):
		angle_rad = self.angle
		angle_deg = 180 * angle_rad / math.pi
		bearing = (-angle_deg + 90) % 360
		return bearing

class Vector3D(Vector):
	def __init__(self, x, y, z):
		Vector.__init__(self, (x, y, z))
