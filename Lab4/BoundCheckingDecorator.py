from functools import wraps

# Change bound_checking_decorator to handle function with multiple arguments	
def bound_checking_decorator(*bounds)
	if len(bounds) % 2 != 0:
		raise Exception("Uneven number of detorator arguments given.")	
	def make_decorator(func):
		@wraps(func)
		def decorator(*args)
			if not (len(bounds)/2 == len(args))
				raise Exception("Number of bounds doesn't match the number of arguments.")
			for min,max,value in zip(bounds[0::2], bounds[1::2], args):
				if not (min <= value and max >= value)
					raise Exception("Out of bounds.")
			return func(*args)
		return decorator
	return make_decorator