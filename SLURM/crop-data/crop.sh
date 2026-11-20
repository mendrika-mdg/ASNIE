#!/bin/bash
#SBATCH --job-name=crop-roa-mdg
#SBATCH --time=24:00:00
#SBATCH --mem=64G
#SBATCH --qos=standard
#SBATCH --partition=standard
#SBATCH --account=wiser-ewsa
#SBATCH -o /home/users/mendrika/ASNIE/SLURM/submission-logs/output/%j.out
#SBATCH -e /home/users/mendrika/ASNIE/SLURM/submission-logs/error/%j.err

module load jaspy/3.11

# Expected arguments
# 1: start YYYYMMDDHHMM
# 2: end   YYYYMMDDHHMM

if [ "$#" -ne 2 ]; then
    echo "Usage: sbatch crop_roa.sh START END"
    exit 1
fi

start="$1"
end="$2"

python /home/users/mendrika/ASNIE/Cropping/crop_roa.py \
    "$start" \
    "$end"