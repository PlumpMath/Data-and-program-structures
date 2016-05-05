#!/usr/bin/env python3

import time
import unittest
from LogTimingDecorator import Logger, logtiming

logger = Logger()

@logtiming(logger)
def fib(n):
  time.sleep(0.01)
  return n if n < 2 else fib(n-2) + fib(n-1)

def fib_nl(n):
  time.sleep(0.01)
  return n if n < 2 else fib_nl(n-2) + fib_nl(n-1)

@logtiming(logger)
def func3(a, b, c):
  return a + b + c

class TestLogTimingDecorator(unittest.TestCase):
  def test_fib(self):
    start = time.time()
    fib(10)
    end   = time.time()
    self.assertEqual(len(logger.function_calls), 177)
    last = logger.function_calls[176]
    self.assertTrue(last.end - last.start < end - start)
    self.assertTrue(last.end - last.start + 0.1 > end - start)
    self.assertEqual(last.func_args, (10,))
    self.assertEqual(last.func_result, 55)
    for i in range(1, 176):
      before  = logger.function_calls[i-1]
      current = logger.function_calls[i]
      after   = logger.function_calls[i+1]
      
      self.assertEqual(current.func_name, "fib")
      self.assertTrue(before.end < current.end)
      self.assertTrue(current.start < current.end)
      self.assertTrue(current.end < after.end)

      (current_arg,) = current.func_args
      self.assertEqual(fib_nl(current_arg), current.func_result)
      
      (before_arg,) = before.func_args
      if(before_arg < current_arg and before_arg > 1 and current_arg > 1):
        self.assertTrue(before.end - before.start <= current.end - current.start)
      
    func3(2, 1, 2)
    self.assertEqual(len(logger.function_calls), 178)
    last = logger.function_calls[177]
    self.assertEqual(last.func_args, (2,1,2,))
    self.assertEqual(last.func_result, 5)
    
if __name__ == '__main__':
  unittest.main()
