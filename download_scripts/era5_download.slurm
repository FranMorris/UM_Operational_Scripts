#!/bin/bash

#SBATCH --job-name=era5_download
#SBATCH --time=12:0:0
#SBATCH --ntasks=1

#SBATCH --account=n02-MRW011379
#SBATCH --partition=serial
#SBATCH --qos=serial

source /work/n02/n02/franmorr/venvs/cdsapi/bin/activate

python download.py

