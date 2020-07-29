"""
A simple O(NlogN) sorting algorithm.
"""

import random
import time

def merge(ax, ay):
	i, j, k, nx, ny = 0, 0, 0, len(ax), len(ay)
	az = [None]*(nx + ny)
	
	while (i < nx) or (j < ny):
		if (not j < ny) or (i < nx and ax[i] < ay[j]):
			az[k] = ax[i]
			i, k = i+1, k+1
		else:
			az[k] = ay[j]
			j, k = j+1, k+1
	
	return az

def nextDesc(arr, i):
	N = len(arr)
	j = i+1
	while j < N:
		if arr[j] >= arr[j-1]:
			j += 1
		else:
			break
	
	return j

def sort(arr):
	N = len(arr)
	
	while True:
		i = 0
		while i < N:
			j = nextDesc(arr, i)
			if j == N:
				break
			
			k = nextDesc(arr, j)
			
			arr[i: k] = merge(arr[i: j], arr[j: k])
			i = k
		
		if i == 0:
			break
	
	return arr

def check(result, arr):
	return result == sorted(arr)

def main():
	N = 10**5
	C = 10**9
	
	arr = [random.randrange(C) for i in range(N)]
	arrTest = [arr[i] for i in range(N)]
	
	sttime = time.perf_counter()
	sort(arrTest)
	edtime = time.perf_counter()
	
	print('Check: {}.'.format('passed' if check(arrTest, arr) else 'failed'))
	print('Elapsed time: {:.3f} seconds'.format(edtime - sttime))

main()