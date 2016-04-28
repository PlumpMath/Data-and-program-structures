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
      val = getattr(prototype, attr)
      if not attr.startswith("__"):
        if(isinstance(val, tuple)):
          val = list(val)
          val[0] = obj
          val = (val[0], val[1])
        setattr(obj, attr, val)
    return obj

  def defineProperty(self, this, obj, name, param):
    prop = Property(self)
    if(hasattr(param, 'getter')):
      prop.getter = param.getter
    if(hasattr(param, 'setter')):
      prop.setter = param.setter
    setattr(obj, name, prop)
