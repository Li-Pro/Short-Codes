import random
import time

def merge(ax, ay):
	i, j, k, nx, ny = 0, 0, 0, len(ax), len(ay)
	az = [None]*(nx+ny)
	
	def addi():
		nonlocal ax, az, i, k
		az[k] = ax[i]
		i, k = i+1, k+1
	
	def addj():
		nonlocal ay, az, j, k
		az[k] = ay[j]
		j, k = j+1, k+1
	
	while i<nx or j<ny:
		if not i<nx:
			addj()
		elif not j<ny:
			addi()
		else:
			if ax[i] < ay[j]:
				addi()
			else:
				addj()
	
	return az

def countAscend(arr, i):
	N = len(arr)
	cnt = 1
	while i+cnt < N:
		if arr[i+cnt] >= arr[i+cnt-1]:
			cnt += 1
		else:
			break
	
	return cnt

def isSorted(arr):
	for i in range(1, len(arr)):
		if arr[i] < arr[i-1]:
			return False
	
	return True

def sort(arr):
	# print('#', arr)
	# print('#')
	
	i, N = 0, len(arr)
	while i < N:
		a = countAscend(arr, i)
		if a == N-i:
			break
		
		b = countAscend(arr, i+a)
		
		arr[i: i+a+b] = merge(arr[i: i+a], arr[i+a: i+a+b])
		i = i+a+b
	
	if not isSorted(arr):
		return sort(arr)
	else:
		return arr

def check(arr, answer):
	return arr == answer

def main():
	N = 10**5 # input()
	C = 10**9
	
	arr = [random.randrange(C) for i in range(N)]
	answer = sorted(arr)
	
	sttime = time.perf_counter()
	sort(arr)
	edtime = time.perf_counter()
	
	print('Check: {}.'.format('passed' if check(arr, answer) else 'failed'))
	print('Elapsed time: {:.3f} seconds'.format(edtime - sttime))

main()