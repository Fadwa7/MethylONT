####-------- CALCULATION OF METHYLATION STATISTICS FROM TSV FILE GENERATED BY DeepSignal-Plant --------####
# Author: Fadwa EL KHADDAR
# Lab : DIADE - IRD
# University : Montpellier - France

import os
import subprocess
import numpy as np
import pandas as pd
import  glob
import sys
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import argparse
import re
from tkinter import *
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('TkAgg')


# Arguments

parser = argparse.ArgumentParser(description=" Script to generate methylation statistics ")
parser.add_argument('-fasta', type=str, help="Path to fasta file" )
parser.add_argument('-i', type=str, help='Path to the directory containing the .tsv files ')
parser.add_argument('-t', type=int, help='Threshold of mapped methylated reads ')
parser.add_argument('-o', type=str, help='Output directory ')

args = parser.parse_args()


# Function definition

def CpG_context():
    global CpG
    global nb_C
    global nb_CpG
    motif_counts = {}
    motif_sum = {}          # Dictionnary to store count all occurences
    motif_occurrences = {}  # Dictionnary to store count of each occurence
    positions_par_chromosome = {}
    for motif in CpG:
        motif_counts[motif] = 0
        motif_sum[motif] = 0
        motif_occurrences[motif] = []
    rows= []

# Loop through k_mer column of treated dataset

    for i, row in treated_df.iterrows():
        kmer = row['k_mer']
        first_two_letters = kmer[:2]
        if "CG" in first_two_letters:
            motif_count = first_two_letters.count("CG")
            motif_counts["CG"] += motif_count
            if motif_count > 0:
                motif_positions = [(row['chromosome'], row['strand'], pos) for pos in
                                   re.finditer("CG", first_two_letters)]  # Store the positions of the motif
                motif_occurrences["CG"].extend(motif_positions)
                rows.append(row)
    rows_CG_df = pd.DataFrame(rows)
    rows_CG = rows_CG_df.sort_values("chromosome")
    output_file = os.path.join(output_dir, filebasename + "_CG.csv")
    rows_CG.to_csv(output_file, index=False, sep='\t')
    #if not rows_CG.empty:
    #    for chromosome in rows_CG['chromosome'].unique():
    #        positions_par_chromosome[chromosome] = list(rows_CG.loc[rows_CG['chromosome'] == chromosome, ['strand', 'position']])
    total_count_CpG = sum(motif_counts.values())
    pourcentage_CpG = (total_count_CpG / nb_CpG) * 100
    pourcentage_C = (total_count_CpG / nb_C) * 100
    
    print(" --- CpG STATISTICS --- ")
    print()
    print(f" * The number of occurrences of CpG methylation : {total_count_CpG} ")
    print(
        f" * The percentage of CpG methylation among all CpGs in the genome : {pourcentage_CpG : .2f} %")
    print(
        f" * The percentage of methylated cytosines (CpG type) among all cytosines in the genome : {pourcentage_C : .2f} %")
    print()

    return total_count_CpG

