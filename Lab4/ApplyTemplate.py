import ast
import inspect
from functools import wraps

# Change bound_checking_decorator to handle function with multiple arguments
def apply_template(*template_args):
  def make_decorator(func):
    @wraps(func)
    def decorator(*args):
      for name, arg_func in zip(template_args[0::2], template_args[1::2]):
          # TODO: Fix this.
      return func
    return decorator
  return make_decorator
