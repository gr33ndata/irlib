# Currently being used by classifier
# Should be replaced with superlist.py soon

class SuperList(list):
	''' 
	SuperList: An alternatice to Python's default lists (arrays)
	'''

	def unique_append(self, item):
		''' Only append item to list if not already there '''
		if not self.__contains__(item):
			self.append(item)

	def do_padding(self, new_len=0, padding_data=float(0)):
		''' Extend a list size to new_len, then fill new cells with padding_data '''
		for i in range(len(self),new_len):
			self.append(padding_data)

	def insert_after_padding(self, index=0, frequency=True):
		''' It's given an index in the list, if list is not big enough it is extended and padded with zeros
			If frequency=False: The indexed cell is set to one if it's zero. Otherwise left as it is.
			If frequency=True: Each time it is called, the number in the indexed cell is increased by one
		'''
		self.do_padding(new_len=index+1, padding_data=0)
		self[index] = self[index]+1 if frequency else 1  
	
	# item: new item to be added to list in its right order
	# less_than: function used to compare items		
	def populate_in_reverse_order(self, item, greater_than):
		if self == []:
			self.append(item)
		elif greater_than(item,self[0]):
			self.insert(0,item)
		else:
			for j in range(0,len(self)):
				if greater_than(item,self[j]):
					self.insert(j,item)
					break
			else:
				self.append(item)
