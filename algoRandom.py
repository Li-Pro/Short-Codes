"""
Implementation of some basic randomized algorithms.
NOT including random generator algorithm (yet(?)).
"""

#----------- Psuedo Random Generator ------------
# This part is just for testing.

import random as _librandom

def _randBit():
	return _librandom.getrandbits(1)

def setSeed(seed=None):
	"""
	Set the random seed.
	
	Quote from <random>:
		None or no argument seeds from current time or from an operating
		system specific randomness source if available.
	
	Complexity:
		= T(random.seed)
	"""
	_librandom.seed(seed)
	return

#------------------------------------------------

import math

# Note:
#	Analyses assume...
#	1. that integer operation is O(1).
#	2. that bit_length() is O(1).

_BPUF = 52
_UFMIN = 2**(-_BPUF)

def getRandBits(k):
	"""
	Return an integer with k random bits.
	
	Complexity:
		O(k)
	"""
	bits = 0
	for i in range(k):
		bits = (bits << 1) | _randBit()
	
	return bits

def _randUnder(N):
	k = N.bit_length()
	num = getRandBits(k)
	while not num < N:
		num = getRandBits(k)
	
	return num

def randRange(a, b):
	"""
	Return an integer with range [a, b).
	
	Complexity:
		O(1) with high probability.
	"""
	length = b - a
	num = a + _randUnder(length)
	return num

def rand(N):
	"""
	Return an integer with range [0, N).
	Alias of `randRange(0, N)`.
	
	Complexity:
		= T(randRange)
	"""
	return randRange(0, N)

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

def _randDecPart():
	num = 0
	for i in range(_BPUF):
		num = num * 2 + (_UFMIN * getRandBits(1))
	
	return num

def _randDecUnder(n):
	divBase = math.floor(1 / n)
	k = divBase.bit_length()
	
	return

def randReal():
	"""
	Return a float from [0, 1).
	
	Complexity:
		O(1)
	"""
	

def randRealRange(a, b):
	"""
	Return a float from [a, b).
	
	Complexity:
		O(1)
	"""
	intNum = randRange(a, b)
	num = intNum + randReal()
	return num

#---------------- Testing Part ------------------

import code as _libcode

if __name__ == "__main__":
	console = _libcode.InteractiveConsole({**globals(), **locals()})
	console.interact()

#------------------------------------------------