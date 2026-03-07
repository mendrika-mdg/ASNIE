#!/bin/bash

# Core threshold (wavelet power)
THRESH_CORES=(0.0)

# CRR threshold (98th percentile)
THRESH_CRRS=(4.365)

BASE_PATH="/work/scratch-nopw2/mendrika/ASNIE/final-database/CRR"
SLURM_SCRIPT="/home/users/mendrika/ASNIE/SLURM/merge_dfs/merge_df_objects.sh"

# Submit core jobs
for THRESH_CORE in "${THRESH_CORES[@]}"; do

  THRESH_TAG="thr_${THRESH_CORE}"
  THRESH_TAG=${THRESH_TAG//./p}

  sbatch -J "core-$THRESH_TAG" "$SLURM_SCRIPT" core "$THRESH_TAG" "$BASE_PATH"

done

# Submit CRR jobs
for THRESH_CRR in "${THRESH_CRRS[@]}"; do

  THRESH_TAG="thr_${THRESH_CRR}"
  THRESH_TAG=${THRESH_TAG//./p}

  sbatch -J "crr-$THRESH_TAG" "$SLURM_SCRIPT" crr "$THRESH_TAG" "$BASE_PATH"

done