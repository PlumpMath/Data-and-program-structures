from VirtualMachine.OpCode import OpCode

class Instruction:
  '''
  Represent a single instruction with its given OpCode and its parameters
  '''
  def __init__(self, opcode: OpCode, *params):
    self.opcode = opcode
    self.params = list(params)


  def __str__(self):
    return str("OpCode: " + self.opcode.name + "Params: " + str(self.params))
