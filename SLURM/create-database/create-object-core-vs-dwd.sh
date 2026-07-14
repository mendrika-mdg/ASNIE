#!/bin/bash
#SBATCH --job-name=core-vs-dwd
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
# 2: end YYYYMMDDHHMM
# 3: threshold_core
# 4: min_pixels

if [ "$#" -ne 4 ]; then
    echo "Usage: sbatch create-object-core-vs-dwd.sh START END THRESH_CORE MIN_PIXELS"
    exit 1
fi

start="$1"
end="$2"
threshold="$3"
min_pixels="$4"

python /home/users/mendrika/ASNIE/Analysis/scripts/core_vs_dwd.py \
    "$start" \
    "$end" \
    "$threshold" \
    "$min_pixels"