def CHG_context():
    global CHG
    global nb_C
    global nb_CpG
    global output_dir
    global filebasename
    motif_counts = {} # create dictionnary to store the times the motif appears in the sequence
    motif_sum = {} #
    motif_occurrences = {}  # create a dictionary to store occurrences of each motif
    positions_par_chromosome = {}

    for motif in CHG:
        motif_counts[motif] = 0
        motif_sum[motif] = 0
        motif_occurrences[motif] = []  # initialize an empty list for each motif
    rows = []
    for i, row in treated_df.iterrows():
        kmer= row['k_mer']
        for motif in CHG:
            motif_count = kmer.count(motif)
            motif_counts[motif] += motif_count
            if motif_count > 0:
                motif_positions = [(row['chromosome'], row['strand'], pos) for pos in re.finditer(motif, kmer)]  # Store the positions of the motif
                motif_occurrences[motif].extend(motif_positions)
                rows.append(row)
    rows_CHG_df = pd.DataFrame(rows)
    rows_CHG = rows_CHG_df.sort_values("chromosome")
    output_file = os.path.join(output_dir, filebasename + "_CHG.csv")
    rows_CHG.to_csv(output_file, index=False, sep='\t')
    #if not rows_CHG.empty:
    #    for chromosome in rows_CHG['chromosome'].unique():
    #        positions_par_chromosome[chromosome] = list(rows_CHG.loc[rows_CHG['chromosome'] == chromosome, ['strand', 'position']])
    total_count_CHG = sum(motif_counts.values())
    pourcentage_C_total = (total_count_CHG / nb_C) * 100

    print(" --- CHG STATISTICS --- ")
    print()
    print(
        f"The percentage of methylated cytosines (CHG type) among all cytosines in the genome:  {pourcentage_C_total: .2f} %")
    print()
    print(f" The number of occurrences of CHG methylation : {total_count_CHG}, which includes : ")
    for motif in CHG:
        pourcentage_C_motif = (motif_counts[motif] / nb_C) * 100
        print(f"    -> {motif} apprears {motif_counts[motif]} times")
        print(f"       The pourcentage of methylated cytosines (type {motif}) is : {pourcentage_C_motif: .2f}%")
        print()

    return total_count_CHG


def CHH_context():
    global CHH
    global nb_C
    global nb_CpG
    global output_dir
    global filebasename
    motif_counts = {}  # create dictionnary to store the times the motif appears in the sequence
    motif_sum = {}  #
    motif_occurrences = {}  # create a dictionary to store occurrences of each motif
    positions_par_chromosome = {}

    for motif in CHH:
        motif_counts[motif] = 0
        motif_sum[motif] = 0
        motif_occurrences[motif] = []  # initialize an empty list for each motif
    rows = []
    for i, row in treated_df.iterrows():
        kmer = row['k_mer']
        for motif in CHH:
            motif_count = kmer.count(motif)
            motif_counts[motif] += motif_count
            if motif_count > 0:
                motif_positions = [(row['chromosome'], row['strand'], pos) for pos in
                                   re.finditer(motif, kmer)]  # Store the positions of the motif
                motif_occurrences[motif].extend(motif_positions)
                rows.append(row)
    rows_CHH_df = pd.DataFrame(rows)
    rows_CHH = rows_CHH_df.sort_values("chromosome")
    output_file = os.path.join(output_dir, filebasename + "_CHH.csv")
    rows_CHH.to_csv(output_file, index=False, sep='\t')
    #if not rows_CHH.empty:
    #    for chromosome in rows_CHH['chromosome'].unique():
    #        positions_par_chromosome[chromosome] = list(
    #            rows_CHH.loc[rows_CHH['chromosome'] == chromosome, ['strand', 'position']])
    total_count_CHH = sum(motif_counts.values())
    pourcentage_C_total = (total_count_CHH / nb_C) * 100
    print(" --- CHH STATISTICS --- ")
    print()
    print(
        f"The percentage of methylated cytosines (CHH type) among all cytosines in the genome:  {pourcentage_C_total: .2f} %")
    print()
    print(f" The number of occurrences of CHH methylation : {total_count_CHH}, which includes : ")
    for motif in CHH:
        pourcentage_C_motif = (motif_counts[motif] / nb_C) * 100
        print(f"    -> {motif} apprears {motif_counts[motif]} times")
        print(f"       The pourcentage of methylated cytosines (type {motif}) is : {pourcentage_C_motif: .2f}%")
        print()
    return total_count_CHH


