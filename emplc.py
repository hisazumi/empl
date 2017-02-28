import sys
import re
from subprocess import check_output
from textx.metamodel import metamodel_from_file
from textx.exceptions import TextXSyntaxError
from jinja2 import Environment, FileSystemLoader


##################################
# setup
# textx (parser generator)
structm = metamodel_from_file('cstruct.tx')
matchm = metamodel_from_file('match.tx')

# setup template engine
env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
matchtmpl = env.get_template('match.tmpl')


##################################
# Pass1: read struct and typedef
#

# struct & type table {typename: [member1, ...], ...}
#  initialized with primitive types
deftab = {'signedchar':False, 'unsignedchar':False, 'short':False, 'unsignedshort':False, 'int':False,
              'unsignedint':False, 'long':False, 'unsignedlong':False, 'unsignedlonglong':False,
              '__mbstate_t':False, 'longunsignedint':False,
              'longlong':False, '__builtin_va_list':False}

    
def read_struct_and_typedef(rest):
    def find_or(rest, key1, key2):
        pos1 = rest.find(key1)
        pos2 = rest.find(key2)
        if pos1 < 0 and pos2 < 0:
            return -1
        elif pos1 >= 0 and ((pos1 < pos2) or (pos2 < 0)):
            return pos1
        elif pos2 >= 0 and ((pos2 < pos1) or (pos1 < 0)):
            return pos2
        else:
            print(pos1, pos2)
            return -1
    
    while True:
        pos = find_or(rest, 'struct', 'typedef')
        if pos < 0:
            return
        try:
            m = structm.model_from_str(rest[pos:])
        
            if m.struct:
                #print('read struct: ' + m.struct.name)
                deftab[m.struct.name] = [[decl.type, decl.name] for decl in m.struct.decls]
            elif m.typedef:
                #print('read typedef: ' + m.typedef.name)
                deftab[m.typedef.name] = deftab[m.typedef.orig]
                
            rest = '\n'.join(m.rest)
        except TextXSyntaxError as e:
            #print('warn: ', rest[pos:pos + 30])
            rest = rest[pos + 7:] # +7 means len('struct')

def pass1(file):
    def read_preprocessed_src(file):
        src = check_output('gcc -E ' + file, shell=True, universal_newlines=True)
        return str(src)

    read_struct_and_typedef(read_preprocessed_src(file))
            

##################################
# Pass2: read %match and generate code
#
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
        elif '[]' in type:
            type_wo_p = type[:-2]
            acc = '[]'
        else:
            type_wo_p = type
            acc = '.'

        # lookup type
        d = deftab[type_wo_p]

        def access(i):
            if acc == '->':
                return expr + acc + d[i][1]
            elif acc == '[]':
                return expr + '[' + str(i) + ']'
            else:
                return expr + acc + d[i][1]

        # traverse
        tab = []
        for i, p in enumerate(pats):
            if len(p.pats) == 0:
                pexpr = str(p.expr)
                if '%h' in pexpr:
                    tab.append(re.sub(r'%h', access(i), pexpr))
                elif (str(p.expr) != '_'):
                    tab.append(access(i) + expand_expr(pexpr))
            else:
                if acc == '[]':
                    # array
                    tab.extend(traverse_patterns(access(i), type_wo_p, p.pats))
                else:
                    # struct
                    tab.extend(traverse_patterns(access(i), d[i][0], p.pats))
        return tab

    cases_pats = [traverse_patterns(model.expr, model.type, c.pat.pats)
                  for c in model.cases]
    blocks = [c.block for c in model.cases]
    print(matchtmpl.render(cases_pats=cases_pats, blocks=blocks))

    
def find_match(src):
    """ find next %match and return (start position, end position) of src """
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

    start_pos = src.find('%match')
    if start_pos < 0:
        return (-1, -1)
    body_rpos = src[start_pos:].find('{')
    end_rpos = find_nested_paren(src[start_pos + body_rpos:])
    return (start_pos, start_pos + body_rpos + end_rpos)


def pass2(file):
    rest = open(sys.argv[1]).read()
    while True:
        spos, epos = find_match(rest)
        
        if spos < 0:
            print(rest)
            break
        elif spos > 0:
            print(rest[0:spos])
            gen_match(parse_match(rest[spos:epos - 1]))
            rest = rest[epos - 1:]
        else:
            print('error')

##################################
# Main

# arg check
if len(sys.argv) != 2:
    print('Usage: python %s file' % sys.argv[0])
    quit()

# go!
pass1(sys.argv[1])
pass2(sys.argv[1])
