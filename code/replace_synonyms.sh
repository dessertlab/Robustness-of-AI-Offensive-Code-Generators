#!/bin/bash

SRC_DIR=$PWD
DATASET_DIR=$SRC_DIR"/Extended_Shellcode_IA32"
dataset="Extended_Shellcode_IA32"					#change here to use a different dataset

function create_folder() {

	rm -rf $DATASET_DIR"_unseen_synonyms_"$criteria"_AT"$perc_train_dev"_test"$perc_test
	mkdir $DATASET_DIR"_unseen_synonyms_"$criteria"_AT"$perc_train_dev"_test"$perc_test

	cp $DATASET_DIR/* $DATASET_DIR"_unseen_synonyms_"$criteria"_AT"$perc_train_dev"_test"$perc_test/
	DATASET_DIR=$DATASET_DIR"_unseen_synonyms_"$criteria"_AT"$perc_train_dev"_test"$perc_test
}

function perturb_file() {

	file_to_perturb=$1
	perc_set=$2

	file_txt=$file_to_perturb
	file_txt_aug=$file_to_perturb
	file_csv=$file_to_perturb"_text.csv"
	file_csv_aug=$file_to_perturb"_perturbed.csv"
	
	# Edit only a portion of file
	
	total_lines=($(wc -l $DATASET_DIR/$file_txt))
	lines_to_edit=$(($total_lines*$perc_set/100))
	lines_to_keep=$(($total_lines-$lines_to_edit))

	echo "
"$lines_to_edit "lines out of" $total_lines "will be attacked.
	"
	
	#Convert file from txt to csv

	echo "Converting to csv and filtering..."

	python $SRC_DIR/src/unseen_synonyms_perturbation/convert_to_csv.py --input_txt_file $DATASET_DIR/$file_txt --output_csv_file $SRC_DIR/src/$file_csv --output_blacklist $SRC_DIR/src/$file_txt".blacklist" --lines_to_edit $lines_to_edit 

	echo "Perturbing dataset with TextAttack...";

	if [ $criteria_num == 0 ]; then
		python $SRC_DIR/src/unseen_synonyms_perturbation/perform_perturbation.py --input-csv $SRC_DIR/src/$file_csv --input-column intent --output-csv $SRC_DIR/src/$file_csv_aug --pct-words-to-swap $perc --transformations-per-example 1 --exclude-original --overwrite --max_candidates 50 --transformation_type "no_constr";
	
	elif [ $criteria_num == 1 ]; then
	       python $SRC_DIR/src/unseen_synonyms_perturbation/perform_perturbation.py --input-csv $SRC_DIR/src/$file_csv --input-column intent --output-csv $SRC_DIR/src/$file_csv_aug --pct-words-to-swap $perc --transformations-per-example 1 --exclude-original --overwrite --max_candidates 50 --transformation_type "wed50";
	       
	elif [ $criteria_num == 2 ]; then
	       python $SRC_DIR/src/unseen_synonyms_perturbation/perform_perturbation.py --input-csv $SRC_DIR/src/$file_csv --input-column intent --output-csv $SRC_DIR/src/$file_csv_aug --pct-words-to-swap $perc --transformations-per-example 1 --exclude-original --overwrite --max_candidates 20 --transformation_type "wed20pos";
	       
	fi

	#Convert augmented file from csv back to txt

	echo "Converting back to txt..."

	python $SRC_DIR/src/unseen_synonyms_perturbation/convert_to_txt.py --input_csv_file $SRC_DIR/src/$file_csv_aug --output_txt_file $DATASET_DIR/$file_txt_aug --input_blacklist $SRC_DIR/src/$file_txt".blacklist" --lines_to_edit $lines_to_edit --orig_txt_file $DATASET_DIR/$file_txt"_orig.in"

	rm $SRC_DIR/src/$file_csv
	rm $SRC_DIR/src/$file_csv_aug
	rm $SRC_DIR/src/$file_txt".blacklist"
	rm $DATASET_DIR/$file_txt"_orig.in"

}

function select_settings() {
	read -p "Select the criteria used to replace synonyms:
[0] - Unseen synonyms without constraints;
[1] - Unseen synonyms with constraints on the word embedding distance (WED);
[2] - Unseen synonyms with constraints on the word embedding distance (WED) and part-of-speech (POS) tag.
--> " criteria_num

	if [ -z "$criteria_num" ] || [ "$criteria_num" -gt 2 ]; then
		criteria="wed20pos";
	else
		if [ $criteria_num == 0 ]; then
			criteria="no_constr";
		elif [ $criteria_num == 1 ]; then
			criteria="wed50";
		elif [ $criteria_num == 2 ]; then
			criteria="wed20pos";
		fi
	fi
	
	read -p "Percentage of training set and dev set to perturb (default 0%): " perc_train_dev
	
	if [ -z "$perc_train_dev" ] || [ "$perc_train_dev" -gt 100 ]; then
		perc_train_dev=0;
	fi
		
	read -p "Percentage of test set to perturb (default 100%): " perc_test
	
	if [ -z "$perc_test" ] || [ "$perc_test" -gt 100 ]; then
		perc_test=100;
	fi
	
	read -p "Ratio of words to perturb within a single intent (range [0-1], default 0.1): " perc_num

	if [ -z "$perc_num" ] || [ $perc_num > 1 ]; then 
		perc=0.1;
	fi
}

select_settings;
create_folder;
if [ "$perc_train_dev" != 0 ]; then
	perturb_file $dataset"-train.in" $perc_train_dev;
	perturb_file $dataset"-dev.in" $perc_train_dev;
fi
if [ "$perc_test" != 0 ]; then
	perturb_file $dataset"-test.in" $perc_test;
fi

echo "Done!";

