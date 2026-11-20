#!/bin/bash
#SBATCH --job-name=dwdts-vs-crr
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
# 3: threshold_ts
# 4: threshold_crr
# 5: min_pixels
# 6: domain name

if [ "$#" -ne 6 ]; then
    echo "Usage: sbatch script.sh START END THRESH_TS THRESH_CRR MIN_PIXELS DOMAIN"
    exit 1
fi

start=$1
end=$2
threshold_ts=$3
threshold_crr=$4
min_pixels=$5
domain=$6

python /home/users/mendrika/ASNIE/Analysis/paper/dwdts_vs_crr.py \
    $start \
    $end \
    $threshold_ts \
    $threshold_crr \
    $min_pixels \
    $domain