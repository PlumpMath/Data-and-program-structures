from Utils import UnknownVariable

class Environment:
  """
  Environment class used to define variables.
  """
  def __init__(self, parent = None):
    """
    Initialise an environment. The parent is an other environment
    where value for variables can be looked up recursively.
    """
    class Container:
      pass
    self.parent = parent
    self.environment = Container

  def defineVariable(self, name, init = None):
    """
    Create a new variable with the name "name" and the initial value
    "init".
    """
    return setattr(self.environment, name, init)

  def setVariable(self, name, value):
    """
    Set the value of a variable. If the variable is not defined in
    this environment, it should look in the parent environment.
    If it is not found in the root environment, it should raise the
    exception Utils.UnknownVariable.
    """
    if hasattr(self.environment, name):
      return setattr(self.environment, name, value)
    elif hasattr(self, "parent") and self.parent is not None:
      return self.parent.setVariable(name, value)
    else:
       raise UnknownVariable(name)

  def value(self, name):
    """
    Get the value of a variable. If the variable is not defined in
    this environment, it should look in the parent environment.
    If it is not found in the root environment, it should raise the
    exception Utils.UnknownVariable.
    """
    if hasattr(self.environment, name):
      return getattr(self.environment, name)
    elif hasattr(self, "parent") and self.parent is not None:
      return self.parent.value(name)
    else:
      raise UnknownVariable(name)
