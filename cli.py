import sys
from core import *

args = sys.argv
regex = sys.argv[1]
test_cases = sys.argv[2:]

d = FSMBuilder.build_determined(Lexer.tokenize(regex))
for case in test_cases:
	print('d acceptance %s %s' % (case, d.acceptance(case)))
