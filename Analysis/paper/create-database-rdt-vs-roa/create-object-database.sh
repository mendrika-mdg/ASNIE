#!/bin/bash
#SBATCH --job-name=rdt-vs-roa
#SBATCH --time=24:00:00
#SBATCH --mem=64G
#SBATCH --qos=standard
#SBATCH --partition=standard
#SBATCH --account=wiser-ewsa
#SBATCH -o /home/users/mendrika/ASNIE/SLURM/submission-logs/output/%j.out
#SBATCH -e /home/users/mendrika/ASNIE/SLURM/submission-logs/error/%j.err

module load jaspy/3.11

# Expected arguments:
# 1: start YYYYMMDDHHMM
# 2: end YYYYMMDDHHMM
# 3: threshold_roa
# 4: min_pixels
# 5: domain name

if [ "$#" -ne 5 ]; then
    echo "Usage: sbatch script.sh START END THRESH_ROA MIN_PIXELS DOMAIN"
    exit 1
fi

start=$1
end=$2
threshold_roa=$3
min_pixels=$4
domain=$5

python /home/users/mendrika/ASNIE/Analysis/paper/rdt_vs_roa.py \
    $start \
    $end \
    $threshold_roa \
    $min_pixels \
    $domain