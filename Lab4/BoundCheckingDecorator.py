from functools import wraps

# Change bound_checking_decorator to handle function with multiple arguments

# def bound_checking_decorator(min, max):
#   def make_decorator(func):
#     def decorator(x):
#       if(x < min or x > max):
#         raise Exception()
#       return func(x)
#     return decorator
#   return make_decorator

def bound_checking_decorator(*dec_args):
  if len(dec_args) % 2 != 0:
    raise Exception("Uneven number of detorator arguments given.")
  def make_detorator(func):
    @wraps(func)
    def detorator(*args):
      for i in range(len(args)):
        if args[i] < dec_args[i * 2] or args[i] > dec_args[i * 2 + 1]:
          raise Exception("Out of bounds.")
        return func(*args)
      return decorator
    return make_decorator
