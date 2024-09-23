import argparse
from textattack.augmentation import Augmenter
from textattack.constraints.pre_transformation import (RepeatModification,StopwordModification)
import csv
import os
import time
import tqdm
import textattack

DEFAULT_CONSTRAINTS = [RepeatModification(), StopwordModification()]

class EmbeddingsAugmenterConstrained(Augmenter):

	def __init__(self, max_cand, transformation_type, **kwargs):
        	from textattack.transformations import WordSwapEmbedding
        	from textattack.constraints.semantics import WordEmbeddingDistance
        	from textattack.constraints.grammaticality import PartOfSpeech
        	
        	transformation = WordSwapEmbedding(max_candidates=max_cand)
        	wed = WordEmbeddingDistance(min_cos_sim=0.8)
        	pos = PartOfSpeech(tagger_type='nltk', tagset='universal', allow_verb_noun_swap=False, compare_against_original=True, language_nltk='eng', language_stanza='en')
        	
        	constraints = DEFAULT_CONSTRAINTS
        	
        	if transformation_type == "wed50":
        		constraints.append(wed)
        	elif transformation_type == "wed20pos":
        		constraints.append(wed)
        		constraints.append(pos)
        		
        	super().__init__(transformation, constraints=constraints, **kwargs)


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

input_csv: str
output_csv: str
input_column: str
pct_words_to_swap: float = 0.1
transformations_per_example: int = 2
random_seed: int = 42
exclude_original: bool = False
overwrite: bool = False
	
parser.add_argument("--input-csv",required=True,type=str,help="Path of input CSV file to augment.")
parser.add_argument("--output-csv",required=True,type=str,help="Path of CSV file to output augmented data.")
parser.add_argument("--input-column","--i",required=True,type=str,help="CSV input column to be augmented")
parser.add_argument("--pct-words-to-swap","--p",help="Percentage of words to modify when generating each augmented example.",type=float,default=0.1)
parser.add_argument("--transformations-per-example","--t",help="number of augmentations to return for each input",type=int,default=2)
parser.add_argument("--exclude-original",default=False,action="store_true",help="exclude original example from augmented CSV")
parser.add_argument("--overwrite",default=False,action="store_true",help="overwrite output file, if it exists")
parser.add_argument("--max_candidates",help="number of nearest neighbors to consider as candidates for perturbation", type=int, default=20)
parser.add_argument("--transformation_type",help="the transformation to perform (with or without constrains", type=str, default="wed20pos")
	
args = parser.parse_args()
	
def EmbeddingsAugmenterCommand(args):
	textattack.shared.utils.set_seed(random_seed)
	start_time = time.time()
	if not (args.input_csv and args.input_column):
		raise ArgumentError("The following arguments are required: --csv, --input-column/--i")
	if not os.path.exists(args.input_csv):
		raise FileNotFoundError(f"Can't find CSV at location {args.input_csv}")
	if os.path.exists(args.output_csv):
		if args.overwrite:
			textattack.shared.logger.info(f"Preparing to overwrite {args.output_csv}.")
		else:
			raise OSError(f"Outfile {args.output_csv} exists and --overwrite not set.")
	csv_file = open(args.input_csv, "r")
	dialect = csv.Sniffer().sniff(csv_file.readline(), delimiters=";,")
	csv_file.seek(0)
	rows = [row for row in csv.DictReader(csv_file, dialect=dialect, skipinitialspace=True)]
	row_keys = set(rows[0].keys())
	if args.input_column not in row_keys:
		raise ValueError(f"Could not find input column {args.input_column} in CSV. Found keys: {row_keys}")
	textattack.shared.logger.info(f"Read {len(rows)} rows from {args.input_csv}. Found columns {row_keys}.")

	augmenter = EmbeddingsAugmenterConstrained(args.max_candidates, args.transformation_type, pct_words_to_swap=args.pct_words_to_swap,transformations_per_example=args.transformations_per_example)

	output_rows = []
	for row in tqdm.tqdm(rows, desc="Augmenting rows"):
		text_input = row[args.input_column]
		if not args.exclude_original:
			output_rows.append(row)
		for augmentation in augmenter.augment(text_input):
			augmented_row = row.copy()
			augmented_row[args.input_column] = augmentation
			output_rows.append(augmented_row)
	with open(args.output_csv, "w") as outfile:
		csv_writer = csv.writer(outfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
		csv_writer.writerow(output_rows[0].keys())
		for row in output_rows:
			csv_writer.writerow(row.values())
	textattack.shared.logger.info(f"Wrote {len(output_rows)} augmentations to {args.output_csv} in {time.time() - start_time}s.")
				
EmbeddingsAugmenterCommand(args)
