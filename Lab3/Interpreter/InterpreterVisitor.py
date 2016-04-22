import inspect
import operator
import collections

import antlr4
import Utils

from ECMAScriptParser import ECMAScriptVisitor

from Interpreter.Console import Console
from Interpreter.Math import MathModule
from Interpreter.Environment import Environment
from Interpreter.Object import Object, ObjectModule
from Interpreter.ControlExceptions import BreakException, ContinueException, ReturnException
from Interpreter.ESException import ESException
from Interpreter.Function import Function


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
                         '~': lambda x: float(~int(x)), '!': operator.not_,
                         '++': lambda x: x.__add__(1), '--': lambda x: x.__add__(-1)}
        self.assignment = { '=': lambda x, y: y,
                            '+=': operator.iadd, '-=': operator.isub,
                            '*=': operator.mul, '/=': operator.truediv}

    def inspector(self, ctx):
        print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
        print("In function: ", inspect.stack()[1].function)
        print("_______________________")
        print("")
        print("Begin child list, there are", len(ctx.children), "children.")
        i = 0
        for child in ctx.children:
            try:
                #val = child.accept(self)
                val = child.getText()
            except:
                pass
            print(i, str(type(val)) + ": " + str(val))
            i += 1
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
        return (ctx.children[0].accept(self), ctx.children[2].accept(self))



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
        this = self.environment.value(ctx.children[0].getText().split('.')[0])
        func = ctx.children[0].accept(self)
        args = ctx.children[1].accept(self)
        if(args == None or args == ')'):
            args = []
        return func(this, *args)


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
        if operator == "&&":
            return arg1 and ctx.children[2].accept(self)
        elif operator == "||":
            return arg1 or ctx.children[2].accept(self)
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
        self.visitChildren(ctx)


    # Visit a parse tree produced by ECMAScriptParser#PropertyGetter.
    def visitPropertyGetter(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#block.
    def visitBlock(self, ctx):
        # We don't have to define any environment since we don't have
        # to implement the let keyword.
        self.visitChildren(ctx)


    # Visit a parse tree produced by ECMAScriptParser#expressionStatement.
    def visitExpressionStatement(self, ctx):
      self.visitChildren(ctx)


    # Visit a parse tree produced by ECMAScriptParser#keyword.
    def visitKeyword(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#elementList.
    def visitElementList(self, ctx):
        return self.childrenToList(ctx.children)


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
        return ctx.children[1].accept(self)


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
        if type(array) == ObjectModule:
            return array.__dict__[str(index)]
        else:
            return array[int(index)]


    # Visit a parse tree produced by ECMAScriptParser#formalParameterList.
    def visitFormalParameterList(self, ctx):
        return self.childrenToList(ctx.children)


    # Visit a parse tree produced by ECMAScriptParser#incrementOperator.
    def visitIncrementOperator(self, ctx):
        return ctx.children[0].accept(self)

    # Visit a parse tree produced by ECMAScriptParser#AssignmentOperatorExpression.
    def visitAssignmentOperatorExpression(self, ctx):
        name = ctx.children[0].getText()
        # We're doing arrays now.
        if ctx.children[1].getText() == '[':
            index = ctx.children[2].accept(self)
            operator = ctx.children[4].accept(self)
            rhs = ctx.children[5].accept(self)
            lhs = self.environment.value(name)
            if type(lhs) == ObjectModule:
                lhs.__dict__[index] = self.assignment[operator](lhs.__dict__[index], rhs)
            else:
                lhs[int(index)] = self.assignment[operator](lhs[int(index)], rhs)
            self.environment.setVariable(name, lhs)
        elif ctx.children[1].getText() == '.':
            key = ctx.children[2].accept(self)
            operator = ctx.children[3].accept(self)
            rhs = ctx.children[4].accept(self)
            lhs = self.environment.value(name)
            if key not in lhs.__dict__:
                lhs.__dict__[key] = None
            lhs.__dict__[key] = self.assignment[operator](lhs.__dict__[key], rhs)
            self.environment.setVariable(name, lhs)
        else:
            operator = ctx.children[1].accept(self)
            rhs = ctx.children[2].accept(self)
            lhs = self.environment.value(name)
            if not self.environment.exists(name) and operator == '=':
                self.environment.defineGlobal(name)
            value = self.assignment[operator](lhs, rhs)
            self.environment.setVariable(name, value)


    # Visit a parse tree produced by ECMAScriptParser#PostUnaryAssignmentExpression.
    def visitPostUnaryAssignmentExpression(self, ctx):
      name = ctx.children[0].accept(self)
      operator = ctx.children[1].accept(self)
      value = self.environment.value(name)
      self.environment.setVariable(name, self.unaries[operator](value))
      return value


    # Visit a parse tree produced by ECMAScriptParser#TernaryExpression.
    def visitTernaryExpression(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#tryStatement.
    def visitTryStatement(self, ctx):
        try:
            ctx.children[1].accept(self)
        except ESException as e:
            ctx.children[2].exceptionValue = e.value
            ctx.children[2].accept(self)
        if len(ctx.children) == 4:
            ctx.children[3].accept(self)

    # Visit a parse tree produced by ECMAScriptParser#debuggerStatement.
    def visitDebuggerStatement(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#DoStatement.
    def visitDoStatement(self, ctx):
        ctx.children[1].accept(self)
        while ctx.children[4].accept(self):
            ctx.children[1].accept(self)


    # Visit a parse tree produced by ECMAScriptParser#ObjectLiteralExpression.
    def visitObjectLiteralExpression(self, ctx):
        return ctx.children[0].accept(self)


    # Visit a parse tree produced by ECMAScriptParser#arrayLiteral.
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
        argument = ctx.children[1].accept(self)
        return self.unaries[operator](argument)


    # Visit a parse tree produced by ECMAScriptParser#WhileStatement.
    def visitWhileStatement(self, ctx):
        while ctx.children[2].accept(self):
            try:
                ctx.children[4].accept(self)
            except BreakException:
                break
            except ContinueException:
                continue


    # Visit a parse tree produced by ECMAScriptParser#returnStatement.
    def visitReturnStatement(self, ctx):
        returnValue = ctx.children[1].accept(self)
        raise ReturnException(returnValue)


    # Visit a parse tree produced by ECMAScriptParser#switchStatement.
    def visitSwitchStatement(self, ctx):
        ctx.children[4].chosenValue = ctx.children[2].accept(self)
        ctx.children[4].accept(self)


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
        argumentIndex = 3
        # If we are dealing with a lambda.
        if ctx.children[1].getText() == '(':
            argumentIndex -= 1
        else:
            name = ctx.children[1].accept(self)


        if ctx.children[argumentIndex].getText() == ')':
            arguments = []
            argumentIndex -= 1
        else:
            arguments = ctx.children[argumentIndex].accept(self)

        body = ctx.children[argumentIndex + 3].accept(self)
        function = Function(arguments, self.environment, body)

        if ctx.children[1].getText() == '(':
            return Function(arguments, self.environment, body)
        else:
            self.environment.defineVariable(name, function)



    # Visit a parse tree produced by ECMAScriptParser#defaultClause.
    def visitDefaultClause(self, ctx):
        return (ctx.children[0].accept(self), ctx.children[2])


    # Visit a parse tree produced by ECMAScriptParser#statement.
    def visitStatement(self, ctx):
        self.visitChildren(ctx)


    # Visit a parse tree produced by ECMAScriptParser#ForStatement.
    def visitForStatement(self, ctx):
        initialization = ctx.children[2].accept(self)
        condIndex = 4
        if initialization == ';':
            condIndex -= 1
        elif initialization == 'var':
            condIndex += 1
            ctx.children[3].accept(self)

        condition = ctx.children[condIndex].accept(self)
        incrementorIndex = condIndex + 2
        if condition == ';':
            incrementorIndex -= 1
        incrementor = ctx.children[incrementorIndex].getText()
        expressionIndex = incrementorIndex + 2
        if incrementor == ')':
            expressionIndex -= 1
        while ctx.children[condIndex].accept(self):
            try:
                ctx.children[expressionIndex].accept(self)
                ctx.children[incrementorIndex].accept(self)
            except BreakException:
                break
            except ContinueException:
                ctx.children[incrementorIndex].accept(self)
                continue

    # Visit a parse tree produced by ECMAScriptParser#caseBlock.
    def visitCaseBlock(self, ctx):
        keyBodyPairs = collections.OrderedDict()
        for child in ctx.children[1:-1]:
            (key, body) = child.accept(self)
            keyBodyPairs[key] = body

        keys = list(keyBodyPairs)
        if ctx.chosenValue in keys:
            startIndex = keys.index(ctx.chosenValue)
        elif "default" in keys:
            startIndex = keys.index("default")

        bodies = list(keyBodyPairs.values())
        for body in bodies[startIndex:]:
            try:
                body.accept(self)
            except BreakException:
                break


    # Visit a parse tree produced by ECMAScriptParser#ParenthesizedExpression.
    def visitParenthesizedExpression(self, ctx):
        # Return what's between the parenthesis ( what ).
        return ctx.children[1].accept(self)


    # Visit a parse tree produced by ECMAScriptParser#objectLiteral.
    def visitObjectLiteral(self, ctx):
        obj = ObjectModule()
        for key, value in self.childrenToList(ctx.children[1:-1]):
            setattr(obj, str(key), value)
        return obj



    # Visit a parse tree produced by ECMAScriptParser#throwStatement.
    def visitThrowStatement(self, ctx):
        raise ESException(ctx.children[1].accept(self))


    # Visit a parse tree produced by ECMAScriptParser#breakStatement.
    def visitBreakStatement(self, ctx):
        raise BreakException()


    # Visit a parse tree produced by ECMAScriptParser#ifStatement.
    def visitIfStatement(self, ctx):
        if ctx.children[2].accept(self):
            ctx.children[4].accept(self)
        # If there is an else statement
        elif len(ctx.children) > 6:
            ctx.children[6].accept(self)


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
        self.environment.defineVariable(name, value)


    # Visit a parse tree produced by ECMAScriptParser#finallyProduction.
    def visitFinallyProduction(self, ctx):
        ctx.children[1].accept(self)


    # Visit a parse tree produced by ECMAScriptParser#IdentifierExpression.
    def visitIdentifierExpression(self, ctx):
      return self.environment.value(ctx.children[0].accept(self))


    # Visit a parse tree produced by ECMAScriptParser#propertyName.
    def visitPropertyName(self, ctx):
        return ctx.children[0].accept(self)


    # Visit a parse tree produced by ECMAScriptParser#catchProduction.
    def visitCatchProduction(self, ctx):
        exceptionName = ctx.children[2].accept(self)
        self.environment.defineVariable(exceptionName, ctx.exceptionValue)
        ctx.children[4].accept(self)
        self.environment.removeVariable(exceptionName)


    # Visit a parse tree produced by ECMAScriptParser#continueStatement.
    def visitContinueStatement(self, ctx):
        raise ContinueException


    # Visit a parse tree produced by ECMAScriptParser#caseClause.
    def visitCaseClause(self, ctx):
        return (ctx.children[1].accept(self), ctx.children[3])


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
                except ReturnException as re:
                    return re.value
        return runFunction

    # Visit a parse tree produced by ECMAScriptParser#eof.
    def visitEof(self, ctx):
        raise Utils.UnimplementedVisitorException(ctx)


    # Visit a parse tree produced by ECMAScriptParser#UnaryAssignmentExpression.
    def visitUnaryAssignmentExpression(self, ctx):
        operator = ctx.children[0].accept(self)
        name = ctx.children[1].accept(self)
        value = self.environment.value(name)
        self.environment.setVariable(name, self.unaries[operator](value))
        return self.environment.value(name)


    def childrenToList(self, items):
        return [item.accept(self) for item in items if not item.getText() == ',']
