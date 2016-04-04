#!/usr/bin/env python3

import unittest
from Interpreter.Environment import Environment
import Utils

class TestEnvironment(unittest.TestCase):
  def test_single_environment(self):
    environment = Environment()    
    self.assertRaises(Utils.UnknownVariable, environment.value, "test")
    environment.defineVariable("test", 10)
    self.assertEqual(environment.value("test"), 10)
    environment.setVariable("test", 5)
    self.assertEqual(environment.value("test"), 5)
    self.assertRaises(Utils.UnknownVariable, environment.setVariable, "test2", 5)
  def test_chain_environment(self):
    root_environment  = Environment()
    child_environment = Environment(root_environment)
    
    root_environment.defineVariable("test", 5)
    self.assertEqual(root_environment.value("test"), 5)
    self.assertEqual(child_environment.value("test"), 5)
    
    child_environment.setVariable("test", 2)
    self.assertEqual(root_environment.value("test"), 2)
    self.assertEqual(child_environment.value("test"), 2)
    
    child_environment.defineVariable("test", 3)
    self.assertEqual(root_environment.value("test"), 2)
    self.assertEqual(child_environment.value("test"), 3)
    
    child_environment.setVariable("test", 6)
    self.assertEqual(root_environment.value("test"), 2)
    self.assertEqual(child_environment.value("test"), 6)
    
    child_environment.defineVariable("test2", 4)    
    self.assertRaises(Utils.UnknownVariable, root_environment.value, "test2")
    self.assertEqual(child_environment.value("test2"), 4)

    self.assertRaises(Utils.UnknownVariable, root_environment.setVariable, "test2", 5)

if __name__ == '__main__':
  unittest.main()
