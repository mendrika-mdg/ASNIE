#!/bin/bash

ROA_THRESHOLD=10
MIN_PIXELS=2

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

  for year in {2023..2024}; do
    for month in $MONTHS; do

      start="${year}${month}010000"

      if [ "$month" == "02" ]; then

        if (( (year % 400 == 0) || (year % 4 == 0 && year % 100 != 0) )); then
          end="${year}${month}292345"
        else
          end="${year}${month}282345"
        fi

      elif [ "$month" == "04" ] || \
           [ "$month" == "06" ] || \
           [ "$month" == "09" ] || \
           [ "$month" == "11" ]; then

        end="${year}${month}302345"

      else
        end="${year}${month}312345"

      fi

      sbatch /home/users/mendrika/ASNIE/Analysis/paper/create-database-rdt-vs-roa/create-object-database.sh \
        $start \
        $end \
        $ROA_THRESHOLD \
        $MIN_PIXELS \
        $DOMAIN

    done
  done

done