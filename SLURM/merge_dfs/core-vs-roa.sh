#!/bin/bash

# Core threshold (wavelet power)
THRESH_CORES=(0.0) # important for folder naming

# RoA threshold (98th percentile)
THRESH_ROAS=(4.886)

BASE_PATH="/work/scratch-nopw2/mendrika/ASNIE/final-database/RoA"
SLURM_SCRIPT="/home/users/mendrika/ASNIE/SLURM/merge_dfs/merge_df_objects.sh"

# Submit core jobs
for THRESH_CORE in "${THRESH_CORES[@]}"; do

  THRESH_TAG="thr_${THRESH_CORE}"
  THRESH_TAG=${THRESH_TAG//./p}

  sbatch -J "core-$THRESH_TAG" "$SLURM_SCRIPT" core "$THRESH_TAG" "$BASE_PATH"

done

# Submit RoA jobs
for THRESH_ROA in "${THRESH_ROAS[@]}"; do

  THRESH_TAG="thr_${THRESH_ROA}"
  THRESH_TAG=${THRESH_TAG//./p}

  sbatch -J "roa-$THRESH_TAG" "$SLURM_SCRIPT" roa "$THRESH_TAG" "$BASE_PATH"

done