class AccountError(Exception):
	def __init__(self, value):
		self.value = value
	def str(self):
		return repr(self.value)

def make_account(balance, rate):
	time = 0
	if (rate < 0):
		raise AccountError("Rate not acceptable.")

	def withdraw(amount, t):
		nonlocal time
		nonlocal balance
		if (t < time):
			raise AccountError("Time moving backwards?")
		intrest = (t-time)*rate*balance
		if balance > (amount + intrest):
			balance = balance - (amount + intrest)
			time = t
		else:
			raise AccountError("Account balance too low")

	def deposit(amount, t):
		nonlocal time
		#nonlocal balance
		if (t < time):
			raise AccountError("Time moving backwards?")
		intrest = (t-time)*rate*balance
		balance = balance + amount - intrest
		time = t

	def get_value():
		return balance

	public_methods = {'withdraw' : withdraw, 'deposit' : deposit, 'get_value' : get_value}
	return public_methods

def test():
	a1 = make_account(10,0.1)		# frame 1
	a2 = make_account(10,0.01)		# frame 2
	a1['deposit'](100,10)			# changes in frame 1
	a2['withdraw'](10,10)			# no changes due to AccountError raised from frame 2
	print("balance for a1: {0}".format(a1['get_value']())) # display a1
	print("balance for a2: {0}".format(a2['get_value']())) # display a2
test()
