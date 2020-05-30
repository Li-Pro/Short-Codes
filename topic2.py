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

def countCollid(N, M):
	cnt = {}
	for i in range(M):
		x = random.randrange(0, N)
		if not x in cnt:
			cnt[x] = 0
		
		cnt[x] += 1
	
	return countMax(cnt)

def test1(bucket=1000):
	""" Fixed N, with M growing. """
	return [countCollid(bucket, i) for i in range(1, bucket)]

def runSubTest(testfunc, bucket, estf=lambda x: x+3, estlabel='O(N)'):
	T = testfunc(bucket)
	sumt, avgt = 0, 0
	for i in range(1, bucket):
		x = T[i-1]
		sumt += x
		avgt += x / estf(i)
	
	print('Result: sum({tfunc}) = {sumt}, sum({tfunc}/{est}) = {avgt}'
		.format(tfunc=testfunc.__name__, sumt=sumt, avgt=avgt, est=estlabel))

def runTest():
	F_NlogN = lambda i: (i+3) * math.log2(i+3)
	
	bucket_size = 1000
	runSubTest(test1, bucket_size, F_NlogN, estlabel='O(NlogN)')
	
	# T1 = test1(bucket_size)
	# st1, st1avg = 0, 0
	# for i in range(1, bucket_size):
		# x = T1[i-1]
		# st1 += x
		# st1avg += x / (2 * (i+3) * math.log2(i+3))
	
	# print('sum(test1) = {}, sum(test1/O(NlogN)) = {}'.format(st1, st1avg))


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