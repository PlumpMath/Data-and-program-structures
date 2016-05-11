import Utils

class ReadOnlyException(Exception):
  '''
  Exception thrown when accessing a read only property
  '''
  def __init__(self):
    pass

class WriteOnlyException(Exception):
  '''
  Exception thrown when accessing a write only property
  '''
  def __init__(self):
    pass

class Property:
  '''
  Define an ECMAScript style property. This should contains three members:
  * getter a Function that is called when accessing the value
  * setter a Function that is called when setting the value
  * this the object to which this property belongs
  '''
  def __init__(self):
    pass

  def __init__(self, obj):
    self.this = obj

  def get(self):
    '''
    Get the value or raise WriteOnlyException
    '''
    if (hasattr(self, "getter")):
      return self.getter(self.this)
    else:
      raise WriteOnlyException()

  def set(self, value):
    '''
    Set the value or raise ReadOnlyException
    '''
    if (hasattr(self, "setter")):
      return self.setter(self.this, value)
    else:
      raise ReadOnlyException()

  def merge(self, other):
    '''
    Merge two properties.
    '''
    if not hasattr(self, "setter"):
      if hasattr(other, "setter"):
        setattr(self, "setter", other.setter)

    if not hasattr(self, "getter"):
      if hasattr(other, "getter"):
        setattr(self, "getter", other.getter)

  def clone(self):
    '''
    Clone a property (useful when creating new objects).
    '''
    if hasattr(self, "this"):
      p = Property(self.this)
    else:
      p = Property()

    if hasattr(self, "setter"):
      p.setter = self.setter
    if hasattr(self, "getter"):
      p.getter = self.getter

    return p
