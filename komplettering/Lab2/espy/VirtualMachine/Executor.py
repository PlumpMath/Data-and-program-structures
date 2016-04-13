from VirtualMachine.Stack import Stack
from VirtualMachine.OpCode import OpCode

class Executor:
  '''
  Execute the code of a program or function
  '''
  def __init__(self, environment = Environment()):
    self.environment = environment
    self.stack  = Stack()

    # The following code acts as a switch statements for OpCodes
    self.opmaps  = {}
    # Stack
    self.opmaps[OpCode.PUSH] = Executor.execute_push
    self.opmaps[OpCode.POP] = Executor.execute_pop    
    # ...

    # Environment and objects manipulation
    # Control
    # Exceptions
    # Array and Objects creation
    # Binary arithmetic operation
    # Binary bolean operation
    # Unary operations
   
    
  
  def execute(self, program):
    '''
    Execute the program given in argument
    '''
    
    # You might have to modify this later.
    for inst in program.instructions:
      inst = program.instructions[self.current_index]
      f = self.opmaps[inst.opcode]
      
      f(self, *inst.params)

  def execute_push(self, value):
    '''
    Execute the PUSH instruction
    '''
    pass
  
  def execute_pop(self, count):
    '''
    Execute the POP instruction
    '''
    pass