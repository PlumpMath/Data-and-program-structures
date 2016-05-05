from Interpreter.Property import Property

class Object:
  def __init__(self):
      pass

class ObjectModule:
  def __init__(self):
    self.prototype = Object()

  def __call__(self, this, *args):
    pass

  def create(self, this, prototype):
    obj = Object()
    for attr in dir(prototype):
      if not attr.startswith("__"):
        val = getattr(prototype, attr)
        if isinstance(val, tuple):
          val = list(val)
          val[0] = obj
          val = (val[0], val[1])
        if isinstance(val, Property):
          val = val.clone()
          val.this = obj
        setattr(obj, attr, val)
    return obj

  def defineProperty(self, this, obj, name, param):
    prop = Property(this)
    if(hasattr(param, 'get')):
      prop.getter = param.get
    if(hasattr(param, 'set')):
      prop.setter = param.set
    setattr(obj, name, prop)
