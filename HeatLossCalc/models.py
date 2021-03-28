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


class BoundrySegment():
	def __init__(self, line, start_point, coord='X', limit='max'):
		self.coord = coord
		self.limit = limit
		self.data = {line: start_point}
		self.start_point = start_point
		self.end_point = start_point
		self.max_length = 15
		self.aproximation = 2
		self.sub_segment = None

	def calc_length(self):
		length = self.start_point.DistanceTo(self.end_point)
		if self.sub_segment is not None:
			length += self.sub_segment.calc_length()
		return length
	
	def add_point(self, line, point):
		if self.coord == 'X':
			point_segm_coord, point_ort_coord = point.X, point.Y
			end_segm_coord, end_ort_coord = self.end_point.X, self.end_point.Y
		if self.coord == 'Y':
			point_segm_coord, point_ort_coord = point.Y, point.X
			end_segm_coord, end_ort_coord = self.end_point.Y, self.end_point.X

		if self.limit == 'max':
			higher_than_end = point_ort_coord > end_ort_coord
		if self.limit == 'min':
			higher_than_end = point_ort_coord < end_ort_coord

		ort_difference = abs(point_ort_coord - end_ort_coord)
		distance_to_endpoint = abs(point_segm_coord - end_segm_coord)

		if higher_than_end:
			#print(self.coord, self.limit, 'adding point: ', point.ToString(), 'after: ', self.end_point.ToString())
			self.sub_segment = None
			self.data[line] = point
			self.end_point = point

		#if not higher_than_end and self.sub_segment is None:
		#	print(self.coord, self.limit, 'creating subsegment at:', point.ToString())
		#	self.sub_segment = BoundrySegment(line, point, self.coord, self.limit)

		#if not higher_than_end and self.sub_segment.calc_length() < self.max_length:
		#	print(self.coord, self.limit, 'adding to subsegment at:', point.ToString())
		#	print('subsegment length', self.sub_segment.calc_length())
		#	self.sub_segment.add_point(line, point)
		
		#if not higher_than_end and self.sub_segment.calc_length() > self.max_length:
		#	print(self.coord, self.limit, 'updated with subsegment at:', point.ToString())
		#	print('subsegment length', self.sub_segment.calc_length())
		#	self.data.update(self.sub_segment.data)
		#	self.sub_segment = None
		#	self.data[line] = point
		#	self.end_point = point

		if ort_difference < self.aproximation and distance_to_endpoint < self.max_length:
			#print(self.coord, self.limit, 'adding point: ', point.ToString(), 'after: ', self.end_point.ToString(), 'ort_dif: ', ort_difference)
			self.sub_segment = None
			self.data[line] = point
			self.end_point = point


class modelBoundry():
	def __init__(self, start=0, end=10, step=1, points=[], axis='X', limit='max'):
		self.axis = axis
		self.limit = limit
		self.step = step
		self.start = start
		self.end = end
		
		self.data = {}
		self.__create_points_data(points)
		
		self.segments = {}
		self.__build_segments()		

	def add_point(self, data, line, point):
		if not data.get(line):
			data[line] = point

		else:
			if self.axis == 'X':
				point_segm_coord = point.X
				point_ort_coord = point.Y
				data_point_ort_coord = data[line].Y
			
			if self.axis == 'Y':
				point_segm_coord = point.Y
				point_ort_coord = point.X
				data_point_ort_coord = data[line].X
			
			if self.limit == 'max':
				local_extreme = point_ort_coord > data_point_ort_coord

			if self.limit == 'min':
				local_extreme = point_ort_coord < data_point_ort_coord

			if line < point_segm_coord < (line + self.step):
				if local_extreme:
					data[line] = point
		
	def __get_leveled_points(self, points):
		leveled_points = {}
		for point in points:
			if leveled_points.get(str(point.Z)):
				leveled_points[str(point.Z)].append(point)
			else:
				leveled_points[str(point.Z)] = [point]
		return leveled_points

	def __clean_data(self, data):
		clean_data = {}
		for line, point in data.items():
			if point not in clean_data.values():
				clean_data[line] = point
		
		return clean_data

	def __create_points_data(self, points):
		leveled_points = self.__get_leveled_points(points)
		for level, points in leveled_points.items():
			self.data[level] = {}
			for line in range(self.start, self.end + 2, self.step):
				for point in points:
					self.add_point(self.data[level], line, point)
			self.__clean_data(self.data[level])

	def __build_segments(self):
		for level, data in self.data.items():
			if self.limit == 'min':
				line = sorted(data.keys())[0]
				point = data[line]
				segment = BoundrySegment(line, point, coord=self.axis, limit=self.limit)
				for line in sorted(data.keys()):
					point = data[line]
					segment.add_point(line, point)

			if self.limit == 'max':
				line = sorted(data.keys())[-1]
				point = data[line]
				segment = BoundrySegment(line, point, coord=self.axis, limit=self.limit)
				for line in reversed(sorted(data.keys())):
					point = data[line]
					segment.add_point(line, point)
			
			self.segments.update({level: segment})


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
													points=self.all_points,
													axis=parameters['axis'],
													limit=parameters['limit'],
													)
