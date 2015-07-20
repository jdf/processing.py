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

foundSettings = False
foundSetup = False 
size = False
fullScreen = False
noSmooth = False
smooth = False

def pyde_preprocessor(module):
	global size, fullScreen, noSmooth, smooth, foundSettings, foundSetup

    # Walk throught the abstract syntax tree for the original sketch. 
	for node in module.body:
		if isinstance(node, ast.FunctionDef):
			if (node.name == 'setup'):
				# The user has defined a setup() function. Look through setup() for calls
				# to size(), fullScreen(), noSmooth() and smooth(). 
				foundSetup = True
				for subNode in node.body:
					if isinstance(subNode, ast.Expr):
						if isinstance(subNode.value, ast.Call):
							calledFunc = subNode.value.func.id
							if (calledFunc == "size"):
								size = subNode
								node.body.remove(subNode)
							elif (calledFunc == "fullScreen"):
								fullScreen = subNode
								node.body.remove(subNode)
							elif (calledFunc == "noSmooth"):
								noSmooth = subNode
								node.body.remove(subNode)
							elif (calledFunc == "smooth"):
								smooth = subNode
								node.body.remove(subNode)
			elif (node.name == 'settings'):
				# The user has defined a settings() function. 
				foundSettings = True

	if (size or fullScreen or noSmooth or smooth):
		# The user called one of the settings() subfunctions inside setup.
		if (foundSettings):
			# If a settings function was already defined, go through the tree to find it.
			# Place all of the special function calls inside settings function body. 
			for node in module.body:
				if (isinstance(node, ast.FunctionDef)):
					if (node.name == 'settings'):
						if (smooth):
							node.body.insert(0, smooth)
						if (noSmooth):
							node.body.insert(0, noSmooth)
						if (size):
							node.body.insert(0, size)
						if (fullScreen):
							node.body.insert(0, fullScreen)
						# Don't look through the rest of the tree. 
						break
		else:
			# If a settings function is not defined, we define one and place all of 
			# the special function calls within it. 
			settingsArgs = ast.arguments(args = [], vararg = None, kwarg = None, defaults = [])
			settingsFunc = ast.FunctionDef("settings",settingsArgs,[],[])
			if (noSmooth):
				settingsFunc.body.insert(0, noSmooth)
			if (smooth):
				settingsFunc.body.insert(0, smooth)
			if (size):
				settingsFunc.body.insert(0, size)
			if (fullScreen):
				settingsFunc.body.insert(0, fullScreen)

			# Place the newly defined settings() function within the module body. 
			# It's like it's been there the whole time... 
			module.body.insert(0, settingsFunc)

module = ast.parse(__processing_source__ + "\n\n", filename=__file__)
pyde_preprocessor(module)
print ast.dump(module)

codeobj = compile(module, __file__, mode='exec')
exec(codeobj)
