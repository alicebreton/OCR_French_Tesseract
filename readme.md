## Description

This repository provides tools to perform Optical Character Recognition (OCR) using the Tesseract engine and evaluate its performance using the Word Error Rate (WER). The setup includes installation instructions for the necessary libraries, guides on how to process images for OCR, and steps for evaluating the accuracy of the recognized text. Output examples and analysis tables are also provided to help visualize and understand the results of the OCR evaluation process. For a deeper analysis of the complete dataset of the book : "Le style, mode d'emploi" of Stéphane Tufféry see the PDF [OCR_Tesseract](./OCR_Tesseract.pdf).

## Installation

Make sure Tesseract is installed, this terminal line is made for Ubuntu based Operating System (OS). Use [installation documentation](https://tesseract-ocr.github.io/tessdoc/Installation.html) for other OS.

```
sudo apt install tesseract-ocr
```

Install all those other libraries:

```
pip install opencv-python pillow numpy pandas
```

or

```
pip install -r requirements.txt
```

## Usage

### OCR

To use the ocr, make sure you have all your images in the `./data/images/`. The images can be either in a *portrait* or *landscape* orientation.

To use the ocr, use this command:

```
bash ./scripts/process_image.sh ./data/images ./data/output
```

### Evaluation

To evaluate the ocr:

```
python ./scripts/eval.py
```

You should get a text file with all the results `./wer_analysis.txt`.

To get a *mardown table* and a further analysis, use this command:

```
python ./scripts/table.py --file_path ./wer_results.txt --output_file ./wer_analysis_output.txt
```

You should now have another text file called `./wer_analysis_output.txt`.

## Output exemple

### Aperçu du WER et des Erreurs

| Fichier                                           | WER (%) | Insertions | Substitutions | Suppressions | Total des Erreurs |
| ------------------------------------------------- | ------- | ---------- | ------------- | ------------ | ----------------- |
| anglicismes_2_ref.txt and anglicismes_2.txt       | 0.00    | 4          | 21            | 1            | 26                |
| anacéphaléose_ref.txt and anacéphaléose.txt   | 15.76   | 1          | 19            | 1            | 21                |
| agitato_atrabile_ref.txt and agitato_atrabile.txt | 7.37    | 0          | 0             | 0            | 0                 |

**WER moyen pour tous les fichiers :** 7.71%

### Somme des Erreurs pour tous les fichiers

| Type d'Erreur | Somme | Pourcentage (%) |
| ------------- | ----- | --------------- |
| Substitutions | 40    | 85.11           |
| Insertions    | 5     | 10.64           |
| Suppressions  | 2     | 4.26            |

### Somme des Substitutions pour tous les fichiers

| Substitution                        | Nombre |
| ----------------------------------- | ------ |
| - -> —                             | 7      |
| jeune -> Jeune                      | 2      |
| Il -> I]                            | 2      |
| ficelé. -> ?                       | 1      |
| ny -> n'y                           | 1      |
| Saint-Lazare, -> Saint-Lazare       | 1      |
| errer -> érrer                     | 1      |
| pardessus -> Pardessus              | 1      |
| s'était -> était                  | 1      |
| son -> SON                          | 1      |
| par -> Par                          | 1      |
| il -> 1]                            | 1      |
| Il -> mou,                          | 1      |
| mou. -> ieutre                      | 1      |
| s'il -> 11                          | 1      |
| esthète. -> ésthète,             | 1      |
| auto- -> auto.                      | 1      |
| attention -> on                     | 1      |
| je -> Je                            | 1      |
| dans -> ans                         | 1      |
| jours, -> Jours,                    | 1      |
| Toi, -> ‘loi,                      | 1      |
| Tu -> ‘Tu                          | 1      |
| voyageais -> Voyageais              | 1      |
| je -> —je                          | 1      |
| Le -> le                            | 1      |
| j'embraye -> J'embraye              | 1      |
| il -> 1l                            | 1      |
| ça -> Ça                          | 1      |
| invraisemblable. -> mvraisemblable. | 1      |
| y -> ÿ                             | 1      |
| l’autobus -> l'autobus             | 1      |
