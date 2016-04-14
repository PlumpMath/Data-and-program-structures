import inspect
import operator

import antlr4
import Utils

from ECMAScriptParser import ECMAScriptVisitor

from Interpreter.Console import Console
from Interpreter.Math import MathModule
from Interpreter.Environment import Environment
from Interpreter.Object import Object, ObjectModule


class InterpreterVisitor(ECMAScriptVisitor):

    def __init__(self, environment = Environment(), input=None):
        self.environment = environment
        self.environment.defineVariable("console", Console())
        self.environment.defineVariable("Math", MathModule())
        self.environment.defineVariable("Object", ObjectModule())
        self.binaries = { '+': operator.add, '-': operator.sub,
                          '*': operator.mul, '/': operator.truediv,
                          '%': operator.mod,
                          '<<': lambda x, y: float(operator.lshift(int(x), int(y))),
                          '>>': lambda x, y: float(operator.rshift(int(x), int(y))),
                          '>>>': lambda x, y: float((int(x) % 0x100000000) >> int(y)),
                          '<': operator.lt, '>': operator.gt,
                          '<=': operator.le, '>=': operator.ge,
                          '==': operator.eq, '!=': operator.ne,
                          '===': lambda x, y: type(x) == type(y) and x == y,
                          '!==': lambda x, y: type(x) != type(y) or x != y,
                          '||': lambda x, y: x or y, '&&': lambda x, y: x and y }
        self.unaries = { '-': operator.neg, '+': operator.pos,
                         '~': lambda x: float(~int(x)), '!': operator.not_ }
        self.assignment = { '=': lambda x, y: y,
                            '+=': operator.iadd, '-=': operator.isub}

    def inspector(self, ctx):
        print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
        print("In function: ", inspect.stack()[1].function)
        print("_______________________")
        print("")
        print("Begin child list.")
        for child in ctx.children:
            val = child.accept(self)
            print(str(type(val)) + ": " + str(val))
        print("End child list of", inspect.stack()[1].function, "\t.!.")
        print("")


    def visitTerminal(self, node):
        if node.symbol.text == "true":
            return True
        elif node.symbol.text == "false":
            return False
        elif node.symbol.text[0] == '"':
            return node.symbol.text[1:-1]
        elif node.symbol.text[0:2] == "0x":
            return float.fromhex(node.symbol.text)
        else:
            return node.symbol.text


    # Visit a parse tree produced by ECMAScriptParser#PropertyExpressionAssignment.
    def visitPropertyExpressionAssignment(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#assignmentOperator.
    def visitAssignmentOperator(self, ctx):
        return ctx.children[0].accept(self)


    # Visit a parse tree produced by ECMAScriptParser#eos.
    def visitEos(self, ctx):
        return


    # Visit a parse tree produced by ECMAScriptParser#program.
    def visitProgram(self, ctx):
        self.visitChildren(ctx)


    # Visit a parse tree produced by ECMAScriptParser#argumentList.
    def visitArgumentList(self, ctx):
      args = []
      for c in ctx.children:
        if(not isinstance(c, antlr4.tree.Tree.TerminalNodeImpl)): # Skip ","
          args.append(c.accept(self))
      return args


    # Visit a parse tree produced by ECMAScriptParser#ArgumentsExpression.
    def visitArgumentsExpression(self, ctx):
        func = ctx.children[0].accept(self)
        args = ctx.children[1].accept(self)
        if(args == None): args = []
        return func(None, *args)


    # Visit a parse tree produced by ECMAScriptParser#ThisExpression.
    def visitThisExpression(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#identifierName.
    def visitIdentifierName(self, ctx):
        return ctx.children[0].accept(self)


    # Visit a parse tree produced by ECMAScriptParser#BinaryExpression.
    def visitBinaryExpression(self, ctx):
        arg1 = ctx.children[0].accept(self)
        operator = ctx.children[1].accept(self)
        arg2 = ctx.children[2].accept(self)
        return self.binaries[operator](arg1, arg2)


    # Visit a parse tree produced by ECMAScriptParser#futureReservedWord.
    def visitFutureReservedWord(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#initialiser.
    def visitInitialiser(self, ctx):
        return ctx.children[1].accept(self)


    # Visit a parse tree produced by ECMAScriptParser#statementList.
    def visitStatementList(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#PropertyGetter.
    def visitPropertyGetter(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#block.
    def visitBlock(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#expressionStatement.
    def visitExpressionStatement(self, ctx):
      self.visitChildren(ctx)


    # Visit a parse tree produced by ECMAScriptParser#keyword.
    def visitKeyword(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#elementList.
    def visitElementList(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#numericLiteral.
    def visitNumericLiteral(self, ctx):
        return float(self.visitChildren(ctx))


    # Visit a parse tree produced by ECMAScriptParser#ForInStatement.
    def visitForInStatement(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#emptyStatement.
    def visitEmptyStatement(self, ctx):
        return


    # Visit a parse tree produced by ECMAScriptParser#labelledStatement.
    def visitLabelledStatement(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#PropertySetter.
    def visitPropertySetter(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#NewExpression.
    def visitNewExpression(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#LiteralExpression.
    def visitLiteralExpression(self, ctx):
      return self.visitChildren(ctx)


    # Visit a parse tree produced by ECMAScriptParser#ArrayLiteralExpression.
    def visitArrayLiteralExpression(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#MemberDotExpression.
    def visitMemberDotExpression(self, ctx):
      obj    = ctx.children[0].accept(self)
      member = ctx.children[2].accept(self)
      return getattr(obj, member)


    # Visit a parse tree produced by ECMAScriptParser#withStatement.
    def visitWithStatement(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#MemberIndexExpression.
    def visitMemberIndexExpression(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#formalParameterList.
    def visitFormalParameterList(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#incrementOperator.
    def visitIncrementOperator(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#AssignmentOperatorExpression.
    def visitAssignmentOperatorExpression(self, ctx):
        self.inspector(ctx)
        name = ctx.children[0].accept(self)
        operator = ctx.children[1].accept(self)
        rhs = ctx.children[2].accept(self)

        if self.environment.exists(name):
            self.environment.defineGlobal(name)

        result = self.assignment[operator](name, rhs)
        self.environment.setVariable(name, result)


    # Visit a parse tree produced by ECMAScriptParser#PostUnaryAssignmentExpression.
    def visitPostUnaryAssignmentExpression(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#TernaryExpression.
    def visitTernaryExpression(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#tryStatement.
    def visitTryStatement(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#debuggerStatement.
    def visitDebuggerStatement(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#DoStatement.
    def visitDoStatement(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#ObjectLiteralExpression.
    def visitObjectLiteralExpression(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#arrayLiteral.
    def visitArrayLiteral(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#elision.
    def visitElision(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#statements.
    def visitStatements(self, ctx):
        self.visitChildren(ctx)


    # Visit a parse tree produced by ECMAScriptParser#UnaryExpression.
    def visitUnaryExpression(self, ctx):
        operator = ctx.children[0].accept(self)
        argument = ctx.children[1].accept(self)
        return self.unaries[operator](argument)


    # Visit a parse tree produced by ECMAScriptParser#WhileStatement.
    def visitWhileStatement(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#returnStatement.
    def visitReturnStatement(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#switchStatement.
    def visitSwitchStatement(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#expressionSequence.
    def visitExpressionSequence(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ECMAScriptParser#literal.
    def visitLiteral(self, ctx):
        return ctx.children[0].accept(self)


    # Visit a parse tree produced by ECMAScriptParser#variableStatement.
    def visitVariableStatement(self, ctx):
        self.visitChildren(ctx)


    # Visit a parse tree produced by ECMAScriptParser#FunctionExpression.
    def visitFunctionExpression(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#defaultClause.
    def visitDefaultClause(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#statement.
    def visitStatement(self, ctx):
        self.visitChildren(ctx)


    # Visit a parse tree produced by ECMAScriptParser#ForStatement.
    def visitForStatement(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#caseBlock.
    def visitCaseBlock(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#ParenthesizedExpression.
    def visitParenthesizedExpression(self, ctx):
        # Return what's between the parenthesis ( what ).
        return ctx.children[1].accept(self)


    # Visit a parse tree produced by ECMAScriptParser#objectLiteral.
    def visitObjectLiteral(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#throwStatement.
    def visitThrowStatement(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#breakStatement.
    def visitBreakStatement(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#ifStatement.
    def visitIfStatement(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#reservedWord.
    def visitReservedWord(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#variableDeclaration.
    def visitVariableDeclaration(self, ctx):
        self.inspector(ctx)
        name = ctx.children[0].accept(self)
        value = ctx.children[1].accept(self)
        self.environment.defineVariable(name, value)


    # Visit a parse tree produced by ECMAScriptParser#finallyProduction.
    def visitFinallyProduction(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#IdentifierExpression.
    def visitIdentifierExpression(self, ctx):
      return self.environment.value(ctx.children[0].accept(self))


    # Visit a parse tree produced by ECMAScriptParser#propertyName.
    def visitPropertyName(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#catchProduction.
    def visitCatchProduction(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#continueStatement.
    def visitContinueStatement(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#caseClause.
    def visitCaseClause(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#arguments.
    def visitArguments(self, ctx):
      return ctx.children[1].accept(self)


    # Visit a parse tree produced by ECMAScriptParser#variableDeclarationList.
    def visitVariableDeclarationList(self, ctx):
        self.visitChildren(ctx)


    # Visit a parse tree produced by ECMAScriptParser#functionBody.
    def visitFunctionBody(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#eof.
    def visitEof(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#UnaryAssignmentExpression.
    def visitUnaryAssignmentExpression(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)
