import regex as re

registers = ['eax', 'ebx', 'ecx', 'edx', 'esp', 'ebp', 'esi', 'edi', 'ah', 'ax', ' al', 'bh', 'bl', 'bx', 'ch', 'cl', 'cx', 'dh', 'dl', 'dx', 'sp', 'bp', 'si', 'di']

reg_names = '|'.join(r"\b{}\b".format(r) for r in registers)							#register names
func_label_names = r"|[\w]+(?= label)|[\w]+(?= function)|[\w]+(?= routine)|[\w]+(?= syscall)"			#words preceding label/funtion/routine/syscall
labels = r"|\d*[a-zA-Z]+\d+"											#variable names with numbers in them
brackets_and_labels = r"|(?<!\S)(\w*[\._]\w+)(?!\S)|(\[.*?\])"							#words with . or _ in between and between []
pattern = reg_names + labels + func_label_names + brackets_and_labels
	
def omit_values(input_file):
	blacklist = re.compile(pattern)

	matches = []
	new_lines = []

	with open(input_file, 'r') as in_file:
		lines = in_file.readlines()
		lines = (line.strip("\n") for line in lines if line)
		for line in lines:
			new_line = line + ' '
			matches = []
			if (len(line.split()) == 1):					#dont remove if intent's just a single word
				new_lines.append(new_line)
				continue		
			for match in re.finditer(blacklist, line):			#for each intent find words to remove
				matches.append(match.group())
			for m in matches:
				if m.startswith("0x"):					#don't delete hexadecimal values 
					continue
				new_line = new_line.replace(m, "", 1)			#delete match from string (just once)
				new_line = new_line.replace("  ", " ")			#delete extra spaces
			new_lines.append(new_line)
		in_file.close()
		
	with open(input_file, 'w') as out_file:
		for line in new_lines:
			out_file.write(line+"\n")
		out_file.close()
	print("Information removal complete!")
