#!/bin/bash
#SBATCH --job-name=parquet-creation
#SBATCH --time=04:00:00
#SBATCH --mem=32G
#SBATCH --qos=standard
#SBATCH --partition=standard
#SBATCH --account=wiser-ewsa
#SBATCH -o /home/users/mendrika/ASNIE/SLURM/submission-logs/output/%j.out
#SBATCH -e /home/users/mendrika/ASNIE/SLURM/submission-logs/error/%j.err

module load jaspy/3.11

# Expect 4 arguments
if [ "$#" -ne 4 ]; then
  echo "Usage: sbatch consolidate.sh PRODUCT YEAR THRESH_TAG BASE_PATH"
  exit 1
fi

PRODUCT=$1
YEAR=$2
THRESH=$3
BASE_PATH=$4

echo "Merging product: $PRODUCT"
echo "Year: $YEAR"
echo "Threshold: $THRESH"
echo "Base path: $BASE_PATH"

python /home/users/mendrika/ASNIE/Utilities/Scripts/merge_dfs_updated.py \
    $PRODUCT \
    $YEAR \
    $THRESH \
    $BASE_PATH