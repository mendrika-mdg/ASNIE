#!/bin/bash

# Core threshold (CTT ≤ -40°C because Python uses -ctt)
THRESH_CORES=(40.0)

# MTG Lightning thresholds
THRESH_LIS=(0.0 0.032 1.056)

BASE_PATH="/work/scratch-nopw2/mendrika/ASNIE/final-database/LI"
SLURM_SCRIPT="/home/users/mendrika/ASNIE/SLURM/merge_dfs/merge_df_objects.sh"

# Submit core merge jobs
for THRESH_CORE in "${THRESH_CORES[@]}"; do

  THRESH_TAG="thr_${THRESH_CORE}"
  THRESH_TAG=${THRESH_TAG//./p}

  sbatch -J "core-$THRESH_TAG" "$SLURM_SCRIPT" core "$THRESH_TAG" "$BASE_PATH"

done

# Submit LI merge jobs
for THRESH_LI in "${THRESH_LIS[@]}"; do

  THRESH_TAG="thr_${THRESH_LI}"
  THRESH_TAG=${THRESH_TAG//./p}

  sbatch -J "li-$THRESH_TAG" "$SLURM_SCRIPT" li "$THRESH_TAG" "$BASE_PATH"

done