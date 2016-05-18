from collections import namedtuple
from .ast import token, ast

class database(object):
  def __init__(self):
    self._tables = {}
    self._table_classes = {}


  def tables(self):
    return list(self._tables.keys())


  def fields(self, name):
    return list(self._table_classes[name]._fields)


  def dump_table(self, name):
    return self._tables[name]


  def execute(self, query):
    return {
      token.create_table:
        lambda q: self.create_table(q.name, q.columns),
      token.insert_into:
        self.insert_into,
      token.delete_from:
        lambda q: self.delete_from(q.table, q.where),
      token.op_and:
        lambda q: self.op_and(q.operands),
      token.op_equal:
        lambda q: self.op_equal(q.operands)
    }[query.token](query)


  def create_table(self, name, columns):
    self._table_classes[name] = namedtuple(name + '_table', columns)
    self._table_classes[name].__new__.__defaults__ = (None,) * len(self._table_classes[name]._fields)
    self._tables[name] = []


  def insert_into(self, query):
    columns = self.fields(query.table)
    row = self._table_classes[query.table](*query.values)
    self._tables[query.table].append(row)


  def delete_from(self, table, where):
    self._tables[table] = self._tables[table] -\
                          list(filter(self.execute(where), self._tables[table]))


  def op_and(self, operands):
    def f(row):
      for operand in operands:
        if not self.execute(operand)(row):
          return False
      return True
    return f


  def op_equal(self, operands):
    print("Operands:", operands)
    def f(row):
      print("Row:", row)
      op0 = execute_or_literal(self, operands[0], row)
      op1 = execute_or_literal(self, operands[1], row)
      return op0 == op1
    return f


  def execute_or_literal(self, node, row):
    if isinstance(node, ast):
      return node(row)
    else:
      return node
