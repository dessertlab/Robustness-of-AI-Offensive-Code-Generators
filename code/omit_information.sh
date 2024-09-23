#!/bin/bash

SRC_DIR=$PWD
DATASET_DIR=$SRC_DIR"/Extended_Shellcode_IA32"
dataset="Extended_Shellcode_IA32"					#change here to use a different dataset

function create_folder() {

	rm -rf $DATASET_DIR"_omitted_information_"$criteria"_AT"$perc_train_dev"_test"$perc_test
	mkdir $DATASET_DIR"_omitted_information_"$criteria"_AT"$perc_train_dev"_test"$perc_test

	cp $DATASET_DIR/* $DATASET_DIR"_omitted_information_"$criteria"_AT"$perc_train_dev"_test"$perc_test/
	DATASET_DIR=$DATASET_DIR"_omitted_information_"$criteria"_AT"$perc_train_dev"_test"$perc_test
}

function perturb_file() {

	file_txt=$1
	perc=$2
	
	# Edit only a portion of file
	
	total_lines=($(wc -l $DATASET_DIR/$file_txt))
	lines_to_edit=$(($total_lines*$perc/100))
	lines_to_keep=$(($total_lines-$lines_to_edit))

	echo "
"$lines_to_edit "lines out of" $total_lines "will be perturbed.
	"
	echo "Omitting information..."
	
	python $SRC_DIR/src/omitted_information_perturbation/remove_words.py --input_txt_file $DATASET_DIR/$file_txt --omit $info_num --lines_to_edit $lines_to_edit
	
	rm $DATASET_DIR/$file_txt"_temp.in"
}

function select_settings() {
	read -p "Select the type of information you want to omit:
[0] -  Omit language-related information like 'register','label', 'address', etc.
[1] -  Omit value-related information like names of registers, functions, variables etc.
[2] -  Omit action-related information such as verbs like 'add', 'call', 'define', etc.
--> " info_num

	if [ -z "$info_num" ] || [ "$info_num" -gt 2 ]; then
		info_num=0;
	fi
	
	if [ "$info_num" == 0 ]; then
		criteria="language"
	elif [ "$info_num" == 1 ]; then
		criteria="value"
	elif [ "$info_num" == 2 ]; then
		criteria="action"
	fi
	
	read -p "Percentage of training set and dev set to perturb (default 0%): " perc_train_dev
	
	if [ -z "$perc_train_dev" ] || [ "$perc_train_dev" -gt 100 ]; then
		perc_train_dev=0;
	fi
		
	read -p "Percentage of test set to perturb (default 100%): " perc_test
	
	if [ -z "$perc_test" ] || [ "$perc_test" -gt 100 ]; then
		perc_test=100;
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
