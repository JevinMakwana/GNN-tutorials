#!/bin/bash

# Download selected files for run_1 from the AhmedML dataset.
# Required: huggingface_hub CLI
# Install with: pip install -U "huggingface_hub[cli]"

set -euo pipefail

HF_OWNER="neashton"
HF_PREFIX="ahmedml"
REPO_ID="${HF_OWNER}/${HF_PREFIX}"
RUN_ID=1
RUN_DIR="run_${RUN_ID}"

# Local output root
LOCAL_DIR="./ahmed_data"
mkdir -p "$LOCAL_DIR"

if ! command -v huggingface-cli >/dev/null 2>&1; then
    echo "Error: huggingface-cli not found."
    echo "Install it with: pip install -U \"huggingface_hub[cli]\""
    exit 1
fi

echo "Downloading selected files for ${RUN_DIR} into ${LOCAL_DIR}..."

huggingface-cli download "$REPO_ID" \
    --repo-type dataset \
    --local-dir "$LOCAL_DIR" \
    --include "${RUN_DIR}/ahmed_${RUN_ID}.stl" \
    --include "${RUN_DIR}/force_mom_${RUN_ID}.csv" \
    --include "${RUN_DIR}/force_mom_varref_${RUN_ID}.csv" \
    --include "${RUN_DIR}/images/**"

echo "Done. Downloaded files under: ${LOCAL_DIR}/${RUN_DIR}"