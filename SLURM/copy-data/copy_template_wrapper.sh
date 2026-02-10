#!/bin/bash

for year in 2020 2021 2022 2023 2024; do
  for month in 06 07 08 09; do
    sbatch /home/users/mendrika/ASNIE/SLURM/copy-data/copy_template.sh $year $month
  done
done
