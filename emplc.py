from pyparsing import \
    Literal, Word, ZeroOrMore, Group, Dict, Optional, \
    printables, ParseException, restOfLine, alphas, alphanums, Keyword, \
    SkipTo, srange, delimitedList

import sys

##################################
# Literals
lbrack = Literal("[").suppress()
rbrack = Literal("]").suppress()
lpar = Literal("(").suppress()
rpar = Literal(")").suppress()
lbrace = Literal("{").suppress()
rbrace = Literal("}").suppress()
semicolon = Literal(";").suppress()
comma = Literal(",").suppress()

##################################
# Keywords
kcase = Keyword('case')
kmatch = Keyword('match')
kdefine = Keyword('define')

##################################
# Syntax Rules

# identifier
identifier = Word(srange("[a-zA-Z0-9_]"))
# type (not implemented)
type = identifier
# variable
variable = identifier
# declare variable in define
defvar = Group(type + variable + semicolon)
# define type_name { type1 var1; type2 var 2; ... };
define = Group(kdefine + identifier + lbrace + Group(ZeroOrMore(defvar)) + rbrace + semicolon)
# pattern (not implemented)
pattern = Group(delimitedList(identifier))
# case [ pattern ] { codes }
case = Group(kcase + type + lbrack + pattern + rbrack + lbrace + SkipTo('}') + rbrace)
# match ( variable ) { case... }
amatch = Group(kmatch + lpar + variable + rpar + lbrace + Group(ZeroOrMore(case)) + rbrace)
# empl
empl = define + amatch



##################################
# Generator

# struct declare {name: [varname1, varname2, ...], ...}
defines = {}


def gen_condition(var, type, ast):
    # ['_', '_', 12]
    print("if(", end="")
    firstp = True
    adef = defines[type]
    for i, p in enumerate(ast):
        if p != '_':
            if firstp:
                firstp = False
            else:
                print(' && ', end="")
            print(var + "->" + adef[i] + "==" + p, end="")
    print(")")


def gen_cases(var, ast):
    for kase in ast:
        if kase[0] == 'case':
            type  = kase[1]
            pat   = kase[2]
            codes = kase[3]

            gen_condition(var, type, pat)
            print("{")
            print(codes, end="")
            print("}")
        else:
            print("syntax error")


def gen_match(ast):
    gen_cases(ast[1], ast[2])


# read defines and make a symbol table
def read_def(ast):
    if ast[0] == 'define':
        id    = ast[1]
        decls = ast[2]

        if id in defines:
            print("multiple definition " + ast[1])
        else:
            defines[id] = [elm[1] for elm in decls]
    else:
        print("error " + ast[0])


# generate definition
def gen_def(ast):
    id = ast[1]
    decls = ast[2]

    print('struct ' + id + '{')
    for t, n in decls:
        print('%s %s;' % (t, n))
    print('};')


def gen(ast):
    read_def(ast[0])
    gen_def(ast[0])
    gen_match(ast[1])


##################################
# Main
if len(sys.argv) != 2:
    print('Usage: python %s file' % sys.argv[0])
    quit()

result = empl.parseString(open(sys.argv[1]).read())
gen(result)

