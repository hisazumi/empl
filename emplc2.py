import sys
from textx.metamodel import metamodel_from_file
from jinja2 import Environment, FileSystemLoader

##################################
# argument check
if len(sys.argv) != 2:
    print('Usage: python %s file' % sys.argv[0])
    quit()

##################################
# Read & Parse
emplm = metamodel_from_file('empl.tx')
empl = emplm.model_from_file(sys.argv[1])

##################################
# Define Table
deftab = {d.name: [[decl.type, decl.name] for decl in d.decls]
			for d in empl.defines}

##################################
# Generate
env  = Environment(loader=FileSystemLoader('./', encoding='utf8'))
tmpl = env.get_template('c.template')
gend = tmpl.render(defines=empl.defines, matches=empl.matches, deftab=deftab)

print(gend)
