def calcProb(n):
	return ((1.0 - (1.0 / (2 ** (8 * n)) )) ** (2 ** 16))
for i in range(1,6):
	print('i = ', i , ' --- ', calcProb(2**i))
