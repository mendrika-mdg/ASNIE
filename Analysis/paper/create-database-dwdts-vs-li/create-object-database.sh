#!/bin/bash
#SBATCH --job-name=dwdts-vs-li
#SBATCH --time=24:00:00
#SBATCH --mem=64G
#SBATCH --qos=standard
#SBATCH --partition=standard
#SBATCH --account=wiser-ewsa
#SBATCH -o /home/users/mendrika/ASNIE/SLURM/submission-logs/output/%j.out
#SBATCH -e /home/users/mendrika/ASNIE/SLURM/submission-logs/error/%j.err

module load jaspy/3.11

# Expected arguments:
# 1: START YYYYMMDDHHMM
# 2: END YYYYMMDDHHMM
# 3: THRESH_TS
# 4: THRESH_LI
# 5: MIN_PIXELS_TS
# 6: MIN_PIXELS_LI
# 7: DOMAIN

if [ "$#" -ne 7 ]; then
    echo "Usage: sbatch script.sh START END THRESH_TS THRESH_LI MIN_PIXELS_TS MIN_PIXELS_LI DOMAIN"
    exit 1
fi

start=$1
end=$2
threshold_ts=$3
threshold_li=$4
min_pixels_ts=$5
min_pixels_li=$6
domain=$7

python /home/users/mendrika/ASNIE/Analysis/paper/dwdts_vs_li.py \
    $start \
    $end \
    $threshold_ts \
    $threshold_li \
    $min_pixels_ts \
    $min_pixels_li \
    $domain