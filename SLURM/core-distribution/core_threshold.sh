#!/bin/bash
#SBATCH --job-name=core-threshold
#SBATCH --time=04:00:00
#SBATCH --mem=32G
#SBATCH --qos=standard
#SBATCH --partition=standard
#SBATCH --account=wiser-ewsa
#SBATCH -o /home/users/mendrika/ASNIE/SLURM/submission-logs/output/%j.out
#SBATCH -e /home/users/mendrika/ASNIE/SLURM/submission-logs/error/%j.err

module load jaspy/3.11
python /home/users/mendrika/ASNIE/Analysis/scripts/core_threshold.py 
