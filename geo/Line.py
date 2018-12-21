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

class Line():
	def __init__(self, base, ray):
		self._base = base
		self._ray = ray

	@classmethod
	def through(cls, pt1, pt2):
		return cls(pt1, pt2 - pt1)

	@property
	def base(self):
		return self._base

	@property
	def ray(self):
		return self._ray

	def __call__(self, mu):
		return self._base + (mu * self._ray)

class LineSegment():
	def __init__(self, start, end):
		self._line = Line(base = start, ray = end - start)
		self._end = end

	@property
	def start(self):
		return self._line.base

	@property
	def end(self):
		return self._end

	@property
	def length(self):
		return self.start.dist(self.end)

	@property
	def midpt(self):
		return self.line(0.5)

	@property
	def line(self):
		return self._line

	def __repr__(self):
		return "LineSegment<%s to %s>" % (self.start, self.end)
