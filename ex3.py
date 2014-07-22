'''Given a string containing comma-separated decimal numbers, 
print the sum of the numbers contained in the string.'''
s = input('Enter numbers, separated by commas: ')
print(sum(float(x) for x in s.split(',')))
