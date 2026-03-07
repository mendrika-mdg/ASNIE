#!/bin/bash

BASE_PATH="/gws/ssde/j25b/swift/mendrika/asnie/database"
SLURM_SCRIPT="/home/users/mendrika/ASNIE/SLURM/merge_dfs/merge_df_objects.sh"

# -------------------------
# Threshold lists
# -------------------------

CORE_THRESHOLDS=(50.024 79.53 80.744 82.64)

ROA_THRESHOLDS=(1.636 2.921 4.886)

CRR_THRESHOLDS=(1.746 2.578 4.365)

LI_THRESHOLDS=(0.0 0.032 1.056 2.617 7.062)

# -------------------------
# 2024 products
# -------------------------

YEAR=2024

for THRESH in "${CORE_THRESHOLDS[@]}"; do

  TAG="thr_${THRESH}"
  TAG=${TAG//./p}

  sbatch -J "merge-core-${YEAR}-${TAG}" \
    "$SLURM_SCRIPT" core "$YEAR" "$TAG" "$BASE_PATH"

done


for THRESH in "${ROA_THRESHOLDS[@]}"; do

  TAG="thr_${THRESH}"
  TAG=${TAG//./p}

  sbatch -J "merge-roa-${YEAR}-${TAG}" \
    "$SLURM_SCRIPT" roa "$YEAR" "$TAG" "$BASE_PATH"

done


for THRESH in "${CRR_THRESHOLDS[@]}"; do

  TAG="thr_${THRESH}"
  TAG=${TAG//./p}

  sbatch -J "merge-crr-${YEAR}-${TAG}" \
    "$SLURM_SCRIPT" crr "$YEAR" "$TAG" "$BASE_PATH"

done


# -------------------------
# 2025 products
# -------------------------

YEAR=2025

for THRESH in "${CORE_THRESHOLDS[@]}"; do

  TAG="thr_${THRESH}"
  TAG=${TAG//./p}

  sbatch -J "merge-core-${YEAR}-${TAG}" \
    "$SLURM_SCRIPT" core "$YEAR" "$TAG" "$BASE_PATH"

done


for THRESH in "${LI_THRESHOLDS[@]}"; do

  TAG="thr_${THRESH}"
  TAG=${TAG//./p}

  sbatch -J "merge-li-${YEAR}-${TAG}" \
    "$SLURM_SCRIPT" li "$YEAR" "$TAG" "$BASE_PATH"

done