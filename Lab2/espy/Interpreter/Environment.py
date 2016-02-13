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
        pass



    def defineVariable(self, name, init = None):
        """
        Create a new variable with the name "name" and the initial value
        "init".
        """        
        self.var_dictionary[name] = init        
        pass



    def setVariable(self, name, value):
        """
        Set the value of a variable. If the variable is not defined in
        this environment, it should look in the parent environment.
        If it is not found in the root environment, it should raise the
        exception Utils.UnknownVariable.
        """
        for key in self.var_dictionary:
            if (key == name):
                self.var_dictionary[name] = value
                return
            else:
                pass #Nothing
        if (self.parent == None):
            pass
        else:
            for key in self.parent.var_dictionary:
                if (key == name):
                    self.parent.var_dictionary[name] = value
                    return
                else:
                    pass #Nothing
        raise UnknownVariable(name)

    def value(self, name):
        """
        Get the value of a variable. If the variable is not defined in
        this environment, it should look in the parent environment.
        If it is not found in the root environment, it should raise the
        exception Utils.UnknownVariable.
        """
        for key in self.var_dictionary:
            if (key == name):                
                return self.var_dictionary.get(name)
            else:
                pass #Nothing
        if (self.parent == None):
            pass
        else:
            for key in self.parent.var_dictionary:
                if (key == name):                    
                    return self.parent.var_dictionary.get(name)
                else:
                    pass #Nothing
        raise UnknownVariable(name)