def plotting():
    global nb_C
    CpG = CpG_context()
    CHG = CHG_context()
    CHH = CHH_context()

    fig, ax = plt.subplots(figsize=(8,6), subplot_kw=dict(aspect="equal"))
    nb_unmethylated = nb_C - CpG - CHG - CHH
    counts = [CpG, CHG, CHH, nb_unmethylated]

    labels = ["CpG", "CHG", "CHH", "unmethylated"]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    wedges, texts, autotexts = ax.pie(counts, autopct='%1.1f%%')
    bbox_props= dict(boxstyle="square, pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"), bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1) / 2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(f"{labels[i]}: {counts[i]}", xy=(x, y), xytext=(1.35 * np.sign(x), 1.4 * y),
                    horizontalalignment=horizontalalignment, **kw)

    #ax.pie(counts, autopct='%1.1f%%', startangle=90, center = (-2,0))
    #legend = ax.legend(labels, loc = 2)
    #ax.axis('equal')

    plt.title(f"Methylation context amoung all cytosines in the sample : {filebasename}")
    root = tk.Tk()
    root.title("Graphique")

    # Créer une zone pour afficher le graphique
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Bouton pour fermer la fenêtre
    button = tk.Button(master=root, text="Fermer", command=root.quit)
    button.pack()

    # Démarrer la boucle principale Tkinter
    tk.mainloop()

print("####-------- CALCULATION OF METHYLATION STATISTICS FROM TSV FILE GENERATED BY DeepSignal-Plant  --------####")

# list of the three methylation contexts

CpG = ["CG"]
CHG = ["CCG", "CAG", "CTG"]
CHH = ["CCC", "CAA", "CTT", "CCA", "CCT", "CAT", "CAC", "CTA", "CTC"]

path = args.i
fasta = args.fasta
#nb_CpG = args.cpg
seuil = args.t
output_dir = args.o

# Running seqtk
result = subprocess.run(f"seqtk comp {fasta} | awk '{{C+=$4}}END{{print C}}'", shell=True, capture_output=True, text=True)
if result.stdout.strip():
    nb_C = int(result.stdout.strip())
    print(f"Total number of cytosine : {nb_C}")
else:
    print("ERROR")

result = subprocess.run(f"seqtk comp {fasta} | awk '{{CpG+=$10}}END{{print CpG}}'", shell=True, capture_output=True, text=True)
if result.stdout.strip():
    nb_CpG = int(result.stdout.strip())
    print(f"Le nombre total de CpG : {nb_CpG}")
else:
    print("ERROR")




# read files

files = path + "/*.tsv"      # store the path to files
for filename in glob.glob(files): # to select all files present in that path
    filebasename = os.path.splitext(os.path.basename(filename))[0] # store the name files
    print()
    print(f" Statistics for the file : {filebasename} ")
    print()
    names = ["chromosome", "position","strand", "pos_in_strand", "prob_0_sum", "prob_1_sum", "count_modified", "count_unmodified", "coverage", "modification_frequency", "k_mer"]    #Ajout des entêtes des colonnes
    call_mods = pd.read_csv(filename, sep='\t', names=names) # read files

    # DataFrame Creation

    df = pd.DataFrame(call_mods)

    # mean coverage :

    couverture= df["coverage"].mean()
    couverture_int =int(couverture)
    print(f" The mean coverage : {couverture_int}")
    print()

    # filtring dataset

    print(f" %%% -- The following statistics are performed on a dataset whose number of reads \n in which the targeted base is considered modified is greater than or equal to {seuil} -- %%%")
    print()
    methyl= df[df["count_modified"] >= seuil]
    methylated=pd.DataFrame(methyl) # save only the methylated reads.

    #methylated.to_csv(f"/home/fadwa/Téléchargements/test/methylated_seuil.tsv", sep ="\t")
    treated_df = methylated[['chromosome', 'strand', 'position', 'k_mer']] #filter dataset
    treated_df = pd.DataFrame(treated_df)
    treated_df['k_mer'] = treated_df['k_mer'].str[2:] # filter dataset "treated_df" which contains only from the 3th element from k_mer


    #CpG_context()
    #CHG_context()
    #CHH_context()
    plotting()
