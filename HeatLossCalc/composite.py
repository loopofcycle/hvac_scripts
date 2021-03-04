class Component():
	def __init__(self, name):
		self.name = name
		self.parent = None
		self.childs = None
	
	def get_composite(self):
		return self.childs

	def set_properties(self, props={}):
		self.props = props
	
	def calc(self):
		print('calculating' + self.name)


class Composite(Component):
	def __init__(self, name):
		super(Component, self).__init__(name)
		self.childs = []
	
	def add(self, child):
		child.parent = self
		self.childs.append(child)
	
	def calc(self):
		super(Component, self).calc()
		for child in self.childs:
			child.calc()

