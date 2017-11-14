from tkinter import *
from core import *

def build_fsm_handler(event):
	test_cases = filter(lambda x: len(x) > 0, test_text.get('1.0', 'end').split("\n")) 
	d = FSMBuilder.build_determined(Lexer.tokenize(regex_entry.get()))
	result = '\n'.join(['%s %s' % (case, d.acceptance(case)) for case in test_cases])
	test_text.delete('1.0', 'end')
	test_text.insert('1.0', result)

def build_moore_handler(event):
	test_cases = filter(lambda x: len(x) > 0, test_text.get('1.0', 'end').split("\n"))
	tokens_lists = [Lexer.tokenize(item.strip()) for item in regex_entry.get().split(',')]
	d = MooreMachineBuilder.build_moore(tokens_lists)
	result = '\n'.join(['%s %s' % (case, d.acceptance(case)) for case in test_cases])
	test_text.delete('1.0', 'end')
	test_text.insert('1.0', result)

def build_buchi_handler(event):
	test_cases = filter(lambda x: len(x) > 0, test_text.get('1.0', 'end').split("\n"))
	tokens_lists = [Lexer.tokenize(item.strip()) for item in regex_entry.get().split(',')]
	d = BuchiMachineBuilder.build_buchi(tokens_lists)
	result = '\n'.join(['%s %s' % (case, d.acceptance(case)) for case in test_cases])
	test_text.delete('1.0', 'end')
	test_text.insert('1.0', result)

root = Tk()
regex_label = Label(root, text="Regular expression")
regex_entry = Entry(root)
test_label = Label(root, text="Test cases (one per line)")
test_text = Text(root, wrap='word')
build_fsm = Button(root, text='Build FSM')
build_moore = Button(root, text='Build Moore')
build_buchi = Button(root, text='Build Buchi')

build_fsm.bind('<Button-1>', build_fsm_handler)
build_moore.bind('<Button-1>', build_moore_handler)
build_buchi.bind('<Button-1>', build_buchi_handler)

regex_label.pack()
regex_entry.pack()
test_label.pack()
test_text.pack()
build_fsm.pack()
build_moore.pack()
build_buchi.pack()

root.mainloop()
