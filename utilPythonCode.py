"""
A simple python interaction console.
"""

from code import InteractiveConsole as _console
from sys import version_info as _version, modules as _modules
from importlib import reload as _reload

class _namedFunction:
	def __init__(self, func=lambda: None, label=''):
		self.__func = func
		self.__label = label
		
		self.__docs = 'No help entry found for this command.'
	
	def __repr__(self):
		return '{}\n'.format(self.__label)
	
	def __call__(self):
		return self.__func()
	
	def setHelpDoc(self, theDoc):
		self.__docs = theDoc
		return self

_currMod = _modules[__name__]
def _reloadModule(theMod, fromList=[], toNamespace=_currMod):
	"""
	Reload a module.
	"""
	if type(theMod) == str:
		theMod = _modules[theMod]
	
	_reload(theMod)
	if type(toNamespace).__name__ == 'module':
		toNamespace = vars(toNamespace)
	

def _loadHelp():
	return

clear = _namedFunction(lambda: print('\n'*100), 'Type clear() to clean the screen.')
reload = _namedFunction(_reloadModule, 'Type reload(...) to reload a module, help(reload) for help.').setHelpDoc(_reloadModule.__doc__.strip())

_help_msg = \
"""
Type help_extra(<obj>) for help about command <obj>.
List of extra commands:
	clear - clean the screen.
	reload - reload a module.
""".strip()

help_extra = _namedFunction(lambda: print(_help_msg +'\n'), _help_msg)

__all__ = ['clear', 'reload', 'help_extra']

def interact(startMsg=None, extraVars={}):
	if startMsg == None:
		cprt = 'Type "help", "help_extra", "copyright", "credits" or "license" for more information.'
		msgs = [
			'Python v{} Interactive Console'.format('.'.join(map(str, _version[0:3]))),
			cprt,
		]
		startMsg = '\n'.join(msgs)
	
	extraFeature = {name: globals()[name] for name in __all__}
	console = _console({**extraFeature, **extraVars})
	console.interact(banner=startMsg, exitmsg='')

if __name__ == '__main__':
	interact()