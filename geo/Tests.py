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
import unittest

from .Vector import Vector2D, Vector3D
from .Line import LineSegment
from .Circle import Circle

class GeoTests(unittest.TestCase):
	def test_vec2d(self):
		v = Vector2D(0, 0)
		self.assertAlmostEqual(v.length, 0)
		self.assertAlmostEqual(v.x, 0)
		self.assertAlmostEqual(v.y, 0)

		v = Vector2D(0, 1)
		self.assertAlmostEqual(v.length, 1)
		self.assertAlmostEqual(v.x, 0)
		self.assertAlmostEqual(v.y, 1)

		v = Vector2D(1, 0)
		self.assertAlmostEqual(v.length, 1)
		self.assertAlmostEqual(v.x, 1)
		self.assertAlmostEqual(v.y, 0)

		v = Vector2D(1, 1)
		self.assertAlmostEqual(v.length, math.sqrt(2))
		self.assertAlmostEqual(v.x, 1)
		self.assertAlmostEqual(v.y, 1)

		self.assertTrue(Vector2D(0, 0) == Vector2D(0, 0))
		self.assertFalse(Vector2D(0, 0) != Vector2D(0, 0))
		self.assertFalse(Vector2D(0, 0) == Vector2D(1, 2))
		self.assertTrue(Vector2D(0, 0) != Vector2D(1, 2))

		v = Vector2D(1, 1).norm
		self.assertAlmostEqual(v.x, math.sin(math.pi / 4))
		self.assertAlmostEqual(v.y, math.sin(math.pi / 4))

		v = Vector2D(10, 10) + Vector2D(15, 30)
		self.assertAlmostEqual(v.x, 10 + 15)
		self.assertAlmostEqual(v.y, 10 + 30)

		v = -Vector2D(1, 2)
		self.assertAlmostEqual(v.x, -1)
		self.assertAlmostEqual(v.y, -2)

		v = Vector2D(10, 10) - Vector2D(15, 30)
		self.assertAlmostEqual(v.x, 10 - 15)
		self.assertAlmostEqual(v.y, 10 - 30)

		d = Vector2D(10, 10).dist(Vector2D(15, 30))
		self.assertAlmostEqual(d, math.sqrt(25 + 400))

	def test_linesegment(self):
		x = LineSegment(Vector2D(1, 2), Vector2D(3, 1))
		self.assertEqual(x.start, Vector2D(1, 2))
		self.assertEqual(x.end, Vector2D(3, 1))
		self.assertEqual(x.line(0), x.start)
		self.assertEqual(x.line(1), x.end)

	def test_circle(self):
		c1 = Circle(Vector2D(1, 2), 3)
		c2 = Circle(Vector2D(3, -1), 4)
		(p1, p2) = c1.intersect_circle(c2)
		self.assertAlmostEqual(p1.x, 3.859762656633831)
		self.assertAlmostEqual(p1.y, 2.906508437755887)
		self.assertAlmostEqual(p2.x, -0.9366857335569081)
		self.assertAlmostEqual(p2.y, -0.29112382237127155)

		c = Circle(Vector2D(0, 0), 3)
		self.assertAlmostEqual(c.dist(Vector2D(3, 4)), 2)
		self.assertAlmostEqual(c.dist(Vector2D(0, 0)), 3)
		self.assertAlmostEqual(c.dist(Vector2D(1, 0)), 2)

		c1 = Circle(Vector2D(-8.88, -0.7), 1.2345)
		c2 = Circle(Vector2D(-8.02, -0.46), 0.9876)
		(p1, p2) = c1.intersect_circle(c2)
		self.assertAlmostEqual(p1.x, -8.4169, places = 4)
		self.assertAlmostEqual(p1.y, 0.4443, places = 4)
		self.assertAlmostEqual(p2.x, -7.8913, places = 4)
		self.assertAlmostEqual(p2.y, -1.4392, places = 4)
