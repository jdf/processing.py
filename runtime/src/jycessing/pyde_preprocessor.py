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

	def insert(self, body):
		for attr in ('size', 'fullScreen', 'noSmooth', 'smooth'):
			if getattr(self, attr):
				body.insert(0, getattr(self, attr))
		
def pyde_preprocessor(module):
	info = Program_info()
    # Walk throught the abstract syntax tree for the original sketch. 
	for node in module.body:
		if isinstance(node, ast.FunctionDef):
			if (node.name == 'setup'):
				# The user has defined a setup() function. Look through setup() for calls
				# to size(), fullScreen(), noSmooth() and smooth(). 
				info.found_setup = True
				for subNode in node.body:
					if not isinstance(subNode, ast.Expr):
						continue
					if not isinstance(subNode.value, ast.Call):
						continue
					func = subNode.value.func
					if hasattr(func, 'id') and func.id in ('size', 'fullScreen', 'noSmooth', 'smooth'):
						node.body.remove(subNode)
						setattr(info, func.id, subNode)
			elif (node.name == 'settings'):
				# The user has defined a settings() function. 
				info.found_settings = True

	if (info.size or info.fullScreen or info.noSmooth or info.smooth):
		# The user called one of the settings() subfunctions inside setup.
		if (info.found_settings):
			# If a settings function was already defined, go through the tree to find it.
			# Place all of the special function calls inside settings function body. 
			for node in module.body:
				if (isinstance(node, ast.FunctionDef)):
					if (node.name == 'settings'):
						info.insert(node.body)
						break
		else:
			# If a settings function is not defined, we define one and place all of 
			# the special function calls within it. 
			settingsArgs = ast.arguments(args=[], vararg=None, kwarg=None, defaults=[])
			settingsFunc = ast.FunctionDef("settings", settingsArgs, [], [])
			info.insert(settingsFunc.body)
			# Place the newly defined settings() function within the module body. 
			# It's like it's been there the whole time... 
			module.body.insert(0, settingsFunc)

module = ast.parse(__processing_source__ + "\n\n", filename=__file__)
pyde_preprocessor(module)

codeobj = compile(module, __file__, mode='exec') 
exec(codeobj)
