#!/bin/bash

CORE_THRESHOLD=0
CRR_THRESHOLD=4.365

MIN_PIXELS=10

for year in 2024; do
  for month in 06 07 08 09; do

    start="${year}${month}010000"

    if [ "$month" == "06" ] || [ "$month" == "09" ]; then
      end="${year}${month}302345"
    else
      end="${year}${month}312345"
    fi

    sbatch /home/users/mendrika/ASNIE/SLURM/create-database-core-vs-crr/create-object-database.sh \
      $start \
      $end \
      $CORE_THRESHOLD \
      $CRR_THRESHOLD \
      $MIN_PIXELS

  done
done