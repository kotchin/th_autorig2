"""

jointchain <--- bind chain
	rig
		subrig
			jointchain
			jointchain
			jointchain
		subrig	
			jointchain

"""

class TreeNode( object ) :
	def __init__( self, _parent=None, _value=None ) :
		self.__value = _value
		if not self.__value : self.__value = self		
		self.__parent = _parent
		self.__children = []

<<<<<<< HEAD
	def add_child( self, _value ) :
		# child = TreeNode( self, _value )
		self.children.append( _value )
=======
	def add_child( self, _value ) :		
		child = _value
		print _value
		# print '---',_value, _value.__class__ issubclass( , _value.__class__ )
		# print isinstance( _value, TreeNode )
		# if( not type( child ) == TreeNode ) :
		# child = TreeNode( self, _value )
		child.__parent = self
		self.__children.append( child )
>>>>>>> b853c271a25aac101c4204b31011cae731333c0b

	def tree_parent( self ) :
		return self.__parent

	def tree_children( self ) :
		return self.__children

	def tree_siblings( self ) :
		return self.parent().children()
