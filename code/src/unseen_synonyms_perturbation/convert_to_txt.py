import csv
import argparse
import regex as re

p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

p.add_argument("--input_csv_file", help="input .csv file containing the testset's augmented intents", default=None)
p.add_argument("--output_txt_file",help="output .in file",default=None)
p.add_argument("--orig_txt_file",help="original file _orig.in file",default=None)
p.add_argument("--input_blacklist", help="input txt file containing blacklisted words and their positiom from 'convert_to_csv.py'", default=None)
p.add_argument("--lines_to_edit", help="number of lines to attack",default=100)

args = p.parse_args()

if not (args.input_csv_file or args.output_txt_file):
	raise ValueError("Must specify input and output files")

input_csv = args.input_csv_file
output_txt = args.output_txt_file
blacklist_txt = args.input_blacklist
orig_txt=args.orig_txt_file
lines_to_edit = int(args.lines_to_edit)

field = []
word = ""
new_lines = []

def special_split(line, separator):
	new_list_of_words = []
	list_of_words = re.split(r"(\[.*?\])|(\".*?\"(?<!(\\\")))" , line)		#first, split the intents if there's something between ' '
	list_of_words = [s for s in list_of_words if s] 					#remove empty elements
	#print(list_of_words)
	for w in list_of_words:
		w.rstrip()									#remove whitespace due to previous string removal
		if not re.fullmatch(r"(\[.*?\])|(\".*?\"(?<!(\\\")))" , w):		#if there were no ' '
			w = re.split(separator, w)						#split each intent on whitespace
			w = [s for s in w if s]							#remove empty elements
			new_list_of_words.append(w)
		else: 
			new_list_of_words.append([w])						#else, if there are some words between ' ', don't split
	new_list_of_words = [s for string in new_list_of_words for s in string]			#reduce double list to single list
	return new_list_of_words
	

def insert_word_into_string(string, word, position):					#insert a word into a string at a specific position
	#list_of_words = re.split(r" ", string)#string.split(' ')
	separator = r" "
	list_of_words = special_split(string, separator)
	list_of_words.insert(position,word)
	return " ".join(list_of_words)

def attack():
	with open(output_txt, "w") as out_file:
		with open(input_csv, "r") as in_file:
			next(in_file)
			for row in csv.reader(in_file):
				out_file.write(" ".join(row)+'\n')				#converting file from csv to txt
		out_file.close()
		
		with open(output_txt, "r+") as out_file:
			with open(blacklist_txt, 'r') as matches_file:
			#with open('decoder-test.in.blacklisted', 'r') as matches_file:
				lines = matches_file.read().splitlines()
				rows = out_file.read().splitlines()
				separator = r","
				for j,line in enumerate(lines):
					field = special_split(line, separator)			#get the fields for each line containing words from blacklist and their position
					if len(field) == 1:					#if there's only one field it's because line's empty except for "#"
						#print ("No word from blacklist.")		#no words were blacklisted in this intent 
						new_lines.append(rows[j])
						new_lines.append('\n')
					else:
						index = []
						word = []
						#print(field)
						for i,val in enumerate(field):			#for each field in a row get pos and words. fields are something like "0,_start,18,jump"
							if i%2==0:				#even index: it's a number indicating position
								index.append(int(val))
							else:					#odd index: it's a word
								word.append(val)
						new_line = rows[j]				#get original lines from file, the ones without blacklisted words
						for i,val in enumerate(index):	
							new_line = insert_word_into_string(new_line, word[i], index[i])	#generate new lines inserting words
						for match in re.findall(r"\"(\w+,)\"", new_line):
							new_line = new_line.replace('"'+match+'"',match)	#remove "" surrounding words with special characters, like "label,"
						#print (new_line)
						new_lines.append(new_line)
						new_lines.append('\n')
						
			out_file.seek(0)
			out_file.truncate()
			out_file.writelines(new_lines)
			out_file.close()
		in_file.close()
		
attack()
with open(orig_txt, 'r') as orig_file:						#original, non augmented file
	all_lines = orig_file.readlines()
	rand_indexes = [int(num) for num in all_lines.pop(-1).split(",")]	#retrieving indexes of modified lines from orig file
	#print(rand_indexes)
	final_lines = []
	with open(output_txt, 'r+') as in_file:					#modified, smaller file
		temp_lines = in_file.readlines()
		for index in range((len(all_lines))):
			if index in rand_indexes:
				final_lines.append(temp_lines[0])
				temp_lines.pop(0)
			else:
				final_lines.append(all_lines[index])
		in_file.seek(0)
		in_file.truncate()
		in_file.writelines(final_lines)
		in_file.close()
	orig_file.close() 

print("Conversion to txt done!")			
