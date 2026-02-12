#!/bin/bash
#SBATCH --job-name=consolidate
#SBATCH --time=04:00:00
#SBATCH --mem=32G
#SBATCH --qos=standard
#SBATCH --partition=standard
#SBATCH --account=wiser-ewsa
#SBATCH -o /home/users/mendrika/ASNIE/SLURM/submission-logs/output/%j.out
#SBATCH -e /home/users/mendrika/ASNIE/SLURM/submission-logs/error/%j.err

module load jaspy/3.11

# Expect 3 arguments
if [ "$#" -ne 3 ]; then
  echo "Usage: sbatch consolidate.sh PRODUCT THRESH_TAG BASE_PATH"
  exit 1
fi

PRODUCT=$1
THRESH=$2
BASE_PATH=$3

echo "Merging $PRODUCT with threshold $THRESH"
echo "Base path: $BASE_PATH"

python /home/users/mendrika/ASNIE/Utilities/Scripts/merge_dfs.py \
    $PRODUCT \
    $THRESH \
    $BASE_PATH
