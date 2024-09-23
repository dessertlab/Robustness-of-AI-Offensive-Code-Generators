import csv
import argparse
import itertools
import random
from omit_action_info import *
from omit_language_info import *
from omit_value_info import *

p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

p.add_argument("--input_txt_file", help="input .in file containing the intents to perturb", default=None)
p.add_argument("--omit", help="type of information you want to omit",default=None)
p.add_argument("--lines_to_edit", help="number of intents to perturb",default=100)

args = p.parse_args()

if not (args.input_txt_file or args.remove):
	raise ValueError("Must specify input file and information to omit")

input_txt = args.input_txt_file
lines_to_edit = int(args.lines_to_edit)
info_type = int(args.omit)

temp_txt = input_txt + "_temp.in"

#perturb input_file based on the type of information to omit (i.e., 0: language-related, 1: value-related, 2: action-related)

def perturb(input_file, info_type):
	if info_type == 0:
		omit_language(input_file)
	elif info_type == 1:
		omit_values(input_file)
	elif info_type == 2:
		omit_actions(input_file)
		omit_general_words(input_file)

#perturb a specific number (equal to lines_to_edit) of random intents (or all of them)
#useful when perturbing different percentages of data for adversarial training

with open(input_txt, 'r+') as in_file:
	all_lines = in_file.readlines()
	rand_indexes = random.sample(range(len(all_lines)), lines_to_edit)
	rand_indexes.sort()
	final_lines = []
	with open(temp_txt, 'w') as temp_file:
		for i in rand_indexes:
			temp_file.write(all_lines[i])
		temp_file.close()
	perturb(temp_txt, info_type)
	with open(temp_txt, 'r') as temp_file:
		temp_lines = temp_file.readlines()
		for index in range((len(all_lines))):
			if index in rand_indexes:
				final_lines.append(temp_lines[0])
				temp_lines.pop(0)
			else:
				final_lines.append(all_lines[index])
		temp_file.close()
	in_file.seek(0)
	in_file.truncate()
	in_file.writelines(final_lines)
	in_file.close()
	
	
	
	

