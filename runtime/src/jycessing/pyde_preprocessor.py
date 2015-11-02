# This preprocesses a processing python mode sketch by moving any special function calls
# such as size() and fullScreen() out of the setup() function where they may be and into 
# the settings() function. This uses the python ast (abstract syntax tree) module to manipulate 
# structure of the original processing sketch. 
# For example a sketch which originally looks like this :
#
# def setup():
#   size(400,400)
#   <statements>
# def draw():
#   <statements>
# 
# Will actually run as : 
#
# def settings():
#   size(400,400)
# def setup():
#   <statements>
# def draw():
#   <statements>

import ast

class Program_info():
	def __init__(self):
		self.found_settings = False
		self.found_setup = False
		self.size = False
		self.fullScreen = False
		self.noSmooth = False
		self.smooth = False

def pyde_preprocessor(module):
	__program_info__ = Program_info()
    # Walk throught the abstract syntax tree for the original sketch. 
	for node in module.body:
		if isinstance(node, ast.FunctionDef):
			if (node.name == 'setup'):
				# The user has defined a setup() function. Look through setup() for calls
				# to size(), fullScreen(), noSmooth() and smooth(). 
				__program_info__.found_setup = True
				for subNode in node.body:
					if isinstance(subNode, ast.Expr):
						if isinstance(subNode.value, ast.Call):
							func = subNode.value.func
							if hasattr(func, 'id') and func.id in ('size', 'fullScreen', 'noSmooth', 'smooth'):
								node.body.remove(subNode)
								setattr(__program_info__, func.id, subNode)
			elif (node.name == 'settings'):
				# The user has defined a settings() function. 
				__program_info__.found_settings = True

	if (__program_info__.size or __program_info__.fullScreen or __program_info__.noSmooth or __program_info__.smooth):
		# The user called one of the settings() subfunctions inside setup.
		if (__program_info__.found_settings):
			# If a settings function was already defined, go through the tree to find it.
			# Place all of the special function calls inside settings function body. 
			for node in module.body:
				if (isinstance(node, ast.FunctionDef)):
					if (node.name == 'settings'):
						if (__program_info__.smooth):
							node.body.insert(0, __program_info__.smooth)
						if (__program_info__.noSmooth):
							node.body.insert(0, __program_info__.noSmooth)
						if (__program_info__.size):
							node.body.insert(0, __program_info__.size)
						if (__program_info__.fullScreen):
							node.body.insert(0, __program_info__.fullScreen)
						# Don't look through the rest of the tree. 
						break
		else:
			# If a settings function is not defined, we define one and place all of 
			# the special function calls within it. 
			settingsArgs = ast.arguments(args = [], vararg = None, kwarg = None, defaults = [])
			settingsFunc = ast.FunctionDef("settings",settingsArgs,[],[])
			if (__program_info__.noSmooth):
				settingsFunc.body.insert(0, __program_info__.noSmooth)
			if (__program_info__.smooth):
				settingsFunc.body.insert(0, __program_info__.smooth)
			if (__program_info__.size):
				settingsFunc.body.insert(0, __program_info__.size)
			if (__program_info__.fullScreen):
				settingsFunc.body.insert(0, __program_info__.fullScreen)

			# Place the newly defined settings() function within the module body. 
			# It's like it's been there the whole time... 
			module.body.insert(0, settingsFunc)

module = ast.parse(__processing_source__ + "\n\n", filename=__file__)
pyde_preprocessor(module)

codeobj = compile(module, __file__, mode='exec')
exec(codeobj)
