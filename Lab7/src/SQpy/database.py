import operator
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
        lambda q: self.row_op(q.operands, operator.eq),
      token.op_inferior:
        lambda q: self.row_op(q.operands, operator.lt),
      token.op_superior:
        lambda q: self.row_op(q.operands, operator.gt),
      token.identifier:
        lambda q: self.identifier(q.identifier),
      token.update:
        lambda q: self.update(q.table, q.set, q.where),
      token.select:
        lambda q: self.select(q.columns, q.from_table),
      token.star:
        lambda _: lambda _: True,
      token.op_divide:
        lambda q: self.row_op(q.operands, operator.truediv)
    }[query.token](query)


  def execute_or_literal(self, node, row):
    if isinstance(node, ast):
      return self.execute(node)(row)
    else:
      return node


  def create_table(self, name, columns):
    self._table_classes[name] = namedtuple(name + '_row', columns)
    self._table_classes[name].__new__.__defaults__ = \
        (None,) * len(self._table_classes[name]._fields)
    self._table_classes[name]._get = _get
    self._tables[name] = []


  def insert_into(self, query):
    columns = self.fields(query.table)
    row = self._table_classes[query.table](*query.values)
    self._tables[query.table].append(row)


  def delete_from(self, table, where):
    unwanted = filter(self.execute(where), self._tables[table])
    for row in unwanted:
      self._tables[table].remove(row)


  def op_and(self, operands):
    def f(row):
      for operand in operands:
        if not self.execute(operand)(row):
          return False
      return True
    return f


  def row_op(self, operands, comparator):
    def f(row):
      op0 = self.execute_or_literal(operands[0], row)
      op1 = self.execute_or_literal(operands[1], row)
      return comparator(op0, op1)
    return f


  def identifier(self, identifiers):
    def f(row):
      # Remove [0] in case of multiple identifiers in the list.
      # Then add code in op_equal and it's brethren to
      # manage the list comparisons.
      return [getattr(row, key) for key in identifiers][0]
    return f


  def update(self, table, set, where):
    wanted = filter(self.execute(where), self._tables[table])
    for row in wanted:
      index = self._tables[table].index(row)
      for key, value in set:
        row = row._replace(**{key: value})
      self._tables[table][index] = row


  def select(self, columns, table, where=None):
    # First filter rows
    if where is None:
      where = ast.star()
    wanted = filter(self.execute(where), self._tables[table])

    # Then filter columns and execute subqueries.
    if isinstance(columns, ast):
      pass
    else:
      resultFuncs = {}
      for i, column in enumerate(columns):
        if isinstance(column, tuple):
          operation, name = column
          resultFuncs[name] = self.execute(operation)
          columns[i] = name

      temp_class = namedtuple('select_row', columns)
      result = []
      for row in wanted:
        straight_rows = row._get(columns)
        subqueries = {key: func(row) for key, func in resultFuncs.items()}
        result.append(temp_class(**{**straight_rows, **subqueries}))
      wanted = result

    return wanted


def _get(self, columns):
  retval = {}
  for key, value in self._asdict().items():
    if key in columns:
      retval[key] = value
  return retval
