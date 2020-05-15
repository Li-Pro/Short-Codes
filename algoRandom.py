"""
Implementation of some basic randomized algorithms.
NOT including random generator algorithm (yet(?)).
"""

#----------- Psuedo Random Generator ------------
# This part is just for testing.

import random as _librandom

def setSeed(seed=None):
	"""
	Set the random seed.
	
	Quote from <random>:
		None or no argument seeds from current time or from an operating
		system specific randomness source if available.
	"""
	_librandom.seed(seed)
	return

def getRandBits(k):
	"""
	Return a k-bit integer.
	This is the basic generator.
	"""
	return _librandom.getrandbits(k)

#------------------------------------------------


import math

# Note:
#	Analyses assume...
#	1. that number operation & functions is O(1).
#	2. that the maximum bit length is fixed.

_BPUF = 52
_FSTP = 2**(-_BPUF)

def rand(N):
	"""
	Return an integer with range [0, N).
	
	Complexity:
		O(1) with high probability.
	"""
	k = N.bit_length()
	num = getRandBits(k)
	while not num < N:
		num = getRandBits(k)
	
	return num

def randRange(a, b):
	"""
	Return an integer with range [a, b).
	
	Complexity:
		O(1)
	"""
	length = b - a
	num = a + rand(length)
	return num

def shuffle(arr):
	"""
	Shuffle the sequence arr.
	
	Complexity:
		O(len(arr))
	
	Remarks:
		RANDOM~~ SHUFFLE~~
	"""
	N = len(arr)
	for i in range(N):
		swapId = rand(i+1)
		arr[i], arr[swapId] = arr[swapId], arr[i]
	
	return

def sample(seq, k):
	"""
	Pick k different ones from sequence seq (unordered).
	
	Complexity:
		O(N (logN-log(N-k))) where N = len(seq), with high probability.
		Close to O(k) for relative small k.
	"""
	picked = set()
	
	arr = []
	N = len(seq)
	for i in range(k):
		p = seq[rand(N)]
		while p in picked:
			p = seq[rand(N)]
		
		picked.add(p)
		arr.append(p)
	
	return arr

def randReal(n=1.0):
	"""
	Return a float from [0, n).
	
	Complexity:
		O(1) with high probability.
	"""
	if not n:
		return 0
	
	baseLen = math.ceil(math.log2(n))
	base = 2**baseLen
	
	num = getRandBits(_BPUF) * _FSTP * base
	while not num < n:
		num = getRandBits(_BPUF) * _FSTP * base
	
	return num

def randRealRange(a, b):
	"""
	Return a float from [a, b).
	
	Complexity:
		O(1)
	"""
	length = b-a
	num = a + randReal(length)
	
	return num

def unitChoice(arr, cumWeigt):
	"""
	Choose an element from arr.
	Each element has their specific cumulative weight, which sum to 1.0
	
	Complexity:
		O(logN) where N = len(arr).
	"""
	x = randReal()
	L, R = 0, len(arr)-1
	while L < R:
		i = (L + R + 1) // 2
		if cumWeigt[i] >= x:
			R = i - 1
		
		else:
			L = i
	
	return arr[L]

def choice(arr, weight):
	"""
	Choose an element from arr, with their specified weights.
	
	Complexity:
		O(N) where N = len(arr).
	"""
	sumWgt = sum(weight)
	
	cumWgt, sumNow = [], 0
	for w in weight:
		cumWgt.append(sumNow)
		sumNow += w/sumWgt
	
	return unitChoice(arr, cumWgt)


#---------------- Testing Part ------------------

import code as _libcode

if __name__ == "__main__":
	console = _libcode.InteractiveConsole({**globals(), **locals()})
	console.interact()

#------------------------------------------------