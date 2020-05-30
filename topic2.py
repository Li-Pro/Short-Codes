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

def main():
	"""
	This only runs simple tests.
	
	Use plotGraph (by Li-Pro) to graph the function.
		plotGraph: https://github.com/Li-Pro/plotGraph.git
	"""
	runTest()

def reload():
	currMod = sys.modules[__name__]
	importlib.reload()

if __name__ == "__main__":
	main()
else:
	# plotGraph plotting arguments
	pltTest1 = dict(lambda x: countMax(test1(1000, x)), domain=(1, 1000), precision=1)

#--------------------------------------------------------------------