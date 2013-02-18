''' 
Informations Retrieval Library
==============================
SuperList is an alternatice to Python's default lists (arrays) 
'''

# Author: Tarek Amr <@gr33ndata> 

class SuperList(list):
    ''' SuperList: An alternatice to Python's default lists (arrays)
        So that we can add some helper methods and functionalities.
    '''
    
    def align_to_list(self, b):
        ''' Make sure self and be are equal in length
        '''
        if len(self) < len(b):
            self.expand(len(b))
        elif len(b) < len(self):
            b.expand(len(self))

    def add(self, b):
        if type(b) == int:
            self.add_number(b)
        else:
            self.add_list(b)
            
    def add_list(self, b):
        ''' Add lists, item to item
        '''
        self.align_to_list(b)
        for i in range(len(self)):
            self[i] += b[i]
    
    def add_number(self, b):
        for i in range(len(self)):
            self[i] += b
    
    def div(self, b):
        if type(b) == int:
            self.div_number(b)
        else:
            self.div_list(b)
                    
    def div_list(self, b):
        self.align_to_list(b)
        for i in range(len(self)):
            self[i] = float(self[i]) / b[i]
            
    def div_number(self, b):
        for i in range(len(self)):
            self[i] = float(self[i]) / b
                    
    def nonzero_count(self):
        ''' Returns number of non-zero items in list
        '''
        return sum([1 for item in self if item > 0])

    def unique_append(self, item):
        ''' Only append item to list if not already there, 
            In case we want our list to act like a set.
            Returns the index of the the added item'''
        if item in self:
            return self.index(item)
        else:
            self.append(item)
            return len(self) - 1

    def _expand(self, new_len=0, padding_data=float(0)):
        ''' /!\ This is an old piece of code,
            We replaced it with more optimized one.
            Underscored and left for testing purpose for now.
            Expand a list size to new_len, 
            then fill new cells with padding_data. 
            The defaul padding_data is float(0).
        '''
        for i in range(len(self),new_len):
            self.append(padding_data)
    
    def expand(self, new_len=0, padding_data=float(0)):
        ''' Expand a list size to new_len, 
            then fill new cells with padding_data. 
            The defaul padding_data is float(0).
        '''
        new_tail = [padding_data] * (new_len - len(self))
        self += new_tail

    def insert_after_padding(self, index, item, padding_data=float(0)):
		''' Add item in specific index location, and expand if needed. 
            Notice that the original insert method for lists, 
            just adds items to end of list if index is bigger than length.
            Also, unlike the original list insert method,
            if there is existing item at index, it is overwritten.  
		'''
		self.expand(new_len=index+1, padding_data=padding_data)
		self[index] = float(item)

    def increment_after_padding(self, index, item, padding_data=float(0)):
		''' Just like insert_after_padding().  
            However, existing items at index are incremented.  
		'''
		self.expand(new_len=index+1, padding_data=padding_data)
		#print 'increment_after_padding:', index, len(self)
		self[index] = self[index] + item

    # We need to implement this
    # def populate_in_order(self, item, less_than):
    
    def populate_in_reverse_order(self, item, greater_than):
        ''' Add items to list, but in order
            Here we make sure bigger items are put at the beginning of list,
            greater_than is the function used to compare items
        '''
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


if __name__ == '__main__':
    
    pass
