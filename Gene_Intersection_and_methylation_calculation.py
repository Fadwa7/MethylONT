import csv
import seaborn as sns
import os
import subprocess
import numpy as np
import pandas as pd
import glob
import sys
import matplotlib
import matplotlib.pyplot as plt
import argparse
import re
from tkinter import *
matplotlib.use('TkAgg')

# Définir les arguments
parser = argparse.ArgumentParser(description="Histogramme of methylation counts using bed files")
parser.add_argument('-gff', type=str, help="Path to GFF file")
parser.add_argument('-bed', type=str, nargs='*', help="Path to bed files. PLEASE PUT files in this order: CG.bed CHG.bed CHH.bed")
parser.add_argument('-o', type=str, help="Path to output folder")

args = parser.parse_args()

gff = args.gff
bed = args.bed
output = args.o
filebasename1 = os.path.splitext(os.path.basename(gff))[0]
filename_liste = []
for file_name in bed:
    filebasename_bed = os.path.splitext(os.path.basename(file_name))[0]
    filename_liste.append(filebasename_bed)
liste = filename_liste
print(f"You are working on these files:\n - GFF file: {filebasename1}\n - BED file: {liste}")

# Filtre du fichier d'annotation gff
command1 = subprocess.Popen(f'awk -v OFS="\t" \'$3 == "gene" && $3 != "mRNA" {{split($9, id, ";"); print $1, $4, $5, id[1]}}\' {gff}', shell=True, stdout=subprocess.PIPE)
output1, errors1 = command1.communicate()
count_features = output1.decode('utf-8').strip().split('\n')

# Intersection de fichier d'annotation et fichier bed
counts_dict = {}
for file in bed:
    filebasename_bed = os.path.splitext(os.path.basename(file))[0]
    command2 = subprocess.Popen(f"bedtools intersect -wao -a stdin -b {file}", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    output2, errors2 = command2.communicate(input=output1)
    intersection = output2.decode('utf-8').strip()
    columns = ["chromosome_f1", "start_f1", "end_f1", "Gene_ID", "chromosome_f2", "start_f2", "end_f2", "methylation"]
    rows = [line.split('\t') for line in intersection.split('\n') if line]
    dataframe = pd.DataFrame(rows, columns=columns)
    dataframe = dataframe[dataframe['methylation'].astype(int) != 0]
    exported_dataframe = f"{output}/gene_Intersection_gff_vs_{filebasename_bed}.csv"
    dataframe.to_csv(exported_dataframe, index=False)

    data = pd.read_csv(exported_dataframe)
    grouped = data.groupby(['chromosome_f1', 'start_f1', 'end_f1','Gene_ID']).agg({'methylation': 'sum'}).reset_index()

    grouped.to_csv(f"{output}/methylations_in_genes_{filebasename_bed}.csv")
    grouped_data = pd.read_csv(f"{output}/methylations_in_genes_{filebasename_bed}.csv")

    counts_dict[filebasename_bed] = grouped_data.groupby('chromosome_f1').size()


# Fusionner les données de comptage de méthylations dans un DataFrame
combined_counts = pd.DataFrame(counts_dict)

# Présentation graphique des résultats
gene_labels = combined_counts.index.tolist()
# Création du graphique à barres
fig, ax = plt.subplots()
bar_width = 0.3  # Largeur des barres
opacity = 0.8

# Récupérer les positions des barres sur l'axe x
x = np.arange(len(gene_labels))

# Afficher les barres pour chaque fichier BED
for i, file in enumerate(bed):
    filebasename_bed = os.path.splitext(os.path.basename(file))[0]
    counts = combined_counts[filebasename_bed].tolist()
    ax.bar(x + i * bar_width, counts, bar_width, alpha=opacity, label=filebasename_bed)

# Ajuster l'échelle de l'axe y
ax.set_ylim(0, max(combined_counts.max()) + 100)  # Ajuster les valeurs min et max selon vos données

# Définir les étiquettes des axes et la légende
ax.set_xlabel('Chromosomes')
ax.set_ylabel('Comptage de méthylations')
ax.set_title('Distribution des méthylations dans les gènes groupés en fonction des chromosomes')
ax.set_xticks(x + bar_width * (len(bed) - 1) / 2)
ax.set_xticklabels(gene_labels, rotation=90)
ax.legend()

# Afficher le graphique
plt.tight_layout()
plt.show()
