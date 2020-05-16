# Prologue [https://www.facebook.com/groups/1403852566495675/permalink/2623398574541062/]
# Split 1000 randomly into 5 non-zero pieces.
"""
喔 最近也在寫random
看到上面有很多有創意的做法
順便整理&分析一下上面的作法

一開始大家基本都是10元到小數後2為看做1000元

然後有:
A. 取亂數W[5] 做分錢的比例
B. 先發 1, 然後連續 random每個人的錢數
C. 先發 1, 對於每單位錢random要分給誰
D. 分成999個空格, random 4個

A. 重點在於每個 Wi>0 則不會有人分不到錢
缺點很明顯, 因為分的錢數不是連續的, 較難滿足比重->單位的轉換。
比如說, random出來的總比重 = 999, 那多的那 1元就很難解決囉w

B. 從1到5做random / 依順序、每次隨機做random
先說這樣的方式是不對的, 因為機率"超~級~不平均"
應該不難想像, 因為這樣的作法對於每個人多拿1元的機率並不相等。
(對第一個人來說可能是1/5, 對第二個人卻是1/4)
剛用python測試出來結果也確實差很多w (越前面賺越多)

C. 很正確又值觀的作法
每1元都用相同的機率分給所有人。
小缺點: 對於更大的錢數效能不足 ( 對於錢數=C 的複雜度是O(C) )

D. 這是我的作法
把鈔票排一排鋪在地上, 鈔票中會有999個空格, 只要選出4個不同的空格就可以平均分配了。
蠻直觀的吧w 剩下就是random出4個空格的部分:
每次隨機挑一個空格, 挑到重覆的就重新再random一個。
如果你是用python的話, "random.sample(range(1, 999), 4)" 就完事了w
順帶一提, 這個演算法對於錢數極高&人數極多都一樣有良好的效率。
"""

import random

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
	space = sorted([0] + space + [1000])     # Starts from 0, ends at 1000
	
	v = []
	for i in range(5):
		v.append(space[i+1]-space[i])
	
	return v

def analyze(algoFunc):
	print('Testing function: ' + algoFunc.__name__)
	
	totalSum = 0
	sumTest = [0 for i in range(5)]
	for testId in range(1000):
		totalSum += 1000
		result = algoFunc()
		assert(sum(result) == 1000)
		
		for i in range(5):
			sumTest[i] += result[i]
	
	print('Average earnings: ', end='')
	for i in range(5):
		print('{:.2f}'.format(10 * (sumTest[i]/totalSum)), end=', ')
	
	print('\n')
	return

def _test():
	analyze(algoA)  # Correct, but has some solvable issue.
	analyze(algoB)  # Incorrect
	analyze(algoC)  # Correct but slow (it runs in seconds).
	analyze(algoD)  # Correct and fast!

if __name__ == "__main__":
	_test()
