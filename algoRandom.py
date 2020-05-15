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
#	1. that integer operation is O(1).
#	2. that bit_length() is O(1).
#	3. that random.getrandbits were close to O(1).

_BPUF = 52
_FSTP = 2**(-_BPUF)
_FEXPMIN = -1022

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

def _randDecPart(n=1.0):
	# only 52-bit fraction
	for n_bas in range(_BPUF, -1, -1):
		if 2**(-n_bas) >= n:
			k = _BPUF - n_bas + 1
			
			num = getRandBits(k) * _FSTP
			while not num < n:
				num = getRandBits(k) * _FSTP
			
			return num

def _randHighPrecisionDecPart(n=1.0):
	# 52-bit fraction, 11-bit exponent
	frpart = _randDecPart()
	for prec in range(0, _FEXPMIN, -1):
		if getRandBits(prec) == 0:
			continue
		
		return frpart / (2**prec)
	
	return frpart / (2**_FEXPMIN)

_randDecim = _randDecPart

def useHighPrecisionFloat(use=True):
	global _randDecim
	if use:
		_randDecim = _randHighPrecisionDecPart
	
	else:
		_randDecim = _randDecPart

def randReal(n):
	"""
	Return a float from [0, n).
	
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