#!/bin/bash

SCRIPT=/home/users/mendrika/ASNIE/SLURM/crop-data/crop.sh

for YEAR in 2023 2024; do

    if [ "$YEAR" -eq 2023 ]; then
        months=$(seq -w 12 12)
    elif [ "$YEAR" -eq 2024 ]; then
        months=$(seq -w 01 10)
    fi

    for month in $months; do

        start="${YEAR}${month}010000"

        last_day=$(cal $month $YEAR | awk 'NF {DAYS = $NF}; END {print DAYS}')

        end="${YEAR}${month}${last_day}2345"

        sbatch --job-name=crop_crr_${YEAR}_${month} \
               $SCRIPT "$start" "$end"

    done

done