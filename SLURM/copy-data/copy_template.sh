#!/bin/bash
#SBATCH --job-name=copy-roa
#SBATCH --time=04:00:00
#SBATCH --mem=4G
#SBATCH --qos=standard
#SBATCH --partition=standard
#SBATCH --account=wiser-ewsa
#SBATCH -o /home/users/mendrika/ASNIE/SLURM/submission-logs/output/%j.out
#SBATCH -e /home/users/mendrika/ASNIE/SLURM/submission-logs/error/%j.err

SRC=/gws/nopw/j04/cocoon/SSA_domain/ch9_wavelet
DST=/gws/ssde/j25b/swift/mendrika/RoA

YEAR=$1
MONTH=$2

if [ -z "$YEAR" ] || [ -z "$MONTH" ]; then
  echo "YEAR and MONTH must be provided"
  exit 1
fi

mkdir -p ${DST}/${YEAR}/${MONTH}

rsync -av \
  ${SRC}/${YEAR}/${MONTH}/ \
  ${DST}/${YEAR}/${MONTH}/

echo "Finished ${YEAR}/${MONTH}"
