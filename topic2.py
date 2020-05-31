"""
Topic: Analysis of MAX hash collision.
This is not the analysis of expected collision complexity,
but the maximum collision occurs in a hash table.

In the analyses:
	N = bucket size, M = object count.
"""

import math
import random

def countCollid(N, M):
	# Count the max (not average nor expected sum) collisions.
	cnt = [0] * N
	mxn = 0
	for i in range(M):
		x = random.randrange(N)
		cnt[x] += 1
		mxn = max(mxn, cnt[x])
	
	return mxn

def test1(size=1000):
	""" Fixed N, with M growing. """
	return [countCollid(size, i) for i in range(1, size)]

def test2(size=1000):
	""" With N growing, and N = M. """
	return [countCollid(i, i) for i in range(1, size)]

def runSubTest(testfunc, size, estf=lambda x: x+3, estlabel='O(N)'):
	T = testfunc(size)
	avgt, estt = 0, 0
	for i in range(1, size):
		x = T[i-1]
		avgt += x / size
		estt += x / estf(i) / size
	
	print('Result: average({tfunc}) = {avg:.3f}, average({tfunc}/{estname}) = {est:.3f}'
		.format(tfunc=testfunc.__name__, avg=avgt, est=estt, estname=estlabel))

def runTest():
	def factorSameOrderOfMagnitude(func):
		def wrapFunc(factor=1.0):
			assert(0.1 <= factor <= 10.0) # In same order of magnitude (base 10)
			return func()
		
		return wrapFunc
	
	@factorSameOrderOfMagnitude
	def fNlogN(factor=1.0):
		return (lambda i: math.log2(i+3) * factor)
	
	@factorSameOrderOfMagnitude
	def fN(factor=1.0):
		return (lambda i: (i+1) * factor)
	
	size = 1000
	runSubTest(test1, size, fNlogN(0.43), 'O(logM)') # seems to be logM ?
	runSubTest(test2, size, fNlogN(0.58), 'O(logM)') # seems to be logM too?

#-------------------------- Testing Part ----------------------------
import importlib
import sys

if __name__ == "__main__":
	### MODULE RUN ###
	def main():
		"""
		This only runs simple tests.
		
		Use plotGraph (by Li-Pro) to graph the function.
			plotGraph: https://github.com/Li-Pro/plotGraph.git
		"""
		runTest()

	main()

else:
	### MODULE IMPORTED ###
	def runHook(pathspec='Locals.plotGraph'):
		"""
		Run the external plotGraph program.
		Usage:
			runHook(path_to_plotGraph_folder)
		"""
		plotGraph = __import__(pathspec, fromlist=['plotGraph']).plotGraph
		plotGraph.startPlot({**globals(), **locals()})
	
	def reload(glob=None):
		"""
		Reload this module (at runtime).
		Usage:
			reload() if called from the __main__ module.
			reload(globals()) otherwise.
		"""
		if glob == None:
			glob = vars(sys.modules['__main__'])
		
		currMod = sys.modules[__name__]
		importlib.reload(currMod)
		
		glob.update({name: getattr(currMod, name) for name in __all__})
	
	def testAvg(func, count=100):
		def testFunc(i):
			sumt = 0
			for t in range(count):
				sumt += func(i)
			
			return sumt / count
		
		return testFunc
	
	## plotGraph plotting arguments ##
	pltTest1 = dict(func=testAvg(lambda i: countCollid(1000, i)), domain=(1, 1000), precision=10)
	pltTest2 = dict(func=testAvg(lambda i: countCollid(i, i)), domain=(1, 1000), precision=10)
	
	__all__ = ['reload', 'runHook', 'pltTest1', 'pltTest2']

#--------------------------------------------------------------------