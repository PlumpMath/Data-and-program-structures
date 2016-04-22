from Interpreter.Environment import Environment

class Function:
  '''
  This class represent a JavaScript function. It is a callable python object.

  It can be used like this:
  f = Function(["arg1", "arg2"], Environment(), lambda env: print(env.value("arg1") + env.value("arg2")))
  f(1,2)

  And it should print 3.

  An other example of use would be:
  f = Function(["arg1", "arg2"], Environment(), lambda env: raise ControlExceptions.ReturnException(print(env.value("arg1") + env.value("arg2"))))
  print(f(None,1,2))

  And it should also print 3.

  '''
  def __init__(self, args, environment, body):
    '''
    This creates a new function with a set of args (which is an array of string with the name of the variables used as arguments), the global environment
    used when defining the function and a lambda function defining the body to be called (should take one single argument, which is the environment)
    '''

    self.parent = environment
    self.argNames = args; # argNames contain a list of the names of the arguments
    self.body = body


  def call(self, that, this, *args):
    '''
    Call the function. This function is usefull since in ECMAScript, a function is an object and it can be called with the function "call". For instance:

    function MyFunction(arg)
    {
      console.log(arg)
    }
    MyFunction.call(2)

    In which case, that is a pointer to MyFunction and this to None. But where it becomes tricky is with:

    var obj = { member: function(arg) { this.value = arg } }
    obj.call(2)

    In which case that contains obj.member and this contains obj.

    In practice, the that argument can be ignored.

    In other word:
    * that is the pointer to the object of the function
    * this is the pointer to the object (equivalent of self in python)
    * args is the list of arguments passed to the function
    '''
    if that != None:
      self.environment.setVariable("that", that)
    self.__call__(this, *args)


  def __call__(self, this, *args):
    '''
    Call the function. With the this argument.

    step by step:
    create function-environment with correct parent in the local scope
    create pointer to self (this)
    zip argument names from function initiation with argument values
    set all environment variables with its values
    return function-body(function-arguments) == return f(x)
    '''
    localEnvironment = Environment(self.parent)
    localEnvironment.defineVariable("this", this)
    argValuePairs = zip(self.argNames, args)
    for name, value in argValuePairs:
      localEnvironment.defineVariable(name, value)

    return self.body(localEnvironment)
