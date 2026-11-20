#!/bin/bash

TS_THRESHOLD=0.0001

# Lightning thresholds
LI_0=0.00001
LI_50=0.032
LI_90=1.056

# Minimum object sizes
MIN_PIXELS_TS=2
MIN_PIXELS_LI=2

YEAR=2025

for DOMAIN in WA CA EA SA; do

  if [ "$DOMAIN" == "WA" ]; then
    MONTHS="06 07 08 09"

  elif [ "$DOMAIN" == "CA" ]; then
    MONTHS="03 04 05 09 10 11"

  elif [ "$DOMAIN" == "EA" ]; then
    MONTHS="03 04 05 10 11 12"

  elif [ "$DOMAIN" == "SA" ]; then
    MONTHS="01 02 03 04 10 11 12"
  fi

  for month in $MONTHS; do

    start="${YEAR}${month}010000"

    if [ "$month" == "02" ]; then

      if (( (YEAR % 400 == 0) || (YEAR % 4 == 0 && YEAR % 100 != 0) )); then
        end="${YEAR}${month}292345"
      else
        end="${YEAR}${month}282345"
      fi

    elif [ "$month" == "04" ] || \
         [ "$month" == "06" ] || \
         [ "$month" == "09" ] || \
         [ "$month" == "11" ]; then

      end="${YEAR}${month}302345"

    else
      end="${YEAR}${month}312345"

    fi

    # LI > 0
    sbatch /home/users/mendrika/ASNIE/Analysis/paper/create-database-dwdts-vs-li/create-object-database.sh \
      $start \
      $end \
      $TS_THRESHOLD \
      $LI_0 \
      $MIN_PIXELS_TS \
      $MIN_PIXELS_LI \
      $DOMAIN

    # LI >= 50th percentile
    sbatch /home/users/mendrika/ASNIE/Analysis/paper/create-database-dwdts-vs-li/create-object-database.sh \
      $start \
      $end \
      $TS_THRESHOLD \
      $LI_50 \
      $MIN_PIXELS_TS \
      $MIN_PIXELS_LI \
      $DOMAIN

    # LI >= 90th percentile
    sbatch /home/users/mendrika/ASNIE/Analysis/paper/create-database-dwdts-vs-li/create-object-database.sh \
      $start \
      $end \
      $TS_THRESHOLD \
      $LI_90 \
      $MIN_PIXELS_TS \
      $MIN_PIXELS_LI \
      $DOMAIN

  done

done