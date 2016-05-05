# Change bound_checking_decorator to handle function with multiple arguments

def bound_checking_decorator(min, max):
  def make_decorator(func):
    def decorator(x):
      if(x < min or x > max):
        raise Exception()
      return func(x)
    return decorator
  return make_decorator