$ErrorActionPreference = 'Stop'

# Download selected files for runs 1-10 from the AhmedML dataset.
# Required: huggingface_hub CLI
# Install with: pip install -U "huggingface_hub[cli]"

$HF_OWNER = 'neashton'
$HF_PREFIX = 'ahmedml'
$REPO_ID = "$HF_OWNER/$HF_PREFIX"
$START_RUN = 1
$END_RUN = 10

$LOCAL_DIR = '.\ahmed_data'
New-Item -ItemType Directory -Path $LOCAL_DIR -Force | Out-Null

$hfCli = Get-Command huggingface-cli -ErrorAction SilentlyContinue
if (-not $hfCli) {
    throw 'huggingface-cli not found. Install with: pip install -U "huggingface_hub[cli]"'
}

Write-Host "Downloading runs $START_RUN-$END_RUN into $LOCAL_DIR..."

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

for ($runNum = $START_RUN; $runNum -le $END_RUN; $runNum++) {
    $runDir = "run_$runNum"
    Write-Host "Downloading $runDir..."

    # Download STL and CSV files.
    Download-One -RemotePath "$runDir/ahmed_$runNum.stl"
    Download-One -RemotePath "$runDir/force_mom_$runNum.csv"
    Download-One -RemotePath "$runDir/force_mom_varref_$runNum.csv"

    # Download images folder.
    $imageArgs = @(
        'download',
        $REPO_ID,
        '--repo-type', 'dataset',
        '--local-dir', $LOCAL_DIR,
        '--include', "$runDir/images/**"
    )
    & huggingface-cli @imageArgs

    # Validate required files exist.
    $runLocalDir = Join-Path $LOCAL_DIR $runDir
    $requiredFiles = @(
        (Join-Path $runLocalDir "ahmed_$runNum.stl"),
        (Join-Path $runLocalDir "force_mom_$runNum.csv"),
        (Join-Path $runLocalDir "force_mom_varref_$runNum.csv")
    )

    foreach ($file in $requiredFiles) {
        if (-not (Test-Path -Path $file -PathType Leaf)) {
            throw "Expected file missing for $runDir : $file"
        }
    }
}

Write-Host "Done. Downloaded runs $START_RUN-$END_RUN under: $LOCAL_DIR"