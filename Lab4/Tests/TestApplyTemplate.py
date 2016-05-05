#!/usr/bin/env python3

import unittest
from ApplyTemplate import apply_template

def func_body(v):
    v = v * x
    
def func_return():
  return v

@apply_template("__body__", func_body, "__return__", func_return)
def func1(v):
  for x in range(1,10):
    __body__
  __return__

@apply_template("__body__", func_body, "__return__", func_return)
def func2(v):
  x = 2
  __body__
  __return__

class TestApplyTemplate(unittest.TestCase):
  def test_func1(self):
    self.assertEqual(func1(10), 3628800)
  def test_func2(self):
    self.assertEqual(func2(10), 20)

if __name__ == '__main__':
  unittest.main()

