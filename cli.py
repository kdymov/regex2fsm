import sys
from core import *

args = sys.argv
regex = sys.argv[1]
machine_type = int(sys.argv[2])
test_cases = sys.argv[3:]

if machine_type == 0:
	d = FSMBuilder.build_determined(Lexer.tokenize(regex))
	for case in test_cases:
		print('d acceptance %s %s' % (case, d.acceptance(case)))
elif machine_type == 1:
	tokens_lists = [Lexer.tokenize(item.strip()) for item in regex.split(',')]
	d = MooreMachineBuilder.build_determined(tokens_lists)
elif machine_type == 2:
	tokens_lists = [Lexer.tokenize(item.strip()) for item in regex.split(',')]
	d = BuchiMachineBuilder.build_determined(tokens_lists)
