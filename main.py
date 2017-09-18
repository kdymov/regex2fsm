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

	def acceptance(self, s):
		if len(s) == 0:
			return self.__is_in_final_state()
		else:
			step = self.__transition(s[0])
			for item in step:
				if item.acceptance(s[1:]):
					return True
			return False

tokens = Lexer.tokenize('{a|b}bba')
print(tokens)

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
