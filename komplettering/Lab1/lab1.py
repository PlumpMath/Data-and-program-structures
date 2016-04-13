#shortcut functions
def cube(x): return x*x*x
def square(x): return x*x
def times(x,y): return x*y
def add(x,y): return x+y
def next(x): return x+1

# Lab 1


def sum(term, lower, successor, upper):
    if lower > upper:
        return 0
    else:
        return term(lower) + \
            sum(term, successor(lower), successor, upper)


def sum_iter(term, lower, successor, upper):
    def iter(lower, result):
        if lower > upper :
            return result
        else:
            return iter(successor(lower), result + term(lower))
    return iter(lower,0)

# 1.1 b) It is tail recursive since it recurses as its very last
#        action. The compiler/interpreter might take advantage of this
#        when optimizing execution.

###################################################################

def product(term, lower, successor, upper):
    if lower > upper:
        return 1
    else:
        return term(lower) * product(term, successor(lower), successor, upper)


def product_iter(term, lower, successor, upper):
    def iter_p(lower, result):
        if lower > upper :
            return result
        else:
            return iter_p(successor(lower), result * term(lower))
    return iter_p(lower,1)

###################################################################

def factorial(value):
    return product((lambda n: n),2,(lambda n: n + 1),value)

def even_function(n):
    if (n % 2 == 0):
        return (n+2)/(n+1)
    else:
        return (n+1)/(n+2)

def approx_pi (n):
    return 4*product_iter(even_function, 1, next, n)

###################################################################

def accumulate (combiner, null, term, lower, succ, upper):
    if lower > upper:
        return null
    else:
        return combiner(term(lower),  accumulate(combiner, null, term, succ(lower), succ, upper))


def accumulate_iter (combiner, null, term, lower, succ, upper):
    def iter_a(lower, result):
        if lower > upper :
            return result
        else:
            return iter_a(succ(lower), combiner(result,  term(lower)))
    return iter_a(lower, null)

# 1.3 c) Transitivitet. Vi måste kunna ändra ordning på operanderna
#        utan att detta påverkar resultatet. Plus och gånger fungerar,
#        minus och delat med ger inte rätt resultat.

###################################################################

def foldl (f,n,lista):
    if len(lista) == 0:
        return n
    else :
        return foldl(f,f(n,lista[0]),lista[1:])

def foldr (f,n,lista):
    if len(lista) == 0:
        return n
    else :
        return foldr(f,f(n,lista[-1]),lista[:-1])

###################################################################

def my_map(f, seq):
    return (foldl((lambda y,x: y+[f(x)]), [], seq))

def reverse_r (seq):
    return foldr((lambda x,y : x+[y]), [], seq)

def reverse_l (seq):
    return foldl((lambda x,y : [y]+x), [], seq)

###################################################################


def repeat(f, n):
    if n == 0:
        return (lambda x: x)
    else:
        return (lambda x: f(repeat(f,n-1)(x)))

# f,g => f o g = f(g(x))
def compose(f,g):
    return (lambda x: f(g(x)))



def repeated_application(f, n):
    if n == 0:
        return lambda x: x
    return accumulate_iter (compose, f, lambda x: f, 1, next, n-1)

# 1.5 b) Vi kan skriva signaturen repeat: func, Int -> func.

###################################################################
def smooth(f):
    return (lambda x: ( f(x + 0.01) + f(x) + f(x - 0.01) ) / 3 )

def n_fold_smooth(f,n):
    return(lambda x: (repeat(smooth,n))(f)(x))
# repeat f,4 -> f(f(f(f(x))))
# smooth f,4 -> (f(4.01) + f(4) + f(3.99))/3 -> y
# om repeat tar in smooth -> smooth(smooth(x)) dvs x = f?
# --> argument i 2 steg? smooth(smooth(x)) -> smooth(smooth(f(x))) = y(x)



###################################################################
###################################################################
###################################################################


def output_function():
    x = 5
    y = 10
    seq = [1,2,3,4,5]

    print("----------- Sum ---------")
    print(" recursive ")
    print("result: {0}".format(sum((lambda n: n),x,next,y)))
    print(" tail recursive ")
    print("result: {0}".format(sum_iter((lambda n: n),x,next,y)))

    print("----------- Product ---------")
    print(" recursive ")
    print("result: {0}".format(product((lambda n: n),x,next,y)))
    print(" tail recursive ")
    print("result: {0}".format(product_iter((lambda n: n),x,next,y)))

    print("----------- factorial ---------")
    print(" based on recursive product ")
    print("result: {0}".format(factorial(x)))
    print("Pi approximation: {0}".format(approx_pi(800)))

    print("----------- Accumulators ---------")
    print("accumulate sum result: {0}".format(accumulate(add,0,(lambda n: n),x,next,y)))
    print("accumulate product result: {0}".format(accumulate(times,1,(lambda n: n),x,next,y)))
    print("accumulate sum_iter result: {0}".format(accumulate_iter(add,0,(lambda n: n),x,next,y)))
    print("accumulate product_iter result: {0}".format(accumulate_iter(times,1,(lambda n: n),x,next,y)))


    print("----------- Folds left and right ---------")
    print(" seq = ",seq)
    print(" foldl(times,2,seq): ", foldl(times,2,seq))
    print(" foldr(add,0,seq): ", foldr(add,0,seq))
    print(" my_map(cube,seq) = ",my_map(cube,seq))
    print(" reverse_l(seq) = ",reverse_l(seq))
    print(" reverse_r(seq) = ",reverse_r(seq))

    print("----------- Repeat -----------")
    sq_twice = repeat(square,2)
    print("repeat square twice with input 5 result: ", sq_twice(5))
    print("Smooth square of 4 result: ", smooth(square)(4))
    five_sm = n_fold_smooth(square,5)
    print("5-fold-smooth square of 4 result: ",five_sm(4))
    regular = n_fold_smooth(square,0)
    print("regular square of 4 result: ",regular(4))

    print("Repeated_application of 5^2 two times: ", repeated_application(square, 2)(5))
    print("Repeated_application of 5^2 one time: ", repeated_application(square, 1)(5))
    print("Repeated_application of 5^2 zero times: ", repeated_application(square, 0)(5))
    print("Repeat 5^2 zero times: ", repeat(square, 0)(5))

output_function()



# 2.1

# Normal order evaluation, or lazy evaluation, would not consider f at
# all since its not needed in order to execute the body of test. Since
# x is equal to 0, the normal order evaluator doesn't have to resolve
# f. This is because normal order evaluation evaluates function bodies
# before function arguments.

# Applicative order evaluation means that the arguments are evaluated
# before the function budy in a left to right order. The implication
# being that an applicative order evaluator would get stuck in an
# infinite loop evaluating f.


#2.2

# print_mess is declared as a function-call with a preset-argument?
# which means print_mess has created it's own scope for keep_val

# value is defined on a global level
# * we run keep_val with the preset given by print_mess. (local value + global x as x is not defined locally)
# * g gets a local x and prints it while f do not inherit the x from g so it uses the global one.
# * same conditions as before but with a new global x. (local x for g and global x for f)

# b)
# global frame:
# x
# f
# g
# keep_val
# print_mess **

# ** f1:
# value = "Stored"
# f
# return?

# g

# f

# c) If python didn't have lexical scoping, but rather dynamic scoping,
#    it would mean that name lookup would step upwards the call stack
#    instead of upwards the functions definition in the code.
#
#    The output would then be:
#    --- x=10, value="New and updated"
#    In g: 5000
#    In f: 5000
#    In g: 5000
#    In f: 5000
