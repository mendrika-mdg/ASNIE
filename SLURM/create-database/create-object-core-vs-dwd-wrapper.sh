#!/bin/bash

# Core thresholds
CORE_0=50.024
CORE_90=79.530
CORE_95=80.744
CORE_98=82.640

# Minimum object size
MIN_PIXELS_CORE=10

YEAR_RAIN=2024

SCRIPT=/home/users/mendrika/ASNIE/SLURM/create-database/create-object-core-vs-dwd.sh

for month in 06 07 08 09; do

  start="${YEAR_RAIN}${month}010000"

  if [ "$month" == "06" ] || [ "$month" == "09" ]; then
    end="${YEAR_RAIN}${month}302345"
  else
    end="${YEAR_RAIN}${month}312345"
  fi

  # Core vs DWD analysis

  sbatch --job-name=core_dwd0_2024_${month}  $SCRIPT "$start" "$end" "$CORE_0"  "$MIN_PIXELS_CORE"
  sbatch --job-name=core_dwd90_2024_${month} $SCRIPT "$start" "$end" "$CORE_90" "$MIN_PIXELS_CORE"
  sbatch --job-name=core_dwd95_2024_${month} $SCRIPT "$start" "$end" "$CORE_95" "$MIN_PIXELS_CORE"
  sbatch --job-name=core_dwd98_2024_${month} $SCRIPT "$start" "$end" "$CORE_98" "$MIN_PIXELS_CORE"

done