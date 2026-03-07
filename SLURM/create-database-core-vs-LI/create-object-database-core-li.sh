#!/bin/bash
#SBATCH --job-name=core-vs-li
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
# 3: THRESH_CORE
# 4: THRESH_LI
# 5: MIN_PIXELS_CORE
# 6: MIN_PIXELS_LI

if [ "$#" -ne 6 ]; then
    echo "Usage: sbatch script.sh START END THRESH_CORE THRESH_LI MIN_PIXELS_CORE MIN_PIXELS_LI"
    exit 1
fi

start=$1
end=$2
threshold_core=$3
threshold_li=$4
min_pixels_core=$5
min_pixels_li=$6

python /home/users/mendrika/ASNIE/Analysis/scripts/core_vs_li.py \
    $start \
    $end \
    $threshold_core \
    $threshold_li \
    $min_pixels_core \
    $min_pixels_li
