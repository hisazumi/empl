# it can read plain struct decl only. it should be support typedef...

import sys
from textx.metamodel import metamodel_from_file
from textx.exceptions import TextXSyntaxError

structm = metamodel_from_file('Cstruct.tx')

# Main
rest = open(sys.argv[1]).read()
while True:
    pos = rest.find('struct')
    if pos < 0:
        break
    
    try:
        m = structm.model_from_str(rest[pos:])
        print('read: ' + m.struct.name)
        rest = '\n'.join(m.rest)
    except TextXSyntaxError as e:
        print('warn: ', rest[pos:pos+40])
        #print(e)
        rest = rest[pos + 7:]
    
    
        
