import ast
import inspect
from functools import wraps

#Trevlig bok(?) som går igenom bland annat python decorators.
#Länk: http://python-3-patterns-idioms-test.readthedocs.io/en/latest/PythonDecorators.html#the-goal-of-macros


def apply_template(*decorator_args):
  def make_decorator(template):
    @wraps(template)
    def decorator(*args):
      template_ast = ast.parse(inspect.getsource(template))
      template_ast.body[0].decorator_list = []
      name_func_pairs = dict(zip(decorator_args[0::2], decorator_args[1::2]))
      class T(ast.NodeTransformer):
        def visit_Expr(self, node):
          if node.value.id in name_func_pairs:
            source = inspect.getsource(name_func_pairs[node.value.id])
            return ast.parse(source).body[0].body
          else:
            return node

      exec(compile(T().visit(template_ast), __file__, mode='exec'))
      return locals()[template_ast.body[0].name](*args)
    return decorator
  return make_decorator
