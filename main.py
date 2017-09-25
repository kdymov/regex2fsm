class Token:
	def __init__(self, initializer):
		self.content = initializer

	def __repr__(self):
		return self.__class__.__name__ + '(' + str(self.content) + ')'

	def parse(self):
		raise NotImplementedError('Method parse is not implemented in Token class')

class LetterToken(Token):
	def parse(self):
		return LetterToken(self.content)

class SequenceToken(Token):
	def parse(self):
		if '|' in self.content:
			return DisjunctionToken([SequenceToken(item) for item in self.content.split('|')]).parse()
		else:
			return [LetterToken(item) for item in self.content]

class RegexToken(Token):
	def parse(self):
		return Lexer.tokenize(self.content)

class DisjunctionToken(Token):
	def parse(self):
		return DisjunctionToken([item.parse() for item in self.content])

class GroupToken(Token):
	def parse(self):
		return GroupToken(RegexToken(self.content[1:-1]).parse())

class IterationToken(Token):
	def parse(self):
		return IterationToken(RegexToken(self.content[1:-1]).parse())

class Lexer:
	@classmethod
	def __parse_groups(cls, regex):
		current_group = ''
		groups = []
		opened = 0
		opened_curve = 0
		for char in regex:
			if char == '(' and opened_curve == 0:
				if opened == 0 and len(current_group) > 0:
					groups.append(SequenceToken(current_group))
					current_group = ''
				opened += 1
				current_group += char
			elif char == ')' and opened_curve == 0:
				opened -= 1
				if opened < 0:
					raise ValueError('Incorrect regex')
				current_group += char
				if opened == 0:
					groups.append(GroupToken(current_group))
					current_group = ''
			elif char == '{' and opened == 0:
				if opened_curve == 0 and len(current_group) > 0:
					groups.append(SequenceToken(current_group))
					current_group = ''
				opened_curve += 1
				current_group += char
			elif char == '}' and opened == 0:
				opened_curve -= 1
				if opened_curve < 0:
					raise ValueError('Incorrect regex')
				current_group += char
				if opened_curve == 0:
					groups.append(IterationToken(current_group))
					current_group = ''
			else:
				current_group += char
		if opened > 0 or opened_curve > 0:
			raise ValueError('Incorrect regex')
		if len(current_group) > 0:
			groups.append(SequenceToken(current_group))
		return groups

	@classmethod
	def __outer_parse(cls, groups):
		return [item.parse() for item in groups]

	@classmethod
	def __make_plane(cls, parsed):
		result = []
		for item in parsed:
			if type(item) == type([]):
				result += item
			else:
				result.append(item)
		return result

	@classmethod
	def tokenize(cls, regex):
		return cls.__make_plane(cls.__outer_parse(cls.__parse_groups(regex)))

class FSM:
	def __init__(self):
		self.__states = {}
		self.__final_states = []
		self.__current_state = None

	def __copy(self):
		b = FSM()
		b.__states = self.__states
		b.__final_states = self.__final_states
		b.__current_state = self.__current_state
		return b

	def __transition(self, char):
		try:
			ways = self.__states[self.__current_state][char]
			results = [self.__copy() for _ in ways]
			for i in range(len(ways)):
				results[i].__current_state = ways[i]
			return results
		except:
			return []

	def __is_in_final_state(self):
		return self.__current_state in self.__final_states

	def all_possible_transitions(self, states, char):
		result = []
		for state in states:
			try:
				result += self.__states[state][char]
			except:
				pass
		result = sorted(list(set(result)))
		return result

	def all_possible_chars(self, states):
		result = []
		for state in states:
			result += self.__states[state].keys()
		result = sorted(list(set(result)))
		return result

	def add_state(self, index, is_final):
		if index in self.__states:
			raise ValueError('State is already exist in FSM')
		else:
			self.__states[index] = {}
			if is_final:
				self.__final_states.append(index)

	def add_transition(self, source, target, char):
		if source in self.__states and target in self.__states:
			try:
				self.__states[source][char].append(target)
			except:
				self.__states[source][char] = [target]
		else:
			raise ValueError('Source or target does not exist in FSM')

	def set_initial_state(self, index):
		if index in self.__states:
			self.__current_state = index
		else:
			raise ValueError('State does not exist in FSM')

	def add_final_state(self, index):
		if index in self.__states:
			self.__final_states.append(index)
		else:
			raise ValueError('State does not exist in FSM')

	def epsilon_closure(self, index):
		result = [index]
		try:
			epsilon_ways = self.__states[index]['$']
			for way in epsilon_ways:
				result += self.epsilon_closure(way)
		except:
			pass
		return result

	def all_epsilon_closures(self):
		result = []
		for index in self.__states:
			result.append((index, self.epsilon_closure(index)))
		return result

	def acceptance(self, s):
		if len(s) == 0:
			return self.__is_in_final_state()
		else:
			step = self.__transition(s[0])
			for item in step:
				if item.acceptance(s[1:]):
					return True
			return False

