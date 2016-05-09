import ast
import inspect
from functools import wraps

#Trevlig bok(?) som går igenom bland annat python decorators.
#Länk: http://python-3-patterns-idioms-test.readthedocs.io/en/latest/PythonDecorators.html#the-goal-of-macros

'''
Sammanfattning:
Problemet verkar vara att funktionen som kallar på apply_template inte vet hur den ska översätta __body__ (och __return__ antar jag)

http://stackoverflow.com/questions/4851463/python-closure-write-to-variable-in-parent-scope

jag tolkar det som att det är hundra gånger smidigare att hantera scope-hopp genom klasser snarare än funktioner.

koden nedan fuckar då func.__body__ existerar i decorator men existerar inte då func(args) körs.


Output:

-- Start of decorator --

Argument number:  1
Name:  __body__
arg_func:  <function func_body at 0x7f53f0106bf8>
function:  <function func1 at 0x7f53edaf3620>
arguments to decorator:  (10,)
template args:  ('__body__', <function func_body at 0x7f53f0106bf8>, '__return__', <function func_return at 0x7f53edaf3510>)

Argument number:  2
Name:  __return__
arg_func:  <function func_return at 0x7f53edaf3510>
function:  <function func1 at 0x7f53edaf3620>
arguments to decorator:  (10,)
template args:  ('__body__', <function func_body at 0x7f53f0106bf8>, '__return__', <function func_return at 0x7f53edaf3510>)
__body__ ::  <function func_body at 0x7f53f0106bf8> __return__ ::  <function func_return at 0x7f53edaf3510>
-- End of decorator --
E

ERROR: test_func1 (__main__.TestApplyTemplate)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/TDDA69/Labs/Lab4/Tests/TestApplyTemplate.py", line 26, in test_func1
    self.assertEqual(func1(10), 3628800)
  File "/home/timos520/Desktop/TDDA69/LABS/alla-3/Lab4/ApplyTemplate.py", line 42, in decorator
    return func(args)
  File "/home/TDDA69/Labs/Lab4/Tests/TestApplyTemplate.py", line 15, in func1
    __body__
NameError: name '__body__' is not defined


--




"line 42" motsvarar raden:       return func(args)  (denna text skrevs efter det att jag kopierade traceback)

'''

def apply_template(*template_args):
  def make_decorator(func):
    @wraps(func)
    def decorator(*args):

      print("")
      print("-- Start of decorator --")
      i = 1
      for name, arg_func in zip(template_args[0::2], template_args[1::2]):
          setattr(func, name, arg_func)

          # TODO: Fix this.
          print("")
          print("Argument number: ", i)
          print("Name: ", name)
          print("arg_func: ", arg_func)
          print("function: ",func)
          print("arguments to decorator: ",str(args))
          print("template args: ", str(template_args))
          i += 1
      if func.__body__ and func.__return__:
        print("__body__ :: ", func.__body__, "__return__ :: ", func.__return__)
      else:
        print("body or return are missing.")
      print("-- End of decorator --")

      return func(args)
    return decorator
  return make_decorator
