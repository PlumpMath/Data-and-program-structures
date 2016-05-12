import time
from functools import wraps

class LogEntry:

  def __init__(self, func_name, func_args, func_result, start, end):
    self.func_name = func_name
    self.func_args = func_args
    self.func_result = func_result
    self.start = start
    self.end = end


class Logger:
  '''
  Logger class. It should contains an array of objects containing the information about function calls
  '''

  def __init__(self):
    self.function_calls = list()


  def log_function_call(self, func_name, func_args, func_result, start, end):
    '''
    Call this function after the function has finished been executed
    func_name: name of the function
    func_args: list of arguments of the function
    func_result: return value from the function call
    start: time when the function was started
    end:   time when the function has finish execution
    '''
    self.function_calls.append(LogEntry(func_name, func_args, func_result, start, end))


def logtiming(logger):
  '''
  Decorator that will add an entry in logger after a function call
  '''
  def make_decorator(func):
    @wraps(func)
    def decorator(*args):
      start = time.perf_counter()
      retval = func(*args)
      stop = time.perf_counter()
      logger.log_function_call(func.__name__, args, retval, start, stop)
      return retval
    return decorator
  return make_decorator
