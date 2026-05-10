$ErrorActionPreference = 'Stop'

# Download selected files for run_1 from the AhmedML dataset.
# Required: huggingface_hub CLI
# Install with: pip install -U "huggingface_hub[cli]"

$HF_OWNER = 'neashton'
$HF_PREFIX = 'ahmedml'
$REPO_ID = "$HF_OWNER/$HF_PREFIX"
$RUN_ID = 1
$RUN_DIR = "run_$RUN_ID"

$LOCAL_DIR = '.\ahmed_data'
New-Item -ItemType Directory -Path $LOCAL_DIR -Force | Out-Null

$hfCli = Get-Command huggingface-cli -ErrorAction SilentlyContinue
if (-not $hfCli) {
    throw 'huggingface-cli not found. Install with: pip install -U "huggingface_hub[cli]"'
}

Write-Host "Downloading selected files for $RUN_DIR into $LOCAL_DIR..."

function Download-One {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RemotePath
    )

    $args = @(
        'download',
        $REPO_ID,
        $RemotePath,
        '--repo-type', 'dataset',
        '--local-dir', $LOCAL_DIR
    )

    & huggingface-cli @args
}

# Download exact files first.
Download-One -RemotePath "$RUN_DIR/ahmed_$RUN_ID.stl"
Download-One -RemotePath "$RUN_DIR/force_mom_$RUN_ID.csv"
Download-One -RemotePath "$RUN_DIR/force_mom_varref_$RUN_ID.csv"

# Download full images folder.
$imageArgs = @(
    'download',
    $REPO_ID,
    '--repo-type', 'dataset',
    '--local-dir', $LOCAL_DIR,
    '--include', "$RUN_DIR/images/**"
)
& huggingface-cli @imageArgs

$runLocalDir = Join-Path $LOCAL_DIR $RUN_DIR
$requiredFiles = @(
    (Join-Path $runLocalDir "ahmed_$RUN_ID.stl"),
    (Join-Path $runLocalDir "force_mom_$RUN_ID.csv"),
    (Join-Path $runLocalDir "force_mom_varref_$RUN_ID.csv")
)

foreach ($file in $requiredFiles) {
    if (-not (Test-Path -Path $file -PathType Leaf)) {
        throw "Expected file missing after download: $file"
    }
}

Write-Host "Done. Downloaded files under: $LOCAL_DIR/$RUN_DIR"