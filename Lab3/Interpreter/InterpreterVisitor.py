import sys
import antlr4
import Utils
import operator
import enum
import pdb

from ECMAScriptParser import ECMAScriptVisitor

from Interpreter.Console import Console
from Interpreter.Math import MathModule
from Interpreter.Environment import Environment
from Interpreter.Function import Function
from Interpreter.Object import Object, ObjectModule

class InterpreterVisitor(ECMAScriptVisitor):

    def __init__(self, environment = Environment(), input=None):
      self.environment = environment
      self.environment.defineVariable("console", Console())
      self.environment.defineVariable("Math", MathModule())
      self.environment.defineVariable("Object", ObjectModule())
      self.operators = { "+": operator.add, "-": operator.sub, "*": operator.mul,
                         "/": operator.truediv, "%": operator.mod,
                         "<<": operator.lshift, ">>": operator.rshift,
                         ">>>": lambda x, y: (x % 0x100000000) >> y,
                         "<": operator.lt, ">": operator.gt,
                         "<=": operator.le, ">=": operator.ge,
                         "==": operator.eq, "!=": operator.ne,
                         "===": lambda x, y: type(x) == type(y) and x == y,
                         "!==": lambda x, y: type(x) != type(y) or x != y,
                         "||": lambda x, y: x or y, "&&": lambda x, y: x and y }

      self.unaries = { "+": lambda x: +x, "-": lambda x: -x, "~": lambda x: ~x,
                       "!": lambda x: not x, "--": lambda x: x - 1,
                       "++": lambda x: x + 1 }


    def visitTerminal(self, node):
        if node.symbol.text == "true":
            return True
        elif node.symbol.text == "false":
            return False
        elif node.symbol.text[0] == '"':
            return node.symbol.text[1:-1]
        elif node.symbol.text[0:2] == "0x":
            return float(int(node.symbol.text, 16))
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
        return None


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
        if args == "(" or args == ")": args = []
        return func(None, *args)


    # Visit a parse tree produced by ECMAScriptParser#ThisExpression.
    def visitThisExpression(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#identifierName.
    def visitIdentifierName(self, ctx):
        return ctx.children[0].accept(self)


    # Visit a parse tree produced by ECMAScriptParser#BinaryExpression.
    def visitBinaryExpression(self, ctx):
        operator = ctx.children[1].accept(self)

        if operator == "&&":
            return ctx.children[0].accept(self) and ctx.children[2].accept(self)
        elif operator == "||":
            return ctx.children[0].accept(self) or ctx.children[2].accept(self)
        else:
            lhs = ctx.children[0].accept(self)
            rhs = ctx.children[2].accept(self)
            return self.operators[operator](lhs, rhs)


    # Visit a parse tree produced by ECMAScriptParser#futureReservedWord.
    def visitFutureReservedWord(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#initialiser.
    def visitInitialiser(self, ctx):
        return ctx.children[1].accept(self)

    # Visit a parse tree produced by ECMAScriptParser#statementList.
    def visitStatementList(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ECMAScriptParser#PropertyGetter.
    def visitPropertyGetter(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#block.
    def visitBlock(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ECMAScriptParser#expressionStatement.
    def visitExpressionStatement(self, ctx):
      self.visitChildren(ctx)


    # Visit a parse tree produced by ECMAScriptParser#keyword.
    def visitKeyword(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#elementList.
    def visitElementList(self, ctx):
        list = []
        for c in [a for a in ctx.children if a.getText() != ","]:
            list.append(c.accept(self))
        return list

    # Visit a parse tree produced by ECMAScriptParser#numericLiteral.
    def visitNumericLiteral(self, ctx):
        s = ctx.children[0].accept(self)
        try:
            return int(s)
        except ValueError:
            return float(s)


    # Visit a parse tree produced by ECMAScriptParser#ForInStatement.
    def visitForInStatement(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#emptyStatement.
    def visitEmptyStatement(self, ctx):
        return None


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
        return ctx.children[0].accept(self)

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
        array = ctx.children[0].accept(self)
        index = ctx.children[2].accept(self)
        return array[index]


    # Visit a parse tree produced by ECMAScriptParser#formalParameterList.
    def visitFormalParameterList(self, ctx):
        array = []
        for c in ctx.children:
            accept = c.accept(self)
            if accept != ",":
                array.append(accept)
        return array


    # Visit a parse tree produced by ECMAScriptParser#incrementOperator.
    def visitIncrementOperator(self, ctx):
        return ctx.children[0].accept(self)


    # Visit a parse tree produced by ECMAScriptParser#AssignmentOperatorExpression.
    def visitAssignmentOperatorExpression(self, ctx):
        operator = ctx.children[1].accept(self)
        if operator == "[":
            name = ctx.children[0].getText()
            array = ctx.children[0].accept(self)
            index = ctx.children[2].accept(self)
            operator = ctx.children[4].accept(self)
            rhs = ctx.children[5].accept(self)
            if operator == "=":
                array[index] = rhs
            elif operator == "+=":
                array[index] = array[index] + rhs
            elif operator == "-=":
                array[index] = array[index] - rhs
            elif operator == "*=":
                array[index] = array[index] * rhs
            elif operator == "/=":
                array[index] = array[index] / rhs
            else:
                print(sys._getframe().f_code.co_name)
                for c in ctx.children:
                    print("Text:", c.getText())
                raise Utils.UnimplementedVisitorException(ctx)
            return self.environment.setVariable(name, array)
        else:
            name = ctx.children[0].accept(self)
            rhs = ctx.children[2].accept(self)
            if operator == "=":
                value = rhs
            elif operator == "+=":
                value = self.environment.value(name) + rhs
            elif operator == "-=":
                value = self.environment.value(name) - rhs
            elif operator == "*=":
                value = self.environment.value(name) * rhs
            elif operator == "/=":
                value = self.environment.value(name) / rhs
            else:
                print(sys._getframe().f_code.co_name)
                for c in ctx.children:
                    print("Text:", c.getText())
                raise Utils.UnimplementedVisitorException(ctx)
            return self.environment.setVariable(name, value)

    # Visit a parse tree produced by ECMAScriptParser#PostUnaryAssignmentExpression.
    def visitPostUnaryAssignmentExpression(self, ctx):
        operator = ctx.children[1].accept(self)
        name = ctx.children[0].accept(self)
        result = self.environment.value(name)
        self.environment.setVariable(name, self.unaries[operator](self.environment.value(name)))
        return result

    # Visit a parse tree produced by ECMAScriptParser#TernaryExpression.
    def visitTernaryExpression(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#tryStatement.
    def visitTryStatement(self, ctx):
        try:
            ctx.children[1].accept(self)
        except ExceptionHandling as eh:
            ctx.children[2].error = eh.value
            ctx.children[2].accept(self)
        if len(ctx.children) > 3:
            ctx.children[3].accept(self)

    # Visit a parse tree produced by ECMAScriptParser#debuggerStatement.
    def visitDebuggerStatement(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#DoStatement.
    def visitDoStatement(self, ctx):
        ctx.children[1].accept(self)
        while ctx.children[4].accept(self):
            try:
                ctx.children[1].accept(self)
            except LoopControl as lc:
                if lc.value == "break":
                    break
                if lc.value == "continue":
                    continue
                else: raise


    # Visit a parse tree produced by ECMAScriptParser#ObjectLiteralExpression.
    def visitObjectLiteralExpression(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by EChMAScriptParser#arrayLiteral.
    def visitArrayLiteral(self, ctx):
        return ctx.children[1].accept(self)


    # Visit a parse tree produced by ECMAScriptParser#elision.
    def visitElision(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#statements.
    def visitStatements(self, ctx):
        self.visitChildren(ctx)


    # Visit a parse tree produced by ECMAScriptParser#UnaryExpression.
    def visitUnaryExpression(self, ctx):
        operator = ctx.children[0].accept(self)
        return self.unaries[operator](ctx.children[1].accept(self))


    # Visit a parse tree produced by ECMAScriptParser#WhileStatement.
    def visitWhileStatement(self, ctx):
        while ctx.children[2].accept(self):
            try:
                ctx.children[4].accept(self)
            except LoopControl as lc:
                if lc.value == "break":
                    break
                if lc.value == "continue":
                    continue
                else: raise


    # Visit a parse tree produced by ECMAScriptParser#returnStatement.
    def visitReturnStatement(self, ctx):
        if len(ctx.children) < 2:
            raise FunctionControl(ctx.children[0].accept(self))
        else:
            raise FunctionControl(ctx.children[0].accept(self), ctx.children[1].accept(self))


    # Visit a parse tree produced by ECMAScriptParser#switchStatement.
    def visitSwitchStatement(self, ctx):
        switch = ctx.children[2].accept(self)
        ctx.children[4].accept(self)(switch)


    # Visit a parse tree produced by ECMAScriptParser#expressionSequence.
    def visitExpressionSequence(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ECMAScriptParser#literal.
    def visitLiteral(self, ctx):
        return ctx.children[0].accept(self)


    # Visit a parse tree produced by ECMAScriptParser#variableStatement.
    def visitVariableStatement(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ECMAScriptParser#FunctionExpression.
    def visitFunctionExpression(self, ctx):
        name = ctx.children[1].accept(self)
        if name == "(": # Anonymous function
            parameters = ctx.children[2].accept(self)
            body = ctx.children[5].accept(self)
            return Function(parameters, self.environment, body)
        elif ctx.children[3].getText() == ")": #No args
            body = ctx.children[5].accept(self)
            self.environment.defineVariable(name, Function(
                [], self.environment, body))
            return self.environment.value(name)
        else:
            parameters = ctx.children[3].accept(self)
            body = ctx.children[6].accept(self)
            self.environment.defineVariable(name, Function(
                parameters, self.environment, body))
            return self.environment.value(name)


    # Visit a parse tree produced by ECMAScriptParser#defaultClause.
    def visitDefaultClause(self, ctx):
        self.visitChildren(ctx)


    # Visit a parse tree produced by ECMAScriptParser#statement.
    def visitStatement(self, ctx):
      self.visitChildren(ctx)


    # Visit a parse tree produced by ECMAScriptParser#ForStatement.
    def visitForStatement(self, ctx):
        firstToken = ctx.children[2].accept(self)
        if firstToken == ";":
            conditionIndex = 3
        elif firstToken == "var":
            conditionIndex = 5
            ctx.children[3].accept(self)
        else:
            conditionIndex = 4

        if ctx.children[conditionIndex].accept(self) == ";":
            condition = lambda x: True
            conditionIndex -= 1;
        else:
            condition = ctx.children[conditionIndex].accept

        while condition(self):
            if ctx.children[conditionIndex + 2].getText() == ")":
                conditionIndex -= 1
            try:
                ctx.children[conditionIndex + 4].accept(self)
            except LoopControl as lc:
                if lc.value == "break":
                    break
                if lc.value == "continue":
                    ctx.children[conditionIndex + 2].accept(self)
                    continue
                else: raise
            ctx.children[conditionIndex + 2].accept(self)


    # Visit a parse tree produced by ECMAScriptParser#caseBlock.
    def visitCaseBlock(self, ctx):
        def f(index):
            fallThrough = False
            for c in ctx.children:
                try:
                    if "case" + str(index) + ":" in c.getText() or fallThrough:
                        fallThrough = True
                        c.accept(self)
                    elif "default:" in c.getText():
                        default = c
                except LoopControl as lc:
                    if lc.value == "break":
                        break
                    else: raise
            if not fallThrough:
                default.accept(self)
        return f


    # Visit a parse tree produced by ECMAScriptParser#ParenthesizedExpression.
    def visitParenthesizedExpression(self, ctx):
        return ctx.children[1].accept(self)


    # Visit a parse tree produced by ECMAScriptParser#objectLiteral.
    def visitObjectLiteral(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#throwStatement.
    def visitThrowStatement(self, ctx):
        raise ExceptionHandling(ctx.children[1].accept(self))


    # Visit a parse tree produced by ECMAScriptParser#breakStatement.
    def visitBreakStatement(self, ctx):
        raise LoopControl(ctx.children[0].accept(self))


    # Visit a parse tree produced by ECMAScriptParser#ifStatement.
    def visitIfStatement(self, ctx):
        statement = ctx.children[0].accept(self)
        if statement == "if":
            if ctx.children[2].accept(self):
                return ctx.children[4].accept(self)
            elif len(ctx.children) > 5:
                return ctx.children[6].accept(self)
        elif statement == "else":
            return ctx.children[1].accept(self)


    # Visit a parse tree produced by ECMAScriptParser#reservedWord.
    def visitReservedWord(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#variableDeclaration.
    def visitVariableDeclaration(self, ctx):
        name = ctx.children[0].accept(self)
        if len(ctx.children) == 2:
            value = ctx.children[1].accept(self)
        else:
            value = None
        return self.environment.defineVariable(name, value)


    # Visit a parse tree produced by ECMAScriptParser#finallyProduction.
    def visitFinallyProduction(self, ctx):
        self.visitChildren(ctx)


    # Visit a parse tree produced by ECMAScriptParser#IdentifierExpression.
    def visitIdentifierExpression(self, ctx):
      return self.environment.value(ctx.children[0].accept(self))


    # Visit a parse tree produced by ECMAScriptParser#propertyName.
    def visitPropertyName(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#catchProduction.
    def visitCatchProduction(self, ctx):
        self.environment.defineVariable(ctx.children[2].accept(self), ctx.error)
        self.visitChildren(ctx)


    # Visit a parse tree produced by ECMAScriptParser#continueStatement.
    def visitContinueStatement(self, ctx):
        raise LoopControl(ctx.children[0].accept(self))


    # Visit a parse tree produced by ECMAScriptParser#caseClause.
    def visitCaseClause(self, ctx):
        self.visitChildren(ctx)


    # Visit a parse tree produced by ECMAScriptParser#arguments.
    def visitArguments(self, ctx):
        return ctx.children[1].accept(self)


    # Visit a parse tree produced by ECMAScriptParser#variableDeclarationList.
    def visitVariableDeclarationList(self, ctx):
        self.visitChildren(ctx)


    # Visit a parse tree produced by ECMAScriptParser#functionBody.
    def visitFunctionBody(self, ctx):
        def runFunction(environment):
            self.environment = environment
            for c in ctx.children:
                try:
                    c.accept(self)
                except FunctionControl as fs:
                    if fs.type == "return":
                        return fs.retval
                    else: raise
        return runFunction


    # Visit a parse tree produced by ECMAScriptParser#eof.
    def visitEof(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#UnaryAssignmentExpression.
    def visitUnaryAssignmentExpression(self, ctx):
        operator = ctx.children[0].accept(self)
        name = ctx.children[1].accept(self)
        self.environment.setVariable(name, self.unaries[operator](self.environment.value(name)))
        return self.environment.value(name)

class LoopControl(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class ExceptionHandling(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class FunctionControl(Exception):
    def __init__(self, type, retval=None):
        self.type = type
        self.retval = retval
    def __str__(self):
        return repr(self.value, self.retval)
