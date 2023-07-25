#!/bin/bash

# Check if the username argument is provided
if [ -z "$1" ]; then
    echo "Error: Please provide your username as an argument."
    echo "Usage: $0 <username>"
    exit 1
fi


#	Import Conda

module load system/Miniconda2/4.3.31


#	Link definition of conda environment

cd

# 	Update the CONDA_ENV_URL with the file ID of the ZIP file

DSP_ENV_URL="https://drive.google.com/u/3/uc?id=1dSVYvjE1S2XlQb57NNMYFkio0TzanAgI&export=download&confirm=yes"

TOMBO_ENV_URL="https://drive.google.com/u/3/uc?id=173CkF9dXAIR7apPnIFCikFtyKFB2vlp0&export=download&confirm=yes"



#	Definition of conda env path


CONDA_ENV_DEST="/home/$1/.conda/envs"

#	Download DeepSignalPlant

wget -O dsp_env.zip "${DSP_ENV_URL}"


unzip -q dsp_env.zip -d "${CONDA_ENV_DEST}"


chmod +x  /home/$1/.conda/envs/DeepSignalPlant/bin/deepsignal_plant


#	Download Tombo


wget -O tombo_env.zip "${TOMBO_ENV_URL}"

unzip -q tombo_env.zip -d "${CONDA_ENV_DEST}"

chmod +x  /home/$1/.conda/envs/tombo/bin/tombo


rm dsp_env.zip 
rm tombo_env.zip
