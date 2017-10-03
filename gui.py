from tkinter import *
from core import *

def handler(event):
	test_cases = filter(lambda x: len(x) > 0, test_text.get('1.0', 'end').split("\n")) 
	d = FSMBuilder.build_determined(Lexer.tokenize(regex_entry.get()))
	result = '\n'.join(['%s %s' % (case, d.acceptance(case)) for case in test_cases])
	print(d._FSM__states)
	print(result)
	test_text.delete('1.0', 'end')
	test_text.insert('1.0', result)

root = Tk()
regex_entry = Entry(root)
test_text = Text(root, wrap='word')
run_btn = Button(root, text='Run')

run_btn.bind('<Button-1>', handler)

regex_entry.pack()
test_text.pack()
run_btn.pack()

root.mainloop()
