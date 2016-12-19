from pyparsing import \
    Literal, Word, ZeroOrMore, Group, Dict, Optional, \
    printables, ParseException, restOfLine, alphas, Keyword, \
    SkipTo

# import pypatt # requires python 2, but did not use

##################################
# Literals
lbrack = Literal("[").suppress()
rbrack = Literal("]").suppress()
lpar = Literal("(").suppress()
rpar = Literal(")").suppress()
lbrace = Literal("{").suppress()
rbrace = Literal("}").suppress()

##################################
# Keywords
kcase = Keyword('case')
kmatch = Keyword('match')

##################################
# Syntax Rules

# variable (not implemented)
variable = Word(alphas)
# pattern (not implemented)
pattern = variable
# case [ pattern ] { codes }
case = Group(kcase + lbrack + pattern + rbrack + lbrace + SkipTo('}') + rbrace)
# match ( variable ) { case... }
amatch = kmatch + lpar + variable + rpar + lbrace + Group(ZeroOrMore(case)) + rbrace

##################################
# Test
result = amatch.parseString('match(p){case [ a ] {printf ("Hello World\n");} case [ b ] {foo();} }')
print(result)

# Gen
def cases(ast):
    for kase in ast:
        if kase[0] == 'case':
            pat   = kase[1]
            codes = kase[2]
            print(pat)
            print(codes)
        else:
            print("error")

def gen(ast):
    variable = ast[1]
    cases(ast[2])

gen(result)

