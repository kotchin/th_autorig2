import pymel.all as pm

from tree import TreeNode

import utils
import settings

relatedjointattr = 'th_related_joint'

class BaseControl( pm.Transform, TreeNode, object ) :
	PARTNAME = 'baseControl'

	__shapedict = {
		# 'default' : 'mc.spaceLocator()'
		'default' : 'pm.spaceLocator()'
	}


	@classmethod
	def convert_to_virtual( cls, _transform ) :
		if( type( _transform ) == pm.Transform ) :
			return utils.add_set_attr( _transform, settings.attrname, cls.PARTNAME, _keyable=False, _locked=True )
		else :		
			utils.err( '%s is not a transform' % ( _transform.name() ) )	
			return False

	@classmethod
	def _isVirtual( cls, obj, name ) :
		fn = pm.api.MFnDependencyNode( obj )
		try :
			if( fn.hasAttribute( settings.attrname ) ) :
				plug = fn.findPlug( settings.attrname )
				return plug.asString() == cls.PARTNAME
		except :
			pass
		return False

	@classmethod
	def _preCreateVirtual( cls, shape_type='default', **kwargs ) :
		if 'n' in kwargs :
			name = kwargs.pop( 'n' )
		elif 'name' in kwargs :
			name = kwargs.get( 'name' )
		else :
			name = cls.PARTNAME
		name = utils.name_from_tags( name, 'control', _replacelast=False )
		kwargs[ 'name' ] = name
		
		if 'st' in kwargs :
			shape_type = kwargs.pop( 'st' )
		elif 'shape_type' in kwargs :
			shape_type = kwargs.get( 'shape_type' )		

		kwargs[ 'shape_type' ] = shape_type

		pkwargs = {
			'shape_type' : shape_type
		}

		return kwargs, pkwargs

	@classmethod
	def _createVirtual( cls, **kwargs ) :
		name = kwargs.get( 'name' )
		shape_type = kwargs.get( 'shape_type' )

		control = eval( cls.__shapedict[ shape_type ] )
		control.rename( name )
		utils.create_zero_sdk_groups( control )

		return control.name()

	@classmethod
	def _postCreateVirtual( cls, node, **kwargs ) :
		node = pm.PyNode( node )

		utils.add_set_attr( node , settings.attrname, cls.PARTNAME )
		utils.add_set_attr( node , relatedjointattr, '' )

		# node.addAttr( settings.attrname, dt='string' )
		# node.setAttr( settings.attrname, cls.PARTNAME )



class RigControl( BaseControl ) :
	PARTNAME = 'rigControl'

	def sdk_group( self ) :
		parent = self.getParent()
		d = settings.name_string_delimeter
		n = utils.get_tag( 'sdk' )
		if( parent.name().rsplit( d, 1 )[-1] == n ) :
			return parent
		else :
			utils.err( 'Cannot find %s group for %s' % ( n, self ) )
			return False

	def zero_group( self ) :
		parent = self.getParent().getParent()
		d = settings.name_string_delimeter
		n = utils.get_tag( 'zero' )
		if( parent.name().rsplit( d, 1 )[-1] == n ) :
			return parent
		else :
			utils.err( 'Cannot find %s group for %s' % ( n, self ) )
			return False

	def position_to_object( self, _obj, _offsetobject=None ) :
		target = _obj
		if( _offsetobject ) : target = _offsetobject

		zerogroup = self.zero_group()
		zerogroup.setTranslation( target.getTranslation( space='world' ), space='world' )
		zerogroup.setRotation( target.getRotation( space='world' ), space='world' )
		
		if( target != _obj ) :
			sdkgroup = self.sdk_group()
			sdkgroup.setTranslation( _obj.getTranslation( space='world' ), space='world' )
			sdkgroup.setRotation( _obj.getRotation( space='world' ), space='world' )

		# record which object we positioned it to
		utils.add_set_attr( self, relatedjointattr, _obj )




pm.factories.registerVirtualClass( RigControl, nameRequired=False )