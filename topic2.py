"""
Topic: Analysis of MAX hash collision.
This is not the analysis of expected collision complexity,
but the maximum collision occurs in a hash table.

In the analyses:
	N = bucket size, M = object count.
"""

import math
import random

def countMax(seq):
	""" Count the max (not average nor expected sum) collisions. """
	mxn = 0
	for x in seq:
		mxn = max(mxn, seq[x])
	
	return mxn

def countCollid(N, M):
	cnt = {}
	for i in range(M):
		x = random.randrange(N)
		if not x in cnt:
			cnt[x] = 0
		
		cnt[x] += 1
	
	return countMax(cnt)

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
	F_NlogN = lambda i: math.log2(i+3) / 2
	
	size = 1000
	runSubTest(test1, size, F_NlogN, 'O(logM)')
	runSubTest(test2, size, F_NlogN, 'O(logM)')

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
	def reload(glob=None):
		"""
		Reload this module (at runtime).
			reload(globals())
			OR
			reload() if called from the __main__ module.
		"""
		if glob == None:
			glob = vars(sys.modules['__main__'])
		
		currMod = sys.modules[__name__]
		importlib.reload(currMod)
		
		glob.update({name: getattr(currMod, name) for name in __all__})

	## plotGraph plotting arguments ##
	pltTest1 = dict(func=lambda i: countCollid(bucket, i), domain=(1, 1000), precision=1)
	
	__all__ = ['reload', 'pltTest1']

#--------------------------------------------------------------------