"""
Topic: Analysis of hash collision.
N = bucket size, M = object count.
"""

import math
import random

def countMax(seq):
	mxn = 0
	for x in seq:
		mxn = max(mxn, seq[x])
	
	return mxn

def test1(N, M):
	""" Fixed N, with M growing. """
	cnt = {}
	for i in range(M):
		x = random.randrange(0, N)
		if not x in cnt:
			cnt[x] = 0
		
		cnt[x] += 1
	
	return cnt

def runTest():
	st1, st1avg = 0, 0
	for i in range(1, 1000):
		x = countMax(test1(1000, i))
		st1 += x
		st1avg += x / (3 * i * math.log2(i+1))
	
	print('sum(test1) = {}, sum(test1/O(NlogN)) = {}'.format(st1, st1avg))


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
		
		# print('hah', {name: getattr(currMod, name) for name in __all__})
		glob.update({name: getattr(currMod, name) for name in __all__})

	# plotGraph plotting arguments
	pltTest1 = dict(func=lambda x: countMax(test1(1000, x)), domain=(1, 1000), precision=1)
	
	__all__ = ['reload', 'pltTest1']

#--------------------------------------------------------------------