#!/bin/bash

# CTT threshold (Python uses -ctt so 40 means CTT ≤ -40°C)
CORE_THRESHOLD=40

# Lightning thresholds
LI_0=0
LI_50=0.032
LI_90=1.056

# Minimum object sizes
MIN_PIXELS_CORE=8
MIN_PIXELS_LI=4

YEAR=2025

for month in 06 07 08 09; do

  start="${YEAR}${month}010000"

  if [ "$month" == "06" ] || [ "$month" == "09" ]; then
    end="${YEAR}${month}302345"
  else
    end="${YEAR}${month}312345"
  fi

  # LI > 0
  sbatch /home/users/mendrika/ASNIE/SLURM/create-database-core-vs-LI/create-object-database-core-li.sh \
    $start \
    $end \
    $CORE_THRESHOLD \
    $LI_0 \
    $MIN_PIXELS_CORE \
    $MIN_PIXELS_LI

  # LI > 50th percentile
  sbatch /home/users/mendrika/ASNIE/SLURM/create-database-core-vs-LI/create-object-database-core-li.sh \
    $start \
    $end \
    $CORE_THRESHOLD \
    $LI_50 \
    $MIN_PIXELS_CORE \
    $MIN_PIXELS_LI

  # LI > 90th percentile
  sbatch /home/users/mendrika/ASNIE/SLURM/create-database-core-vs-LI/create-object-database-core-li.sh \
    $start \
    $end \
    $CORE_THRESHOLD \
    $LI_90 \
    $MIN_PIXELS_CORE \
    $MIN_PIXELS_LI

done