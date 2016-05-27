#!/usr/bin/env python3

from Interpreter.Function import Function
from Interpreter.Environment import Environment

f = Function(["arg1", "arg2"], Environment(), lambda env: print(env.value("arg1") + env.value("arg2")))
f(None,1,2)
