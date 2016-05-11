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
      print("Template:", dir(template_ast.body[0].args))
      template_ast.body[0].args = args

      name_func_pairs = dict(zip(decorator_args[0::2], decorator_args[1::2]))
      print(name_func_pairs)
      class T(ast.NodeTransformer):
        def visit_Expr(self, node):
          print("We're here", node.value.id)
          if node.value.id in name_func_pairs:
            print("node.value.id", node.value.id)
            print("Something:", inspect.getsource(name_func_pairs[node.value.id]))
            print("What we return:", dir(ast.parse(inspect.getsource(name_func_pairs[node.value.id])).body[0].body[0]))
            print("What we return:", ast.parse(inspect.getsource(name_func_pairs[node.value.id])).body[0].body[0])

            return ast.parse(inspect.getsource(name_func_pairs[node.value.id])).body[0].body[0]
          else:
            return node

      print("Template_ast.body[0].name", template_ast.body[0].name)
      print("CodeObject:", compile(T().visit(template_ast), __file__, mode='exec').co_consts)
      exec(compile(T().visit(template_ast), __file__, mode='exec'))
      return locals()[template_ast.body[0].name]
    return decorator
  return make_decorator
