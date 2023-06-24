####### Script To Plot UpSetPlot ######
# Author : Fadwa EL KHADDAR
# Lab : UMR-DIADE IRD France 
# Univerity : University of Montpellier


import matplotlib.pyplot as plt
import pandas as pd
from upsetplot import from_contents, plot
import argparse
import os

parser = argparse.ArgumentParser("UpSet Plot for bed file intersections")
parser.add_argument('-i', type=str, nargs='*', help="Path to bed files")
args = parser.parse_args()

files = args.i
contents = {}
colors = 'black'  # Specify the color for all bars
liste = []
for file_name in files:
    filebasename = os.path.splitext(os.path.basename(file_name))[0]
    liste.append(filebasename)
    file_read = pd.read_csv(file_name, sep='\t', names=['Chromosome', 'start', 'end'])
    file_set = set(zip(file_read['Chromosome'], file_read['start'], file_read['end']))
    contents[filebasename] = file_set

print("#----- You are working on these files to construct UpSetPlot : -----#")
for name in liste:
    print(name)

# Add all data sets to a dictionary and plot the UpSet graph
upset_data = from_contents(contents)
with plt.style.context('Solarize_Light2'):
    plot(upset_data, subset_size="count", facecolor=colors, shading_color="lightgray", sort_by='cardinality', show_counts='{:d}')
    plt.show()
