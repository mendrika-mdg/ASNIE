#!/bin/bash

THRESH_CORES=(20 50)
THRESH_ROAS=(0.6617 1.0261 1.6357 2.9205)
MIN_PIXELS=10

for year in 2020 2021 2022 2023 2024; do
  for month in 06 07 08 09; do

    start="${year}${month}010000"

    if [ "$month" == "06" ] || [ "$month" == "09" ]; then
      end="${year}${month}302345"
    else
      end="${year}${month}312345"
    fi

    for THRESH_CORE in "${THRESH_CORES[@]}"; do
      for THRESH_ROA in "${THRESH_ROAS[@]}"; do

        sbatch /home/users/mendrika/ASNIE/SLURM/create-database/create-object-database.sh \
          $start \
          $end \
          $THRESH_CORE \
          $THRESH_ROA \
          $MIN_PIXELS

      done
    done

  done
done
