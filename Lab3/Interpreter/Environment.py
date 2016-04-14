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
        self.parent = parent
        self.var_dictionary = {}



    def defineVariable(self, name, init = None):
        """
        Create a new variable with the name "name" and the initial value
        "init".
        """
        self.var_dictionary[name] = init


    def setVariable(self, name, value):
        """
        Set the value of a variable. If the variable is not defined in
        this environment, it should look in the parent environment.
        If it is not found in the root environment, it should raise the
        exception Utils.UnknownVariable.
        """
        if name in self.var_dictionary:
            self.var_dictionary[name] = value
        elif self.parent:
            self.parent.setVariable(name, value)
        else:
            raise UnknownVariable(name)


    def value(self, name):
        """
        Get the value of a variable. If the variable is not defined in
        this environment, it should look in the parent environment.
        If it is not found in the root environment, it should raise the
        exception Utils.UnknownVariable.
        """
        if name in self.var_dictionary:
            return self.var_dictionary[name]
        elif self.parent:
            return self.parent.value(name)
        else:
            raise UnknownVariable(name)


    def exists (self, name):
        """
        Find if a variable is defined or not.

        Returns True/False
        """
        if name in self.var_dictionary:
            return True
        elif self.parent:
            return self.parent.exists(name)
        else:
            return False


    def defineGlobal(self, name):
        """
        Defines a variable in the global scope
        Ref: http://stackoverflow.com/questions/1470488/what-is-the-function-of-the-var-keyword-and-when-to-use-it-or-omit-it
        """
        if self.parent:
            self.parent.defineGlobal(name)
        else:
            self.defineVariable(name)
