import time

class Logger:
  '''
  Logger class. It should contains an array of objects containing the information about function calls
  '''
  
  def __init__(self):
    pass
  def log_function_call(self, func_name, func_args, func_result, start, end):
    '''
    Call this function after the function has finished been executed
    func_name: name of the function
    func_args: list of arguments of the function
    func_result: return value from the function call
    start: time when the function was started
    end:   time when the function has finish execution
    '''
    pass

def logtiming(logger):
  '''
  Decorator that will add an entry in logger after a function call
  '''
  pass
