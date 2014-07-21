'''Given three integers: print the largest odd integer'''
x = int(input('First number: '))
y = int(input('Second number: '))
z = int(input('Third number: '))

# Evens are excluded, as even % 2 == 0
if max(x % 2 * x, y % 2 * y, z % 2 * z) != 0:
	print(max(x % 2 * x, y % 2 * y, z % 2 * z))
else:
	print('No odd numbers were input.')
