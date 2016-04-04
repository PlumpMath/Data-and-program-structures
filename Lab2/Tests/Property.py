#!/usr/bin/env python3

import unittest
from Interpreter.Property import Property, ReadOnlyException, WriteOnlyException

class Obj:
  pass

class TestProperty(unittest.TestCase):
  def test_property(self):
    this = Obj()
    prop = Property(this)
    
    # No setter and no getter has been set, this should raise exception
    self.assertRaises(WriteOnlyException, prop.get)
    self.assertRaises(ReadOnlyException, prop.set, 2)
    
    # Set a value on the this object
    setattr(this, "val", 2)
    
    # Add the getter and setter
    prop.getter = lambda this: getattr(this, "val") + 1
    prop.setter = lambda this, val: setattr(this, "val", val - 1)
    
    # Check that the get function is working
    self.assertEqual(prop.get(), 3)

    # Check that the set function is working
    prop.set(4)
    self.assertEqual(prop.get(), 4)
    self.assertEqual(getattr(this, "val"), 3)
    
    # Check that the clone function is working
    prop2 = prop.clone()
    self.assertEqual(prop2.get(), 4)
    this2 = Obj()
    setattr(this2, "val", 4)
    prop2.this = this2
    self.assertEqual(prop.get(), 4)
    self.assertEqual(prop2.get(), 5)
    prop2.set(3)
    self.assertEqual(prop.get(), 4)
    self.assertEqual(prop2.get(), 3)
    
  def test_property_merge(self):
    # Check that the merge function is working
    this = Obj()
    prop  = Property(this)
    prop2 = Property(this)
    
    setattr(this, "val", 2)
    prop.getter = lambda this: getattr(this, "val") + 1
    prop2.setter = lambda this, val: setattr(this, "val", val - 1)

    self.assertEqual(prop.get(), 3)
    prop2.set(4)
    self.assertEqual(prop.get(), 4)
    self.assertEqual(getattr(this, "val"), 3)
    
    prop.merge(prop2)
    prop.set(3)
    self.assertEqual(prop.get(), 3)
    self.assertEqual(getattr(this, "val"), 2)
    
if __name__ == '__main__':
  unittest.main()
