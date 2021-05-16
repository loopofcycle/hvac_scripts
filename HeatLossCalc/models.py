# -*- coding: utf-8 -*-
from pprint import pprint
from Autodesk.Revit.DB import SpatialElementBoundaryOptions


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
		self.__set_endpoints()
		
	def __set_endpoints(self):
		opt = SpatialElementBoundaryOptions()
		segments = self.entity.GetBoundarySegments(opt)
		if len(segments):
			self.lines = [segment.GetCurve() for segment in segments[0]]
			self.all_points = []
			for line in self.lines:
				self.all_points.append(line.GetEndPoint(0))
				self.all_points.append(line.GetEndPoint(1))
			self.set_endpoints(self.all_points)

class modelSegment():
	def __init__(self, axis, limit, lines):
		pass


class modelBoundry():
	def __init__(self, start=0, end=10, step=1, lines=[], axis='X', limit='max'):
		self.axis = axis
		self.limit = limit
		self.step = step
		self.start = start
		self.end = end
		
		self.data = self.__create_lines_data(lines)
		self.segments = self.__build_segments()

	def __create_lines_data(self, lines):
		leveled_lines = {}
		for line in lines:
			if leveled_lines.get(line.Origin.Z):
				leveled_lines[line.Origin.Z].append(line)
			else:
				leveled_lines[line.Origin.Z] = [line]
		return leveled_lines

	def __build_segments(self):
		segments = {}
		for level, lines in self.data.items():
			segment = modelSegment(self.axis, self.limit, lines)
			segments.update({level: segment})

		return segments


class modelPerimeter(GeometryEntity):
	def __init__(self, rooms):
		self.rooms = []
		for room in rooms:
			self.__add_to_rooms(room)

		self.all_points = []
		for room in self.rooms:
			if room.all_points:
				self.all_points.extend(room.all_points)

		self.all_lines = []
		for room in self.rooms:
			if room.lines:
				self.all_lines.extend(room.lines)

		self.set_endpoints(self.all_points)
		self.max_distance = self.end_points[0].DistanceTo(self.end_points[1])
		self.__set_boundaries()

	def __add_to_rooms(self, seq):
		for element in seq:
			if isinstance(element, list):
				self.__add_to_rooms(element)
			if element.end_points:
				self.rooms.append(element)

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
													lines=self.all_lines,
													axis=parameters['axis'],
													limit=parameters['limit'],
													)
