"""
A simple python interaction console.
Use interact() to open the console.
"""

from code import InteractiveConsole as _console
from sys import version_info as _version, modules as _modules
from importlib import reload as _reload

class _namedFunction:
	def __init__(self, func=lambda: None, label=''):
		self.__func = func
		self.__label = label
		
		self.docs = 'No help entry found for this command.'
	
	def __repr__(self):
		return '{}\n'.format(self.__label)
	
	def __call__(self, *args, **kwargs):
		return self.__func(*args, **kwargs)
	
	def setHelpDoc(self, theDoc):
		self.docs = theDoc
		return self


## Command clear ##
_clear_doc = \
"""
clear() clears the screen (with 100 empty lines).
""".strip()

clear = _namedFunction(lambda: print('\n'*100), 'Type clear() to clean the screen.').setHelpDoc(_clear_doc)


## Command reload ##
_reload_doc = \
"""
Reload a module.
Parameters:
	theMod - the module (str / module).
	
	Optional Parameters:
		fromList - the list to import (from <theMod> import <fromList>).
		toNamespace - when <fromList> is specified, save the import names into <toNamespace> (usually globals() / locals()).
	
	Examples:
		reload(math)
		reload(math, fromList=['sin'], toNamespace=globals())
""".strip()

def _reloadModule(theMod, fromList=[], toNamespace=globals()):
	if type(theMod) == str:
		theMod = _modules[theMod]
	
	_reload(theMod)
	
	if type(toNamespace).__name__ == 'module':
		toNamespace = vars(toNamespace)
	
	fromNamespace = vars(theMod)
	for name in fromList:
		toNamespace[name] = fromNamespace[name]
	
	return theMod

reload = _namedFunction(_reloadModule, 'Type reload(...) to reload a module, help_extra(reload) for help.').setHelpDoc(_reload_doc)


## Command help ##
_help_msg = \
"""
Type help_extra(<obj>) for help about command <obj>.

List of extra commands:
	help_extra - show help about console add-on commands.
	clear - clean the screen.
	reload - reload a module.
""".strip()

def _loadHelp(obj=None):
	if obj == None:
		print(_help_msg +'\n')
	else:
		if not isinstance(obj, _namedFunction):
			print('"{}" is not an add-on command.\n'.format(obj))
		else:
			print(obj.docs +'\n')

help_extra = _namedFunction(_loadHelp, _help_msg).setHelpDoc(_help_msg)


__all__ = ['clear', 'reload', 'help_extra']

def interact(startMsg=None, extraVars={}):
	"""
	Open a Python interactive console.
	Parameters:
		startMsg - the startup message.
		extraVars - load the <extraVars> into console variables.
	"""
	if startMsg == None:
		cprt = 'Type "help", "help_extra", "copyright", "credits" or "license" for more information.'
		msgs = [
			'Python v{} Interactive Console'.format('.'.join(map(str, _version[0:3]))),
			cprt,
		]
		startMsg = '\n'.join(msgs)
	elif startMsg != '':
		startMsg = '{}\n'.format(startMsg)
	
	extraFeature = {name: globals()[name] for name in __all__}
	console = _console({**extraFeature, **extraVars})
	console.interact(banner=startMsg, exitmsg='')

if __name__ == '__main__':
	interact()