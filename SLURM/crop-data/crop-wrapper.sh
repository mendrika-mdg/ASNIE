#!/bin/bash

SCRIPT=/home/users/mendrika/ASNIE/SLURM/crop-data/crop.sh

for YEAR in 2020 2021 2022 2023 2024; do

    for month in {01..12}; do

        start="${YEAR}${month}010000"

        last_day=$(cal $month $YEAR | awk 'NF {DAYS = $NF}; END {print DAYS}')

        end="${YEAR}${month}${last_day}2345"

        sbatch --job-name=crop_core_${YEAR}_${month} \
               $SCRIPT "$start" "$end"

    done

done