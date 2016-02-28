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


# ---------------------
    for i in args:
        environment.defineVariable(i); # must be defined in environment so a value can be added in __call__.



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

    self.__call__(self, this, *args)
    '''
    Problem analys:
    
    Test delen som skapar error är följande
    def func2(self, env):
        self.assertEqual(env.value("this"), 10)
        self.assertEqual(env.value("arg1"), 2)
        self.assertEqual(env.value("arg2"), 5)


    env  = Environment()
    function = Function(["arg1", "arg2"], env, lambda environment: self.func2(environment))
    function(10, 2, 5)
    function.call(None, 10, 2, 5)


    function(10, 2, 5) säger att this: 10 args: (2,5) vilket är rätt.
    medan
    function.call(None, 10, 2, 5) säger att this är ett Function object. vilket är fel

    Min output säger för funcion respektive .call:

    this: 10 args:  (2, 5)
    ['arg1', 'arg2'] (2, 5)
    this: <Interpreter.Function.Function object at 0x7f07ccbebf28> args:  (10, 2, 5)
    ['arg1', 'arg2'] (10, 2, 5)
    more args then argNames



    Traceback output:
    AssertionError: <Interpreter.Function.Function object at 0x7f07ccbebf28> != 10



    Detta betyder att om funktionen kallas direkt har vi ett beteende och gör vi ett call har vi ett annat?

    vi vet också från problem beskrivningen att

    "this is the pointer to the object (equivalent of self in python)"
    vilket jag skulle säga stämmer för .call men inte för function. vilket gör detta ännu mer invecklat då det är function som beter sig så som de verkar förvänta sig.

    '''


  def __call__(self, this, *args):
    '''
    Call the function. With the this argument.
    '''

    print(self.argNames, args)
    self.environment = Environment(self.parent)
    self.environment.defineVariable("this", this)
    numberofNone = 0 # Handle extra None-arguments
    strangeTHIS = 0  # if call-function we need to handle it
    for count, value in enumerate(args):
      if (value == None):
        numberofNone += 1                 # ??
      elif (count > ((len(self.argNames) + numberofNone) -1 + strangeTHIS)):
        pass  
      else:
        if((this == self) and (strangeTHIS == 0)):
            self.environment.setVariable("this", value)
            strangeTHIS = -1
        else:  
            self.environment.setVariable(self.argNames[count - numberofNone], value) 
            #fails if variable isn't defined in init. It could probably also be done by defining the variable here(?)
    return self.body(self.environment)
