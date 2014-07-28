x = float(input('Enter number: '))
epsilon = 0.01
low = -abs(x)
high = max(x, 1.0)
ans = (high + low)/2.0
while abs(ans**3 - x) >= epsilon:
#print 'ans =', ans, 'low =', low, 'high =', high
	if ans**3 < x:
		low = ans
	else:
		high = ans
	ans = (high + low)/2.0
print ans, 'is close to square root of', x 
