'''Takes an integer and returns two integers, root and pwr, such that 0 < pwr < 6 and root**pwr = integer provided.'''

x = int(input('Enter desired integer: '))

root = 1
pwr = 1
if x > 1:
	while root**pwr < x or pwr > 1: # stops the loop if root**1 > x, so non-infinite
		pwr = 1 # reset pwr for incrementing
		while pwr < 6:
			if root**pwr < x:
				pwr += 1
			elif root**pwr == x:
				print(x, '=', root, '^', pwr)
				break
			else:
				break
		root += 1
elif x == 1 or x == 0:
	print(x, '=', x, '^ any pwr')
else:
	while root**pwr > x or pwr > 1:
		pwr = 1
		while pwr < 6:
			if root**pwr > x:
				pwr += 2 # Nothing negative has an even exponent
			elif root**pwr == x:
				print(x, '=', root, '^', pwr)
				break
			else:
				break
		root -= 1
