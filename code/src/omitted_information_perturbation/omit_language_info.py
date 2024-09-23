import regex as re

language_related = ['label', 'address', 'location', 'flag', 'variable', 'memory', 'byte','register\'s', 'register', 'pointer', 'stack', 'operand', 'section',  'registers', 'array', 'function', 'routine', 'syscall']

def omit_language(input_file):
	pattern = '|'.join(r"\b{}\b".format(g) for g in language_related)
	blacklist = re.compile(pattern)

	matches = []
	new_lines = []

	with open(input_file, 'r') as in_file:
		lines = in_file.readlines()
		lines = (line.strip("\n") for line in lines if line)
		for line in lines:
			matches = []
			new_line = line + ' '		
			if (len(line.split()) == 1):				#dont remove if intent's just a single word
				new_lines.append(new_line)
				continue	
			for match in re.finditer(blacklist, line):		#for each intent find words to omit
				matches.append(match.group())			#append each matched word to a list to omit them from the string later
			for m in matches:
				new_line = new_line.replace(m, "")		#delete matches from string
				new_line = new_line.replace("  ", " ")		#delete extra spaces
			new_lines.append(new_line)
		in_file.close()

	with open(input_file, 'w') as out_file:
		for line in new_lines:
			out_file.write(line+"\n")
		out_file.close()
	print("Information omitted successfully!")
	
general_words = ['zero out', 'increment', 'increase', 'decrement', 'point to', 'negate'] #additional verbs to omit
	
def omit_general_words(input_file):
	pattern = '|'.join(r"\b{}\b".format(g) for g in general_words)
	blacklist = re.compile(pattern)

	matches = []
	new_lines = []

	with open(input_file, 'r') as in_file:
		lines = in_file.readlines()
		lines = (line.strip("\n") for line in lines if line)
		for line in lines:
			matches = []
			new_line = line + ' '		
			if (len(line.split()) == 1):				#dont remove if intent's just a single word
				new_lines.append(new_line)
				continue	
			for match in re.finditer(blacklist, line):		#for each intent find words to omit
				matches.append(match.group())			#append each matched word to a list to omit them from the string later
			for m in matches:
				new_line = new_line.replace(m, "")		#delete matches from string
				new_line = new_line.replace("  ", " ")		#delete extra spaces
			new_lines.append(new_line)
		in_file.close()

	with open(input_file, 'w') as out_file:
		for line in new_lines:
			out_file.write(line+"\n")
		out_file.close()
