#!/usr/bin/env python3

import unittest
from BoundCheckingDecorator import bound_checking_decorator

@bound_checking_decorator(0, float('inf'))
def fib(n):
  return n if n < 2 else fib(n-2) + fib(n-1)

@bound_checking_decorator(-1, 1, -2, 2, -3, 3)
def func3(a, b, c):
  return a + b + c

class TestBoundCheckingDecorator(unittest.TestCase):
  def test_fib(self):
    self.assertEqual(fib(15), 610)
    self.assertRaises(Exception, fib, -1)
  def test_func3(self):
    self.assertEqual(func3(1, 1, 2), 4)
    self.assertEqual(func3(0, 1, 2), 3)
    self.assertRaises(Exception, func3, -2, 3, -4)
    self.assertRaises(Exception, func3, 2, -3, 4)
    self.assertRaises(Exception, func3, -2, 1, 1)
    self.assertRaises(Exception, func3, 2, 1, 1)
    self.assertRaises(Exception, func3, 0, 3, 1)
    self.assertRaises(Exception, func3, 0, -3, 1)
    self.assertRaises(Exception, func3, 0, 0, 4)
    self.assertRaises(Exception, func3, 0, 0, -4)

if __name__ == '__main__':
  unittest.main()
