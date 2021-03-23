# -*- coding: utf-8 -*-
from pprint import pprint
from Autodesk.Revit.DB import SpatialElementBoundaryOptions

class modelBoundry():
	def __init__(self, start=0, end=1, step=0.05, points=[], axis='X', limit='max'):
		self.data = {}
		for line in range(start, end + 2, step):
			for point in points:
				self.add_point(line, point, axis=axis, limit=limit, step=step)
		self.clear_off_data()

	def add_point(self, line, point, axis, limit, step):
		if not self.data.get(line):
			self.data[line] = point
		
		if axis == 'X' and limit == 'max':
			if line < point.X < (line + step):
				if point.Y > self.data[line].Y:
					self.data[line] = point
		
		if axis == 'X' and limit == 'min':
			if line < point.X < (line + step):
				if point.Y < self.data[line].Y:
					self.data[line] = point

		if axis == 'Y' and limit == 'max':
			if line < point.Y < (line + step):
				if point.X > self.data[line].X:
					self.data[line] = point

		if axis == 'Y' and limit == 'min':
			if line < point.Y < (line + step):
				if point.X < self.data[line].X:
					self.data[line] = point

	def clear_off_data(self):
		pass

	def show(self):
		pprint(self.data)

class GeometryEntity():
	def set_endpoints(self, all_points):
		self.end_points = [all_points[0]]
		for point in all_points:
			if point.Z != 0: continue
			base_point = self.end_points[0]	
			if (point.X + point.Y)**2 < (base_point.X + base_point.Y)**2:
				self.end_points.remove(base_point)
				self.end_points.append(point)

		self.end_points.append(all_points[0])
		for point in all_points:
			base_point = self.end_points[0]
			farthest_point = self.end_points[1]
			if point.Z != base_point.Z: continue
			if base_point.DistanceTo(point) > base_point.DistanceTo(farthest_point):
				self.end_points.remove(farthest_point)
				self.end_points.append(point)
		
class modelRoom(GeometryEntity):
	def __init__(self, room):
		self.entity = room
		self.name = room.GetParameters('Имя')[0].AsString()
		#self.area = room.GetParameters('Площадь')[0].AsString()
		#self.volume = room.GetParameters('Объем')[0].AsString()
		#self.number = room.GetParameters('Номер')[0].AsString()
		self.end_points = []
		self._set_endpoints()
		
	def _set_endpoints(self):
		opt = SpatialElementBoundaryOptions()
		segments = self.entity.GetBoundarySegments(opt)
		if len(segments):
			self.lines = [segment.GetCurve() for segment in segments[0]]
			self.all_points = []
			for line in self.lines:
				self.all_points.append(line.GetEndPoint(0))
				self.all_points.append(line.GetEndPoint(1))
			self.set_endpoints(self.all_points)

class modelPerimeter(GeometryEntity):
	def __init__(self, rooms):
		self.rooms = []
		for seq in rooms:
			self.__add_to_rooms(seq)

		self.all_points = []
		for room in self.rooms:
			if room.all_points:
				self.all_points.extend(room.all_points)

		self.set_endpoints(self.all_points)
		self.max_distance = self.end_points[0].DistanceTo(self.end_points[1])
		self.__set_boundaries()


	def __add_to_rooms(self, seq):
		for element in seq:
			if isinstance(element, list):
				self.__add_to_rooms(element)
			if element.end_points:
				self.rooms.append(element)
	
	def __set_boundaries_from_EP(self):
		self.boundary_offset = 2
		self.boundaries = {'left': [self.end_points[0]],
							'up': [self.end_points[1]],
							'right': [self.end_points[1]],
							'down': [self.end_points[0]]
							}
		for direction in self.boundaries:
			points = self.boundaries[direction]
			next_point = 'exist'
			while next_point is not None:
				next_point = self.__find_closest(point=points[-1],
												direction=direction)
				points.append(next_point)

		pprint(self.boundaries)

	def __find_closest(self, point, direction):
		
		min_distance = self.max_distance
		closest_point = None		
		remaining_points = list(set(self.all_points) - set(self.boundaries[direction]))

		if direction == 'left' or direction == 'right':
			for lookup_point in remaining_points:
				if point.Z != lookup_point.Z: continue
				this_distance = abs(point.Y - lookup_point.Y)
				direction_offset = abs(point.X - lookup_point.X)
				if this_distance < min_distance and direction_offset < self.boundary_offset:
					min_distance = this_distance
					closest_point = lookup_point

		if direction == 'up' or direction == 'down':
			for lookup_point in remaining_points:
				if point.Z != lookup_point.Z: continue
				this_distance = abs(point.X - lookup_point.X)
				direction_offset = abs(point.Y - lookup_point.Y)
				if this_distance < min_distance and direction_offset < self.boundary_offset:
					min_distance = this_distance
					closest_point = lookup_point

		return closest_point

	def __set_boundaries(self):
		orientations = { 'left' : { 'axis': 'Y', 'limit': 'min'},
						'up' : { 'axis': 'X', 'limit': 'max'}, 
						'right' : { 'axis': 'Y', 'limit': 'max'}, 
						'down' : { 'axis': 'X', 'limit': 'min'},
						}
		self.boundaries = {}
		for orient, parameters in orientations.items():
			self.boundaries[orient] = modelBoundry( start=int(self.end_points[0].X),
													end=int(self.end_points[1].X),
													step=1,
													points=self.all_points,
													axis=parameters['axis'],
													limit=parameters['limit'],
													)
		for name, b in self.boundaries.items():
			print(name)
			b.show()