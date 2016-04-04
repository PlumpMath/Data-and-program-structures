#!/usr/bin/env python3

import unittest
from Interpreter.Environment import Environment
from Interpreter.Function import Function
import Interpreter.ControlExceptions as ControlExceptions
import Utils

class TestFunction(unittest.TestCase):
  
  def func1(self, env):
    self.assertEqual(env.value("arg1"), 10)
    self.assertEqual(env.value("arg2"), 2)
    self.assertEqual(env.value("finalarg"), 5)
  
  def func2(self, env):
    self.assertEqual(env.value("this"), 10)
    self.assertEqual(env.value("arg1"), 2)
    self.assertEqual(env.value("arg2"), 5)
  
  def func3(self, env):
    self.assertEqual(env.value("this"), 10)
    self.assertEqual(env.value("glob"), 4)
    self.assertEqual(env.value("arg1"), 2)
    self.assertEqual(env.value("arg2"), 5)
    env.defineVariable("testator", 2)
    env.setVariable("glob", 3)
  
  def func4(self, env):
    return env.value("arg1") + env.value("arg2")    
  
  def test_function(self):
    #
    # This test that a simple call works
    #
    env  = Environment()
    function = Function(["arg1", "arg2", "finalarg"], env, lambda environment: self.func1(environment))
    function(None, 10, 2, 5)
    function.call(None, None, 10, 2, 5)
    
    #
    # This test that "this" is correctly set
    #
    env  = Environment()
    function = Function(["arg1", "arg2"], env, lambda environment: self.func2(environment))
    function(10, 2, 5)
    function.call(None, 10, 2, 5)
    
    #
    # This test that global variables works
    #
    env  = Environment()
    env.defineVariable("glob", 4)
    function = Function(["arg1", "arg2"], env, lambda environment: self.func3(environment))
    function(10, 2, 5)
    self.assertEqual(env.value("glob"), 3)
    self.assertRaises(Utils.UnknownVariable, env.value, "testator")

    env.setVariable("glob", 4)
    function.call(None, 10, 2, 5)
    self.assertEqual(env.value("glob"), 3)
    self.assertRaises(Utils.UnknownVariable, env.value, "testator")
    
    #
    # This test that the ReturnException is correctly catched in the call function
    #
    env  = Environment()
    function = Function(["arg1", "arg2"], env, lambda environment: self.func4(environment))
    self.assertEqual(function(None, 2, 5), 7)

if __name__ == '__main__':
  unittest.main()
