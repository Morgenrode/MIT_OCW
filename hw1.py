'''HW1: Credit card debt/monthly balance calculator.'''

bal = float(input('Outstanding balance on the credit card: '))
intr = float(input('Annual interest rate on the credit card (decimal): '))
#mmr = float(input('Minimum monthly payment (decimal): '))

def remaining_bal(balance, interest, min_rate):
	total = 0
	less_prem = 0
	for month in range(1,13):
		mmp = balance * min_rate
		int_paid = (interest / 12) * balance
		prem_paid = mmp - int_paid
		balance  -= prem_paid
		total += mmp
		less_prem += prem_paid
		print('Month:', month)
		print('Payment:', round(mmp, 2))
		print('Premium paid:', round(prem_paid, 2))
		print('Remaining balance:', round(balance, 2))
		if month == 12:
			print('-' * 25, '\n', 'RESULT')
			print('Total paid: ', round(total, 2), '\n', 'Remaining Balance: ', round(balance, 2))	

def payoff_year(balance, interest_rate):
	mir = interest_rate / 12
	min_payment = balance / 12.0
	top_payment = (balance * ((1 + mir))**12)/12
	x = balance
	month = 0
	while True:
		x = balance
		month = 0
		payment = (top_payment + min_payment)/2
		while month < 12 and x > 0:
			x = x*(1 + mir) - payment
			month += 1
		if top_payment - min_payment < 0.50:
			return (payment, month, x)
		elif x < 0:
			top_payment = payment
		else: 
			min_payment = payment
		print(payment)
		print(x)


print('RESULT  \n Payment needed:  %.2f \n \
Months needed:  %s  \n \
Final balance:  %.2f ' % (payoff_year(bal, intr)))
