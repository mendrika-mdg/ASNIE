#!/bin/bash
#SBATCH --job-name=extract-objects
#SBATCH --time=24:00:00
#SBATCH --mem=64G
#SBATCH --qos=standard
#SBATCH --partition=standard
#SBATCH --account=wiser-ewsa
#SBATCH -o /home/users/mendrika/ASNIE/SLURM/submission-logs/output/%j.out
#SBATCH -e /home/users/mendrika/ASNIE/SLURM/submission-logs/error/%j.err

module load jaspy/3.11

# Expected arguments
# 1: PRODUCT (core, rdt, ts, roa, crr, li)
# 2: start YYYYMMDDHHMM
# 3: end YYYYMMDDHHMM
# 4: threshold
# 5: min_pixels

if [ "$#" -ne 5 ]; then
    echo "Usage: sbatch extract_objects.sh PRODUCT START END THRESHOLD MIN_PIXELS"
    exit 1
fi

product=$1
start=$2
end=$3
threshold=$4
min_pixels=$5

python /home/users/mendrika/ASNIE/Analysis/scripts/object_extraction.py \
    $product \
    $start \
    $end \
    $threshold \
    $min_pixels