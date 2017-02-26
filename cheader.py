# it can read plain struct decl only. it should be support typedef...

import sys
from textx.metamodel import metamodel_from_file
from textx.exceptions import TextXSyntaxError

structm = metamodel_from_file('Cstruct.tx')

# Main
rest = open(sys.argv[1]).read()
while True:
    spos = rest.find('struct')
    tpos = rest.find('typedef')
    if spos < 0 or tpos < 0:
        break
    elif spos > 0 and (spos < tpos or tpos < 0):
        pos = spos
    elif tpos > 0 and (tpos < spos or spos < 0):
        pos = tpos
    
    try:
        m = structm.model_from_str(rest[pos:])
        if m.struct:
            print('read: ' + m.struct.name)
        else:
            print('read: ' + m.typedef.name)
        rest = '\n'.join(m.rest)
    except TextXSyntaxError as e:
        print('warn: ', rest[pos:pos+30])
        #print(e)
        rest = rest[pos + 7:]
    
    
        
