#!/bin/bash

# Core CTT thresholds
CORE_0=50.024
CORE_90=79.530
CORE_95=80.744
CORE_98=82.640

# Rain thresholds
ROA_90=1.636
ROA_95=2.921
ROA_98=4.886

CRR_90=1.746
CRR_95=2.578
CRR_98=4.365

# Lightning thresholds
LI_0=0.000
LI_50=0.032
LI_90=1.056
LI_95=2.617
LI_98=7.062

# Minimum object sizes
MIN_PIXELS_CORE=10
MIN_PIXELS_RAIN=10
MIN_PIXELS_LI=4

YEAR_RAIN=2024
YEAR_LI=2025

SCRIPT=/home/users/mendrika/ASNIE/SLURM/create-database/create-object-database.sh

for month in 06 07 08 09; do

  start="${YEAR_RAIN}${month}010000"

  if [ "$month" == "06" ] || [ "$month" == "09" ]; then
    end="${YEAR_RAIN}${month}302345"
  else
    end="${YEAR_RAIN}${month}312345"
  fi


  # ---------------------------
  # 2024 products
  # ---------------------------

  # CORE 2024

  sbatch --job-name=core0_2024_${month}  $SCRIPT core $start $end $CORE_0  $MIN_PIXELS_CORE
  sbatch --job-name=core90_2024_${month} $SCRIPT core $start $end $CORE_90 $MIN_PIXELS_CORE
  sbatch --job-name=core95_2024_${month} $SCRIPT core $start $end $CORE_95 $MIN_PIXELS_CORE
  sbatch --job-name=core98_2024_${month} $SCRIPT core $start $end $CORE_98 $MIN_PIXELS_CORE


  # ROA

  sbatch --job-name=roa90_2024_${month} $SCRIPT roa $start $end $ROA_90 $MIN_PIXELS_RAIN
  sbatch --job-name=roa95_2024_${month} $SCRIPT roa $start $end $ROA_95 $MIN_PIXELS_RAIN
  sbatch --job-name=roa98_2024_${month} $SCRIPT roa $start $end $ROA_98 $MIN_PIXELS_RAIN


  # CRR

  sbatch --job-name=crr90_2024_${month} $SCRIPT crr $start $end $CRR_90 $MIN_PIXELS_RAIN
  sbatch --job-name=crr95_2024_${month} $SCRIPT crr $start $end $CRR_95 $MIN_PIXELS_RAIN
  sbatch --job-name=crr98_2024_${month} $SCRIPT crr $start $end $CRR_98 $MIN_PIXELS_RAIN


  # ---------------------------
  # 2025 products
  # ---------------------------

  start_li="${YEAR_LI}${month}010000"

  if [ "$month" == "06" ] || [ "$month" == "09" ]; then
    end_li="${YEAR_LI}${month}302345"
  else
    end_li="${YEAR_LI}${month}312345"
  fi


  # CORE 2025

  sbatch --job-name=core0_2025_${month}  $SCRIPT core $start_li $end_li $CORE_0  $MIN_PIXELS_CORE
  sbatch --job-name=core90_2025_${month} $SCRIPT core $start_li $end_li $CORE_90 $MIN_PIXELS_CORE
  sbatch --job-name=core95_2025_${month} $SCRIPT core $start_li $end_li $CORE_95 $MIN_PIXELS_CORE
  sbatch --job-name=core98_2025_${month} $SCRIPT core $start_li $end_li $CORE_98 $MIN_PIXELS_CORE


  # Lightning

  sbatch --job-name=li0_2025_${month}  $SCRIPT li $start_li $end_li $LI_0  $MIN_PIXELS_LI
  sbatch --job-name=li50_2025_${month} $SCRIPT li $start_li $end_li $LI_50 $MIN_PIXELS_LI
  sbatch --job-name=li90_2025_${month} $SCRIPT li $start_li $end_li $LI_90 $MIN_PIXELS_LI
  sbatch --job-name=li95_2025_${month} $SCRIPT li $start_li $end_li $LI_95 $MIN_PIXELS_LI
  sbatch --job-name=li98_2025_${month} $SCRIPT li $start_li $end_li $LI_98 $MIN_PIXELS_LI


done