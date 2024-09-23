from flair.data import Sentence
from string import ascii_letters

language_related = ['label', 'address', 'location', 'flag', 'variable', 'memory', 'byte','register\'s', 'register', 'pointer', 'stack', 'operand', 'section',  'registers', 'array', 'function', 'routine', 'syscall']

registers = ['eax', 'ebx', 'ecx', 'edx', 'esp', 'ebp', 'esi', 'edi', 'ah', 'ax', 'al', 'bh', 'bl', 'bx', 'ch', 'cl', 'cx', 'dh', 'dl', 'dx', 'sp', 'bp', 'si', 'di']

def has_special_characters(word):
	if not set(word).difference(ascii_letters):
	    return 0
	else:
	    return 1
	
def omit_actions(input_file):
	from flair.models import SequenceTagger
	tagger = SequenceTagger.load("flair/upos-english")
	
	new_lines = []
	pos_blacklist = language_related + registers					#if pos tagging is incorrect, do not omit these words
	pos_blacklist.append('encodedshellcode')
	with open(input_file, 'r') as in_file:
		lines = in_file.readlines()
		lines = (line.strip("\n") for line in lines if line)
		for line in lines:
			new_line = line
			if (len(line.split()) == 1):					#dont remove if intent's just a single word
				new_lines.append(new_line)
				continue
			sentence = Sentence(line, use_tokenizer=False)			#flair pos: https://huggingface.co/flair/upos-english
			tagger.predict(sentence)
			for entity in sentence.get_spans('pos'):
				word = entity.text
				tag = str(entity.labels[0])
				if tag.startswith('V') and word not in pos_blacklist and not has_special_characters(word):
					print("verb: ", word, " tag: ", tag)
					new_line = new_line.replace(word+' ', "")
			new_lines.append(new_line)
	in_file.close()
	
	with open(input_file, 'w') as out_file:
		for line in new_lines:
			out_file.write(line+"\n")
		out_file.close()
	print("Information omitted successfully!")
