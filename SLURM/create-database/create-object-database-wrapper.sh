#!/bin/bash

# 90th percentile
CORE_90=223.5
ROA_90=1.6357

# 95th percentile
CORE_95=260.1
ROA_95=2.9205

MIN_PIXELS=10

for year in 2020 2021 2022 2023 2024; do
  for month in 06 07 08 09; do

    start="${year}${month}010000"

    if [ "$month" == "06" ] || [ "$month" == "09" ]; then
      end="${year}${month}302345"
    else
      end="${year}${month}312345"
    fi

    # 90th run
    sbatch /home/users/mendrika/ASNIE/SLURM/create-database/create-object-database.sh \
      $start \
      $end \
      $CORE_90 \
      $ROA_90 \
      $MIN_PIXELS

    # 95th run
    sbatch /home/users/mendrika/ASNIE/SLURM/create-database/create-object-database.sh \
      $start \
      $end \
      $CORE_95 \
      $ROA_95 \
      $MIN_PIXELS

  done
done
