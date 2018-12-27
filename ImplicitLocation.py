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

import geo

class ImplicitLocation(object):
	def __init__(self, depth = None, distances = None, bearings = None):
		self._depth = depth
		self._distances = distances
		if self._distances is None:
			self._distances = { }
		self._bearings = bearings
		if self._bearings is None:
			self._bearings = { }

	@property
	def depth(self):
		return self._depth

	@property
	def distances(self):
		return self._distances

	@property
	def bearings(self):
		return self._bearings

	def _estimate_coordinates(self, buoys, hypothesis):
		point_cloud = [ ]
		for (name, distance) in self._distances.items():
			buoy = buoys[name]
			sphere = geo.Sphere(midpt = buoy["pos"], radius = distance)
			nearest_point = sphere.nearest_point(hypothesis)
			point_cloud.append(nearest_point)

		# Average the points, i.e., take the gravity center
		sum_pt = geo.Vector3D(0, 0, 0)
		for point in point_cloud:
			sum_pt += point
		estimate = sum_pt / len(point_cloud)

		# Then calculate sum-of-squares error
		error = 0
		for point in point_cloud:
			error += point.dist(estimate) ** 2
		return (estimate, error)

	def _improve_hypothesis(self, buoys, hypothesis, movement_vector):
		(estimate, error) = self._estimate_coordinates(buoys, hypothesis)
		did_halve = False
		while movement_vector.length > 0.1:
			guess = hypothesis + movement_vector
			(new_estimate, new_error) = self._estimate_coordinates(buoys, guess)
			if new_error < error:
				# Improvement!
				did_halve = False
				(estimate, error, hypothesis) = (new_estimate, new_error, guess)
				continue
			else:
				# We made it worse. What happened?
				if not did_halve:
					# We went in the right direction before, but then suddenly
					# improvement stopped. Halve the vector
					movement_vector *= 0.5
					did_halve = True
				else:
					# We either halves and it didn't improve, reverse direction
					movement_vector *= -0.5
					did_halve = False
		return (estimate, error)

	def calculate_coordinates(self, buoys):
		if self.depth is not None:
			hypothesis = geo.Vector3D(0, 0, self.depth)
			steps = [ geo.Vector3D(1000, 0, 0), geo.Vector3D(0, 1000, 0) ]
		else:
			hypothesis = geo.Vector3D(0, 0, 0)
			steps = [ geo.Vector3D(1000, 0, 0), geo.Vector3D(0, 1000, 0), geo.Vector3D(0, 0, 500) ]

		while True:
			prev_hypothesis = hypothesis
			stepping_error = None
			for step in steps:
				(hypothesis, error) = self._improve_hypothesis(buoys, hypothesis, geo.Vector3D(1000, 0, 0))
				if (stepping_error is None) or (error > stepping_error):
					stepping_error = error
				if self.depth is not None:
					hypothesis = geo.Vector3D(hypothesis.x, hypothesis.y, self.depth)

			if (prev_hypothesis.dist(hypothesis)) < 1:
				break

		return (hypothesis, stepping_error)

	@classmethod
	def _input_value(cls, prompt):
		while True:
			value = input(prompt).strip()
			if value == "":
				return None
			try:
				value = int(value)
			except ValueError:
				print("Invalid value: '%s'" % (value))
				continue
			return value

	@classmethod
	def _input_buoy(cls, buoy):
		distance = cls._input_value("Distance to %s: " % (buoy["name"]))
		bearing = None
		return (distance, bearing)

	@classmethod
	def input_keyboard(cls, buoys):
		depth = cls._input_value("Depth: ")
		distances = { }
		bearings = { }
		for buoy in buoys.values():
			(distance, bearing) = cls._input_buoy(buoy)
			if distance is not None:
				distances[buoy["name"]] = distance
			if bearing is not None:
				bearings[buoy["name"]] = bearing
		return cls(depth = depth, distances = distances, bearings = bearings)

	def to_dict(self):
		return {
			"depth":		self._depth,
			"distances":	self._distances,
			"bearings":		self._bearings,
		}

	@classmethod
	def from_dict(cls, data_dict):
		return cls(depth = data_dict.get("depth"), distances = data_dict.get("distances"), bearings = data_dict.get("bearings"))

	def __str__(self):
		items = [ ]
		if self._depth is not None:
			items.append("Depth = %d" % (self._depth))
		items += [ "Dst(%s) = %d" % (key, value) for (key, value) in sorted(self._distances.items()) ]
		items += [ "Brg(%s) = %d" % (key, value) for (key, value) in sorted(self._bearings.items()) ]
		return "Loc<%s>" % (", ".join(items))