class FSMBuilder:
	@classmethod
	def build(cls, tokens):
		a = FSM()
		a.add_state('0', False)
		a.add_state('1', True)
		a.add_transition('0', '1', '@0')
		a.set_initial_state('0')
		address = 1
		last_state = 1
		addr = [('@0', tokens, '0', '1')]
		while len(addr) > 0:
			current = addr[0]
			if type(current[1]) == type([]):
				prev = current[2]
				last_in_seq = current[3]
				del a._FSM__states[current[2]][current[0]]
				for i in current[1][:-1]:
					last_state += 1
					a.add_state(str(last_state), False)
					if type(i) == type(LetterToken('')):
						a.add_transition(str(prev), str(last_state), i.content)
					elif type(i) == type(GroupToken('')):
						addr.append(('@' + str(address), i.content, str(prev), str(last_state)))
						a.add_transition(str(prev), str(last_state), '@' + str(address))
						address += 1
					else:
						addr.append(('@' + str(address), i, str(prev), str(last_state)))
						a.add_transition(str(prev), str(last_state), '@' + str(address))
						address += 1
					prev = last_state
				if type(current[1][-1]) == type(LetterToken('')):
					a.add_transition(str(prev), str(last_in_seq), current[1][-1].content)
				elif type(current[1][-1]) == type(GroupToken('')):
					addr.append(('@' + str(address), current[1][-1].content, str(prev), str(last_in_seq)))
					a.add_transition(str(prev), str(last_in_seq), '@' + str(address))
					address += 1
				else:
					addr.append(('@' + str(address), current[1][-1], str(prev), str(last_in_seq)))
					a.add_transition(str(prev), str(last_in_seq), '@' + str(address))
					address += 1
				addr = addr[1:]
			elif type(current[1]) == type(DisjunctionToken('')):
				del a._FSM__states[current[2]][current[0]]
				from_state = current[2]
				to_state = current[3]
				for item in current[1].content:
					addr.append(('@' + str(address), item, from_state, to_state))
					a.add_transition(from_state, to_state, '@' + str(address))
					address += 1
				addr = addr[1:]
			elif type(current[1]) == type(IterationToken('')):
				del a._FSM__states[current[2]][current[0]]
				from_state = current[2]
				to_state = current[3]
				last_state += 1
				a.add_state(str(last_state), False)
				a.add_transition(from_state, str(last_state), '$')
				a.add_transition(str(last_state), to_state, '$')
				addr.append(('@' + str(address), current[1].content, str(last_state), str(last_state)))
				a.add_transition(str(last_state), str(last_state), '@' + str(address))
				address += 1
				addr = addr[1:]
			else:
				break
		return a

	@classmethod
	def remove_eps(cls, fsm):
		closures = fsm.all_epsilon_closures()
		return fsm

	@classmethod
	def determinize(cls, fsm):
		return fsm

tokens = Lexer.tokenize('{a|b}bba')
print(tokens)
x = FSMBuilder.build(tokens)
print(x._FSM__states)
print('x acceptance $aa$bba', x.acceptance('$aa$bba'))
print('x acceptance $b$bba', x.acceptance('$b$bba'))
print('x acceptance $bbababababaaababa$bba', x.acceptance('$bbababababaaababa$bba'))
print(x.all_epsilon_closures())

a = FSM()
a.add_state('0', False)
a.add_state('1', False)
a.add_state('2', False)
a.add_state('3', True)
a.add_transition('0', '0', 'a')
a.add_transition('0', '0', 'b')
a.add_transition('0', '1', 'b')
a.add_transition('1', '2', 'b')
a.add_transition('2', '3', 'a')
a.set_initial_state('0')
test = ['ba', 'a', 'aaaab', 'abba', 'ababbbbbbababababaa']
for i in test:
	print(a.acceptance(i))

trans = a.all_possible_chars(['0', '1'])
for tr in trans:
	print(a.all_possible_transitions(['0', '1'], tr))
