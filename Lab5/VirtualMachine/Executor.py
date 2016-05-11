from Interpreter.Environment import Environment
from VirtualMachine.Stack import Stack
from VirtualMachine.OpCode import OpCode

class Executor:
  '''
  Execute the code of a program or function
  '''
  def __init__(self, environment = Environment()):
    self.environment = environment
    self.stack  = Stack()
    self.program_counter = 0

    # The following code acts as a switch statements for OpCodes
    self.opmaps  = {}

    # Stack Manipulation
    self.opmaps[OpCode.NOP] = Executor.execute_NOP
    self.opmaps[OpCode.PUSH] = Executor.execute_PUSH
    self.opmaps[OpCode.POP] = Executor.execute_POP
    self.opmaps[OpCode.DUP] = Executor.execute_DUP
    self.opmaps[OpCode.SWAP] = Executor.execute_SWAP

    # Environment and objects manipulation
    self.opmaps[OpCode.LOAD] = Executor.execute_LOAD
    self.opmaps[OpCode.STORE] = Executor.execute_STORE
    self.opmaps[OpCode.DCL] = Executor.execute_DCL
    self.opmaps[OpCode.LOAD_MEMBER] = Executor.execute_LOAD_MEMBER
    self.opmaps[OpCode.STORE_MEMBER] = Executor.execute_STORE_MEMBER
    self.opmaps[OpCode.LOAD_INDEX] = Executor.execute_LOAD_INDEX
    self.opmaps[OpCode.STORE_INDEX] = Executor.execute_STORE_INDEX

    # Control
    self.opmaps[OpCode.JMP] = Executor.execute_JMP
    self.opmaps[OpCode.IFJMP] = Executor.execute_IFJMP
    self.opmaps[OpCode.UNLESSJMP] = Executor.execute_UNLESSJMP
    self.opmaps[OpCode.CALL] = Executor.execute_CALL
    self.opmaps[OpCode.NEW] = Executor.execute_NEW
    self.opmaps[OpCode.RET] = Executor.execute_RET
    self.opmaps[OpCode.SWITCH] = Executor.execute_SWITCH

    # Exceptions
    self.opmaps[OpCode.TRY_PUSH] = Executor.execute_TRY_PUSH
    self.opmaps[OpCode.TRY_POP] = Executor.execute_TRY_POP
    self.opmaps[OpCode.THROW] = Executor.execute_THROW

    # Array and Objects creation
    self.opmaps[OpCode.MAKE_ARRAY] = Executor.execute_MAKE_ARRAY
    self.opmaps[OpCode.MAKE_OBJECT] = Executor.execute_MAKE_OBJECT
    self.opmaps[OpCode.MAKE_FUNC] = Executor.execute_MAKE_FUNC
    self.opmaps[OpCode.MAKE_GETTER] = Executor.execute_MAKE_GETTER
    self.opmaps[OpCode.MAKE_SETTER] = Executor.execute_MAKE_SETTER

    # Binary arithmetic operation
    self.opmaps[OpCode.ADD] = Executor.execute_ADD
    self.opmaps[OpCode.MUL] = Executor.execute_MUL
    self.opmaps[OpCode.SUB] = Executor.execute_SUB
    self.opmaps[OpCode.DIV] = Executor.execute_DIV
    self.opmaps[OpCode.MOD] = Executor.execute_MOD
    self.opmaps[OpCode.LEFT_SHIFT] = Executor.execute_LEFT_SHIFT
    self.opmaps[OpCode.RIGHT_SHIFT] = Executor.execute_RIGHT_SHIFT
    self.opmaps[OpCode.UNSIGNED_RIGHT_SHIFT] = Executor.execute_UNSIGNED_RIGHT_SHIFT

    # Binary bolean operation
    self.opmaps[OpCode.SUPPERIOR] = Executor.execute_SUPPERIOR
    self.opmaps[OpCode.SUPPERIOR_EQUAL] = Executor.execute_SUPPERIOR_EQUAL
    self.opmaps[OpCode.INFERIOR] = Executor.execute_INFERIOR
    self.opmaps[OpCode.INFERIOR_EQUAL] = Executor.execute_INFERIOR_EQUAL
    self.opmaps[OpCode.EQUAL] = Executor.execute_EQUAL
    self.opmaps[OpCode.DIFFERENT] = Executor.execute_DIFFERENT
    self.opmaps[OpCode.AND] = Executor.execute_AND
    self.opmaps[OpCode.OR] = Executor.execute_OR

    # Unary operations
    self.opmaps[OpCode.NEG] = Executor.execute_NEG
    self.opmaps[OpCode.TILDE] = Executor.execute_TILDE
    self.opmaps[OpCode.NOT] = Executor.execute_NOT


  def execute(self, program):
    ''' Execute the program given in argument. '''
    # You might have to modify this later.
    program_length = len(program.instructions)
    while self.program_counter < program_length:
      instruction = program.instructions[self.program_counter]
      f = self.opmaps[instruction.opcode]
      self.program_counter += 1
      f(self, *instruction.params)



  # Stack Manipulation
  def execute_NOP(self):
    pass

  def execute_PUSH(self, value):
    self.stack.push(value)

  def execute_POP(self, count):
    for x in range(0, count):
      self.stack.pop()

  def execute_DUP(self):
    self.stack.dup()

  def execute_SWAP(self):
    self.stack.swap()


  # Environment and objects manipulation
  def execute_LOAD(self, name):
    self.stack.push(self.environment.value(name))

  def execute_STORE(self, name):
    self.environment.setVariable(name, self.stack.peek())

  def execute_DCL(self, name):
    self.environment.defineVariable(name)

  def execute_LOAD_MEMBER(self, index):
    obj = self.stack.pop()
    if type(obj) == list:
      if index == 'length':
        value = len(obj)
      else:
        value = obj[int(index)]
    else:
      value = getattr(obj, index)
    self.stack.push(value)

  def execute_STORE_MEMBER(self, index):
    obj = self.stack.pop()
    value = self.stack.peek()
    if type(obj) == list:
      obj[int(index)] = value
    else:
      setattr(obj, index, value)

  def execute_LOAD_INDEX(self):
    index = self.stack.pop()
    obj = self.stack.pop()
    if type(obj) == list:
      if index == 'length':
        value = len(obj)
      else:
        value = obj[int(index)]
    else:
      value = getattr(obj, str(index))
    self.stack.push(value)

  def execute_STORE_INDEX(self):
    index = self.stack.pop()
    obj = self.stack.pop()
    value = self.stack.pop()
    if type(obj) == list:
      obj[index] = value
    else:
      setattr(obj, index, value)
    self.stack.push(value)


    # Control
  def execute_JMP(self, position):
    self.program_counter = position

  def execute_IFJMP(self, position):
    if self.stack.pop():
      self.program_counter = position

  def execute_UNLESSJMP(self, position):
    if not self.stack.pop():
      self.program_counter = position

  def execute_CALL(self):
    pass

  def execute_NEW(self):
    pass
  def execute_RET(self):
    pass
  def execute_SWITCH(self):
    pass

    # Exceptions
  def execute_TRY_PUSH(self):
    pass
  def execute_TRY_POP(self):
    pass
  def execute_THROW(self):
    pass

    # Array and Objects creation
  def execute_MAKE_ARRAY(self):
    pass
  def execute_MAKE_OBJECT(self):
    pass
  def execute_MAKE_FUNC(self):
    pass
  def execute_MAKE_GETTER(self):
    pass
  def execute_MAKE_SETTER(self):
    pass

    # Binary arithmetic operation
  def execute_ADD(self):
    pass
  def execute_MUL(self):
    pass
  def execute_SUB(self):
    pass
  def execute_DIV(self):
    pass
  def execute_MOD(self):
    pass
  def execute_LEFT_SHIFT(self):
    pass
  def execute_RIGHT_SHIFT(self):
    pass
  def execute_UNSIGNED_RIGHT_SHIFT(self):
    pass

    # Binary bolean operation
  def execute_SUPPERIOR(self):
    pass
  def execute_SUPPERIOR_EQUAL(self):
    pass
  def execute_INFERIOR(self):
    pass
  def execute_INFERIOR_EQUAL(self):
    pass
  def execute_EQUAL(self):
    pass
  def execute_DIFFERENT(self):
    pass
  def execute_AND(self):
    pass
  def execute_OR(self):
    pass

    # Unary operations
  def execute_NEG(self):
    pass
  def execute_TILDE(self):
    pass
  def execute_NOT(self):
    pass
