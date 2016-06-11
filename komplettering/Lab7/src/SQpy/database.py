import operator
from collections import namedtuple
from .ast import token, ast

class database(object):
  def __init__(self):
    self._tables = {}
    self._table_classes = {}
    self._count = 0
    self._total = 0
    self._total_count = 0
    self._aggregate = False


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
        lambda q: self.select(q),
      token.star:
        lambda _: lambda _: True,
      token.op_divide:
        lambda q: self.row_op(q.operands, operator.truediv),
      token.fn_count:
        lambda q: self.fn_count(q.field),
      token.fn_avg:
        lambda q: self.fn_avg(q.field),
      token.inner_join:
        lambda q: self.inner_join(q.table, q.on)
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
    def f(row, row2=None):
      op0 = self.execute_or_literal(operands[0], row)
      if row2:
        op1 = self.execute_or_literal(operands[1], row2)
      else:
        op1 = self.execute_or_literal(operands[1], row)
      return comparator(op0, op1)
    return f


  def identifier(self, identifier):
    def f(row):
      if len(identifier) == 1:
        return getattr(row, identifier[0])
      elif isinstance(row, tuple):
        return getattr(row, identifier[1])
      else:
        if identifier[0] in row:
            return getattr(row[identifier[0]], identifier[1])
        else:
            return None
    return f


  def update(self, table, set, where):
    wanted = filter(self.execute(where), self._tables[table])
    for row in wanted:
      index = self._tables[table].index(row)
      for key, value in set:
        row = row._replace(**{key: value})
      self._tables[table][index] = row


  def select(self, q):
    # Related to the uglyness that is fn_count.
    self._count = 0
    self._total_count = 0

    columns = q.columns
    table = q.from_table
    # First filter rows
    if hasattr(q, "where"):
      where = q.where
    else:
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
        if hasattr(q, "joins"):
            row = {table : row}
            row = [row]
            for join in q.joins:
                row = self.execute(join)(row)
        if isinstance(row, list) and row is not None:
            for value in row:
                if value is None:
                    continue
                subqueries = {key: func(value) for key, func in resultFuncs.items()}
                result.append(temp_class(**subqueries))
        elif not isinstance(row, dict):
          straight_rows = row._get(columns)
          subqueries = {key: func(row) for key, func in resultFuncs.items()}
          result.append(temp_class(**merge_dicts(straight_rows, subqueries)))
        else:
          subqueries = {key: func(row) for key, func in resultFuncs.items()}
          result.append(temp_class(**subqueries))
      if self._aggregate:
        self._aggregate = False
        wanted = [result[-1]]
      else:
        wanted = result

    return wanted


  def fn_count(self, field):
    self._aggregate = True
    # Now this is both ugly and bad.
    def f(row):
      if field in row._asdict():
        self._count += 1
      return self._count
    return f


  def fn_avg(self, field):
    self._aggregate = True
    # The same goes for this function.
    def f(row):
      if field in row._asdict():
        self._total_count += 1
        self._total += row._asdict()[field]
      return self._total / self._total_count
    return f


  def inner_join(self, table, on):
    def f(original_rows):
      retval = []
      for original_row in original_rows:
        for added_row in self._tables[table]:
          new_row = None
          if original_row is None:
            continue
          if self.execute(on)(original_row,added_row):
            new_row = {table:added_row , **original_row}
          elif not on.operands[0].identifier[0] in original_row:
            # Try to swap the identifiers, due to backwards input.
            id_zero = on.operands[0].identifier[0]
            id_one = on.operands[0].identifier[1]
            on.operands[0].identifier[0] = on.operands[1].identifier[0]
            on.operands[0].identifier[1] = on.operands[1].identifier[1]
            on.operands[1].identifier[0] = id_zero
            on.operands[1].identifier[1] = id_one
            if self.execute(on)(original_row,added_row):
              new_row = {table: added_row, **original_row}
            # Swap back.
            id_zero = on.operands[0].identifier[0]
            id_one = on.operands[0].identifier[1]
            on.operands[0].identifier[0] = on.operands[1].identifier[0]
            on.operands[0].identifier[1] = on.operands[1].identifier[1]
            on.operands[1].identifier[0] = id_zero
            on.operands[1].identifier[1] = id_one
          retval.append(new_row)
      return retval
    return f


def _get(self, columns):
  retval = {}
  for key, value in self._asdict().items():
    if key in columns:
      retval[key] = value
  return retval


def merge_dicts(a, b):
  retval = a.copy()
  retval.update(b)
  return retval
