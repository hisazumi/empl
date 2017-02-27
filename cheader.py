# it can read plain struct decl only. it should be support typedef...

import sys
from textx.metamodel import metamodel_from_file
from textx.exceptions import TextXSyntaxError

structm = metamodel_from_file('Cstruct.tx')

def find_or(key1, key2):
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

# Main
rest = open(sys.argv[1]).read()

deftab = {'signedchar':False, 'unsignedchar':False, 'short':False, 'unsignedshort':False, 'int':False,
              'unsignedint':False, 'long':False, 'unsignedlong':False, 'unsignedlonglong':False,
              '__mbstate_t':False, 'longunsignedint':False,
              'longlong':False, '__builtin_va_list':False}

while True:
    pos = find_or('struct', 'typedef')
    if pos < 0:
        break
    
    try:
        m = structm.model_from_str(rest[pos:])
        
        if m.struct:
            print('read struct: ' + m.struct.name)
            deftab[m.struct.name] = [[decl.type, decl.name] for decl in m.struct.decls]
        else:
            print('read typedef: ' + m.typedef.name)
            deftab[m.typedef.name] = deftab[m.typedef.orig]
            
        rest = '\n'.join(m.rest)
    except TextXSyntaxError as e:
        print('warn: ', rest[pos:pos + 30])
        rest = rest[pos + 7:] # +7 means len('struct')
    
print(deftab)
