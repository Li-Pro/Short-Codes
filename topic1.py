# Prologue [https://www.facebook.com/groups/1403852566495675/permalink/2623398574541062/]
# Split 1000 randomly into 5 non-zero pieces.

import random
import time

def algoA():
	w = [random.randint(1, 1000) for i in range(5)]  # Weight
	sumW = sum(w)                                    # Weight sum
	
	v = [0 for i in range(5)]                        # Earning
	for i in range(5):
		v[i] = int(1000 * (w[i] / sumW))             # Scale of (w[i]/sumW)
	
	leftMoney = 1000 - sum(v)                        # Issue: Unused money.
	
	# A way to amend this is...
	for i in range(leftMoney):
		j = random.randrange(5)                      # Split them randomly (bruh)
		v[j] += 1
	
	return v

def algoB():
	v = [1 for i in range(5)]
	
	totalLeft = 1000 - 5
	for i in range(4):
		x = random.randrange(totalLeft)  # Randomly pick a number...
		
		v[i] += x
		totalLeft -= x
	
	v[4] += totalLeft
	totalLeft = 0
	
	return v                             # Issue: Uneven probabilities.

def algoC():
	v = [1 for i in range(5)]
	
	totalLeft = 1000 - 5
	for i in range(totalLeft):   # Tends to be O(totalLeft)
		j = random.randrange(5)  # Randomly pick a person to give 1 dollar.
		v[j] += 1
	
	return v

def algoD():
	space = random.sample(range(1, 999), 4)  # Random 4 space
	space = [0] + sorted(space) + [1000]     # Starts from 0, ends at 1000
	
	v = []
	for i in range(5):
		v.append(space[i+1]-space[i])
	
	return v

def analyze(algoFunc, testCnt):
	print('---')
	ana_sttime = time.perf_counter()
	
	totalSum = 0
	sumTest = [0 for i in range(5)]
	for testId in range(testCnt):
		totalSum += 1000
		result = algoFunc()
		assert(sum(result) == 1000)
		
		for i in range(5):
			sumTest[i] += result[i]
	
	ana_edtime = time.perf_counter()
	print('Tested {} with {:>5} tests in {:.3f} second(s).'.format(algoFunc.__name__, testCnt, ana_edtime - ana_sttime))
	print('Average earnings: ', end='')
	for i in range(5):
		print('{:.2f}'.format(10 * (sumTest[i]/totalSum)), end=', ')
	
	print()
	
	print()
	return

def _test():
	analyze(algoA, 10000)  # Correct, but has some solvable issue.
	analyze(algoB, 10000)  # Incorrect
	analyze(algoC,   700)  # Correct but slow (it runs in seconds).
	analyze(algoD, 10000)  # Correct and fast!

if __name__ == "__main__":
	_test()
