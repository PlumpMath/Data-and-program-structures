Inaktiv	Lars Eriksson
Offline	Alexander Örtenberg
Offline	Anders Wirén
Offline	davrex
Offline	Joel Strömblad
Offline	Oscar Sandkvist
10 av 2 199
schema
Inkorgen
	×
Tim Österlund <timos520@student.liu.se>
	
19 jan.
		
till mig
https://se.timeedit.net/web/liu/db1/schema/ri15YXQ2651Z53Qv9X025986y4Y550986Y63Y9gQ9076X85Z35347Y679XX66550Y9748459794Y5585Q7.html
Tim Österlund	
IDA - gammalt TDDA69 (huvudsakligen lab1) 2016-01-19 7:12 GMT+01:00 Tim Öster...
	Bilagor19 jan.
Tim Österlund	
...
	Bilagor3 feb. (4 dagar sedan)
Tim Österlund <timos520@student.liu.se>
	
Bilagor4 feb. (3 dagar sedan)
		
till mig
Lab 1 solved. (?)
4 bilagor
Förhandsgranska bilaga account.py
[Text]
Förhandsgranska bilaga constraints.py
[Text]
Förhandsgranska bilaga lab1.py
[Text]
Förhandsgranska bilaga temperature.py
[Text]
	
Klicka här om du vill Svara eller Vidarebefordra
Använder 0,73 GB
Hantera
Programpolicy
Tillhandahålls av
Google
Senaste kontoaktivitet: 11 timmar sedan
Information
	
	

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
	
def test()
	a1 = make_account(10,0.1)		# frame 1
	a2 = make_account(10,0.01)		# frame 2
	a1['deposit'](100,10)			# changes in frame 1
	a2['withdraw'](10,10)			# no changes due to AccountError raised from frame 2
	print("balance for a1: {0}".format(a1['get_value']())) # display a1
	print("balance for a2: {0}".format(a2['get_value']())) # display a2
test()	
