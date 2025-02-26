# Enhancing Robustness of AI Offensive Code Generators via Data Augmentation

This repository contains the code, the dataset and the experimental results related to the paper **Enhancing Robustness of AI Offensive Code Generators via Data Augmentation** published in the *Empirical Software Engineering Journal (EMSE)*.

The paper presents a data augmentation method to perturb the natural language (NL) code descriptions used to prompt AI-based code generators and automatically generate offensive code. This method is used to create new code descriptions that are semantically equivalent to the original ones, and then to assess the robustness of 3 state-of-the-art code generators against unseen inputs. Finally, the perturbation method is used to perform data augmentation, i.e., increase the diversity of the NL descriptions in the training data, to enhance the models' performance against both perturbed and non-perturbed inputs. 

![alt text](https://github.com/dessertlab/Robustness-of-AI-Offensive-Code-Generators/blob/main/perturbation_process.png)


This repository contains:
1. [**Extended Shellcode IA32**](https://github.com/dessertlab/Robustness-of-AI-Offensive-Code-Generators/tree/main/code/Extended_Shellcode_IA32), the assembly dataset used for the experiments, which we developed by extending the publicly available [Shellcode IA32](https://github.com/dessertlab/Shellcode_IA32) dataset for automatically generating shellcodes from NL descriptions. This extended version contains 5,900 unique pairs of assembly code snippets/English intents, including 1,374 intents (~23% of the dataset) that generate multiple lines of assembly code (e.g., whole functions).
2. The source code to replicate the **injection of perturbations** by performing *word substitutions* or *word omissions* on the NL code descriptions (``code`` folder). This folder also contains a README.md file detailing how to set up the project, how to change the dataset if needed, and how to run the code.
3. The **results** we obtained by feeding the perturbed code descriptions to the AI models, i.e., Seq2Seq, CodeBERT and CodeT5+ (``paper results`` folder). This folder also contains the evaluation of the models' performance on single-line vs. multi-line code snippets and the results of a survey we conducted to manually assess the semantic equivalence of perturbed NL descriptions to their original counterpart.

### Citation
If you find this work to be useful for your research, please consider citing: 

```
@article{improta2025enhancing,
  title={Enhancing robustness of AI offensive code generators via data augmentation},
  author={Improta, Cristina and Liguori, Pietro and Natella, Roberto and Cukic, Bojan and Cotroneo, Domenico},
  journal={Empirical Software Engineering},
  volume={30},
  number={1},
  year={2025},
  publisher={Springer US New York}
}
```

### Contacts 
For further information, contact us via email: *cristina.improta@unina.it* (Cristina) and *pietro.liguori@unina.it* (Pietro).
