# Enhancing Robustness of AI Offensive Code Generators via Data Augmentation

The README file is written based on our setup experience on *Ubuntu 18.04.3 LTS*. 
Please run on Linux or macOS. It is strongly recommended to run with **at least one GPU**.
Before setting up our project we'd like to make sure you have some prerequisite installations and setups. 

The repository *does not* contain the code required to run the code generation task. It contains the code required to replicate the data augmentation process via perturbation injection and the Extended_Shellcode_IA32 dataset we used for our experiments.

## Step 1: Dependencies Setup

* Move to the main directory.
* We used with **Python 3.7**, but other Python versions should work as well.
* Run ``pip3 install -r requirements.txt --user`` to install the required dependencies.

## Step 2: Dataset Setup

* Move the dataset you want to use for the perturbation process to the main directory.
* Your dataset should be divided as follows:
	- ``[DATASET_NAME]_train.in``, containing the intents of the training set; 
	- ``[DATASET_NAME]_dev.in``, containing the intents of the validation set;  
	- ``[DATASET_NAME]_test.in``, containing the intents of the test set.
* To change the dataset you want to work with, change the *DATASET_DIR* and *dataset* variables in ``replace_synonyms.sh`` or ``omit_information.sh``.

## Step 3: Apply Perturbations

### Word Substitution

* If you want to apply the **word substitution perturbation** to your data, run ``./replace_synonyms.sh``.
* You will be prompted to select: the criteria used to substitute synonyms, the percentage of words to perturb, and the percentage of intents you want to perturb in the training/validation set and test set.

A new folder named ``[DATASET_NAME]_unseen_synonyms`` will be created, containing the perturbed dataset.

### Word Omission

* If you want to apply the **word omission perturbation** to your data, run ``./omit_information.sh``.
* You will be prompted to select: the type of information you want to omit, and the percentage of intents you want to perturb in the training/validation set and test set.

The folder``[DATASET_NAME]_omitted_information`` will be created, containing the perturbed dataset.
