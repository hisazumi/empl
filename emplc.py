import sys
from textx.metamodel import metamodel_from_file
from jinja2 import Environment, FileSystemLoader
import re


##################################
# argument check
if len(sys.argv) != 2:
    print('Usage: python %s file' % sys.argv[0])
    quit()


##################################
# setup textx (parser generator)
defm = metamodel_from_file('define.tx')
matchm = metamodel_from_file('match.tx')


##################################
# setup template engine
env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
deftmpl = env.get_template('define.tmpl')
matchtmpl = env.get_template('match.tmpl')


##################################
# Define
deftab = {}


def parse_define(src):
    m = defm.model_from_str(src)
    deftab[m.define.name] = [[decl.type, decl.name] for decl in m.define.decls]
    return m.define


def gen_define(model):
    print(deftmpl.render(define=model))


##################################
# Match
def parse_match(src):
    return matchm.model_from_str(src).match


def gen_match(model):
    def expand_expr(expr):
        def startswithop(str):
            ops = ['>=', '<=']
            ops.extend(list("><+-*/"))
            for op in ops:
                if expr.startswith(op):
                    return True
            return False

        if startswithop(expr):
            return expr
        else:
            return '==' + expr

    def traverse_patterns(expr, type, pats):
        # find struct access operator & type
        if '*' in type:
            type_wo_p = type[:-1]
            acc = '->'
        else:
            type_wo_p = type
            acc = '.'

        # lookup type
        d = deftab[type_wo_p]

        # traverse
        tab = []
        for i, p in enumerate(pats):
            if len(p.pats) == 0:
                pexpr = str(p.expr)
                if 'here' in pexpr:
                    tab.append(re.sub(r'here', expr + acc + d[i][1], pexpr))
                elif (str(p.expr) != '_'):
                    tab.append(expr + acc + d[i][1] + expand_expr(pexpr))
            else:
                tab.extend(traverse_patterns(expr + acc + d[i][1],
                                             d[i][0], p.pats))
        return tab

    cases_pats = [traverse_patterns(model.expr, model.type, c.pat.pats)
                  for c in model.cases]
    blocks = [c.block for c in model.cases]
    print(matchtmpl.render(cases_pats=cases_pats, blocks=blocks))


##################################
# Parse & Generate

# Some utilities for parser
# src is not contain start '{'
def find_nested_paren(src):
    opened_paren = 1
    for i, c in enumerate(src):
        if c == '{':
            opened_paren += 1
        elif c == '}':
            opened_paren -= 1

        if opened_paren <= 0:
            return i + 1
    return -1


def find_match(src):
    start_pos = src.find('%match')
    if start_pos < 0:
        return (-1, -1)
    body_rpos = src[start_pos:].find('{')
    end_rpos = find_nested_paren(src[start_pos + body_rpos:])
    return (start_pos, start_pos + body_rpos + end_rpos)


def find_define(src):
    start_pos = src.find('%define')
    if start_pos <= 0:
        return (-1, -1)
    else:
        return (start_pos, src.find('};') + 2)


# Main
rest = open(sys.argv[1]).read()
while True:
    match_index = find_match(rest)
    define_index = find_define(rest)
    mi = match_index[0]
    di = define_index[0]

    if mi < 0 and di < 0:
        print(rest)
        break
    elif (mi >= 0 and di < 0) or (mi < di and mi > 0):
        i = match_index
        print(rest[0:i[0]])
        gen_match(parse_match(rest[i[0]:i[1] - 1]))
        rest = rest[i[1] - 1:]
    elif (mi < 0 and di >= 0) or (mi > di and di > 0):
        i = define_index
        print(rest[0:i[0]])
        gen_define(parse_define(rest[i[0]:i[1]]))
        rest = rest[i[1]:]
    else:
        print('error')
