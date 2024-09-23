# Enhancing Robustness of AI Offensive Code Generators via Data Augmentation

This repository contains the results we obtained during our empirical analysis. 
To reduce the possibility of errors in the manual analysis, multiple authors discussed cases of discrepancy, obtaining a consensus for all the metrics. 

- ``[MODEL]_Extended_Shellcode_IA32_no_perturbation`` contains Syntax and Semantic Accuracy scores achieved by the models when tested on the original test set (no perturbation).

- ``[MODEL]_Extended_Shellcode_IA32_word_substitution`` contains Syntax, Semantic, and Robust Accuracy scores achieved by the models when tested on the test set perturbed with word substitution.

- ``[MODEL]_Extended_Shellcode_IA32_word_substitution_AT`` contains Syntax, Semantic, and Robust Accuracy scores achieved by the models when tested on the test set perturbed with word substitution and employing Adversarial Training. The file contains 3 worksheets with varying amounts of perturbation in the training set (25%, 50%, 100%).

- ``[MODEL]_Extended_Shellcode_IA32_word_substitution_AT_cleanTestset`` contains Syntax and Semantic Accuracy scores achieved by the models when tested on the original test set (no perturbation) and employing Adversarial Training. 

- ``[MODEL]_Extended_Shellcode_IA32_word_omission`` contains Syntax, Semantic, and Robust Accuracy scores achieved by the models when tested on the test set perturbed with word omission. The file contains 3 worksheets, one for each type of word omission perturbation (structure-related, action-related, and name-related).

- ``[MODEL]_Extended_Shellcode_IA32_word_omission_AT`` contains Syntax, Semantic, and Robust Accuracy scores achieved by the models when tested on the test set perturbed with word omission and employing Adversarial Training. The file contains 9 worksheets, 3 for each type of word omission perturbation (structure-related, action-related, and name-related) and varying amounts of perturbation in the training set (25%, 50%, 100%).

- ``[MODEL]_Extended_Shellcode_IA32_word_omission_AT_cleanTestset`` contains Syntax and Semantic Accuracy scores achieved by the models when tested on the original test set (no perturbation) and employing Adversarial Training. The file contains 3 worksheets, one for each type of word omission perturbation (structure-related, action-related, and name-related).
