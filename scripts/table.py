import re
import pandas as pd
from collections import Counter
import argparse

def parse_wer_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()

    data = re.sub(r'Mean WER for all files: \d+\.\d+%', '', data)

    wer_pattern = r'WER for (.+): (\d+\.\d+)%'
    wer_matches = re.findall(wer_pattern, data)

    error_pattern = r'Incorrect tokens:\n((?:\s+- .+\n)*)'
    error_matches = re.findall(error_pattern, data)

    error_matches.extend([""] * (len(wer_matches) - len(error_matches)))

    files = []
    wers = []
    insertions = []
    substitutions = []
    deletions = []
    substitution_counter = Counter()

    for i, match in enumerate(wer_matches):
        file_name = match[0]
        wer = float(match[1])

        error_block = error_matches[i]

        insert_count = error_block.count('Insertion')
        subst_count = error_block.count('Substitution')
        delete_count = error_block.count('Deletion')

        subst_pattern = r"Substitution: '(.+)' -> '(.+)'"
        subst_matches = re.findall(subst_pattern, error_block)
        for original, new in subst_matches:
            substitution_counter[(original, new)] += 1

        files.append(file_name)
        wers.append(wer)
        insertions.append(insert_count)
        substitutions.append(subst_count)
        deletions.append(delete_count)

    df_overview = pd.DataFrame({
        'Fichier': files,
        'WER (%)': wers,
        'Insertions': insertions,
        'Substitutions': substitutions,
        'Suppressions': deletions
    })

    df_overview['Total des Erreurs'] = df_overview['Insertions'] + df_overview['Substitutions'] + df_overview['Suppressions']

    total_insertions = df_overview['Insertions'].sum()
    total_substitutions = df_overview['Substitutions'].sum()
    total_deletions = df_overview['Suppressions'].sum()
    total_errors = df_overview['Total des Erreurs'].sum()

    df_sum_errors = pd.DataFrame({
        'Type d\'Erreur': ['Insertions', 'Substitutions', 'Suppressions', 'Total des Erreurs'],
        'Somme': [total_insertions, total_substitutions, total_deletions, total_errors]
    })

    df_sum_errors['Pourcentage (%)'] = (df_sum_errors['Somme'] / total_errors) * 100

    df_sum_errors = df_sum_errors.sort_values(by='Somme', ascending=False)

    df_sum_substitutions = pd.DataFrame.from_dict(substitution_counter, orient='index', columns=['Nombre'])
    df_sum_substitutions.index = df_sum_substitutions.index.map(lambda x: f"{x[0]} -> {x[1]}")
    df_sum_substitutions = df_sum_substitutions.reset_index()
    df_sum_substitutions.columns = ['Substitution', 'Nombre']

    df_sum_substitutions = df_sum_substitutions.sort_values(by='Nombre', ascending=False)

    return df_overview, df_sum_errors, df_sum_substitutions

def output_to_file(df_overview, df_sum_errors, df_sum_substitutions, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("### Aperçu du WER et des Erreurs\n")
        file.write("| Fichier | WER (%) | Insertions | Substitutions | Suppressions | Total des Erreurs |\n")
        file.write("|---------|---------|------------|---------------|--------------|-------------------|\n")
        for _, row in df_overview.iterrows():
            file.write(f"| {row['Fichier']} | {row['WER (%)']:.2f} | {row['Insertions']} | {row['Substitutions']} | {row['Suppressions']} | {row['Total des Erreurs']} |\n")

        file.write("\n### Somme des Erreurs pour tous les fichiers\n")
        file.write("| Type d'Erreur | Somme | Pourcentage (%) |\n")
        file.write("|---------------|-------|-----------------|\n")
        for _, row in df_sum_errors.iterrows():
            file.write(f"| {row['Type d\'Erreur']} | {row['Somme']} | {row['Pourcentage (%)']:.2f} |\n")

        file.write("\n### Somme des Substitutions pour tous les fichiers\n")
        file.write("| Substitution | Nombre |\n")
        file.write("|--------------|--------|\n")
        for _, row in df_sum_substitutions.iterrows():
            file.write(f"| {row['Substitution']} | {row['Nombre']} |\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Traiter les résultats WER et afficher les tableaux.")
    parser.add_argument('--file_path', type=str, default="./wer_results.txt", help="Chemin vers le fichier des résultats WER.")
    parser.add_argument('--output_file', type=str, default="./wer_analysis_output.txt", help="Chemin vers le fichier de sortie.")
    
    args = parser.parse_args()

    df_overview, df_sum_errors, df_sum_substitutions = parse_wer_file(args.file_path)

    output_to_file(df_overview, df_sum_errors, df_sum_substitutions, args.output_file)
