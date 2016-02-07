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
    pass

  def defineVariable(self, name, init = None):
    """
    Create a new variable with the name "name" and the initial value
    "init".
    """
    pass

  def setVariable(self, name, value):
    """
    Set the value of a variable. If the variable is not defined in
    this environment, it should look in the parent environment.
    If it is not found in the root environment, it should raise the
    exception Utils.UnknownVariable.
    """
    pass

  def value(self, name):
    """
    Get the value of a variable. If the variable is not defined in
    this environment, it should look in the parent environment.
    If it is not found in the root environment, it should raise the
    exception Utils.UnknownVariable.
    """
    pass