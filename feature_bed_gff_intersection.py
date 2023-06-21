# Author : Fadwa EL KHADDAR
# University : Université de Montpellier
# Lab Institut : IRD -Montpellier
import os
import subprocess
import pandas as pd
import matplotlib
import argparse
matplotlib.use('TkAgg')

# Définir les arguments
parser = argparse.ArgumentParser(description="Histogramme of methylation counts using bed files")
parser.add_argument('-gff', type=str, help="Path to GFF file")
parser.add_argument('-bed', type=str, nargs='*', help="Path to bed files. PLEASE PUT files in this order: CG.bed CHG.bed CHH.bed")
parser.add_argument('-feature', type=str, help="Feature to look for")
parser.add_argument('-o', type=str, help="Path to output folder")

args = parser.parse_args()

gff = args.gff
bed = args.bed
feature = args.feature
output = args.o

filebasename1 = os.path.splitext(os.path.basename(gff))[0]
filename_liste = []
for file_name in bed:
    filebasename_bed = os.path.splitext(os.path.basename(file_name))[0]
    filename_liste.append(filebasename_bed)
liste = filename_liste
print(f"You are working on these files:\n - GFF file: {filebasename1}\n - BED file: {liste}")

# Filtre du fichier d'annotation gff
command1 = subprocess.Popen(f'awk -v OFS="\t" \'$3 == "{feature}" && $3 != "mRNA" {{split($9, id, ";"); print $1, $4, $5, id[1]}}\' {gff}', shell=True, stdout=subprocess.PIPE)
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
    exported_dataframe = f"{output}/{feature}_Intersection_gff_vs_{filebasename_bed}.csv"
    dataframe.to_csv(exported_dataframe, index=False)

    data = pd.read_csv(exported_dataframe)
    grouped = data.groupby(['chromosome_f1', 'start_f1', 'end_f1','Gene_ID']).agg({'methylation': 'sum'}).reset_index()

    grouped.to_csv(f"{output}/methylations_in_{feature}_{filebasename_bed}.csv")
