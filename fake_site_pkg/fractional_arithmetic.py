"""Converts integers literals into instances of the Fraction class.
   This works for doing using Python exclusively to do integer arithmetics but it
   fails miserably in other contexts.  For exemple::

        for i in range(3):
            ...
   gets converted to

        for i in range(Fraction(3)):
            ...

   which fails. It is only meant as a demo of AST transformations.
   """
import ast


class FractionWrapper(ast.NodeTransformer):
    """Wraps all integers in a call to Integer()"""
    def visit_Num(self, node):
        if isinstance(node.n, int):
            return ast.Call(func=ast.Name(id='Fraction', ctx=ast.Load()),
                            args=[node], keywords=[])
        return node


def transform_ast(tree):
    tree = FractionWrapper().visit(tree)
    ast.fix_missing_locations(tree)
    return tree


def add_import():
    return "from fractions import Fraction\n"
