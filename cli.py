import sys
from core import *

# Run CLI: python cli.py "{a|b}bba" abba bba ababababababa abbabababababbba bbbbbba

args = sys.argv
regex = sys.argv[1]
test_cases = sys.argv[2:]

d = FSMBuilder.build_determined(Lexer.tokenize(regex))
print(d._FSM__states)
for case in test_cases:
	print('d acceptance %s %s' % (case, d.acceptance(case)))
