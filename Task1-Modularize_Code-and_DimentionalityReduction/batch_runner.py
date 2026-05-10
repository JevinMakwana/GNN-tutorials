#!/usr/bin/env python3
"""
Batch runner: Process 10 runs of the AhmedML dataset through the pipeline.
Iterates over runs 1-10, updates config paths, and runs main.py for each.
Logs results and collects statistics.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

# Script configuration
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
VENV_PYTHON = REPO_ROOT / ".venv" / "Scripts" / "python.exe"
PYTHON_EXE = VENV_PYTHON if VENV_PYTHON.exists() else Path(sys.executable)
DATA_ROOT = REPO_ROOT / "ahmed_data"
OUTPUT_ROOT = REPO_ROOT / "batch_results"
RUNS = list(range(1, 11))  # Runs 1-10
TASK_DIR = SCRIPT_DIR
CONFIG_TEMPLATE = """
INPUT_STL_PATH = "{input_path}"
OUTPUT_VTM_PATH = "{output_vtm}"
OUTPUT_PYG_PATH = "{output_pyg}"
MODEL_NAME = "{model_name}"
"""


def setup_batch_results():
    """Create batch results directory structure."""
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUTPUT_ROOT / "logs").mkdir(exist_ok=True)
    (OUTPUT_ROOT / "outputs").mkdir(exist_ok=True)
    print(f"✓ Batch results directory: {OUTPUT_ROOT.absolute()}")


def validate_input_files():
    """Check that all 10 run directories have required STL files."""
    print("\nValidating input files...")
    missing = []
    for run_num in RUNS:
        stl_path = DATA_ROOT / f"run_{run_num}" / f"ahmed_{run_num}.stl"
        if not stl_path.exists():
            missing.append(f"run_{run_num}: {stl_path}")
        else:
            size_mb = stl_path.stat().st_size / (1024 * 1024)
            print(f"  run_{run_num}: {size_mb:.2f} MB")
    
    if missing:
        print("\nMissing input files:")
        for m in missing:
            print(f"  - {m}")
        return False
    return True


def update_config(run_num: int):
    """Update config.py for the given run number."""
    input_dir = DATA_ROOT / f"run_{run_num}"
    output_dir = OUTPUT_ROOT / "outputs" / f"run_{run_num}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # POSIX-style path string, ideal for cross-platform
    # so convert paths to POSIX-style paths 
    config_content = CONFIG_TEMPLATE.format(
        input_path=(input_dir.absolute().as_posix()),
        output_vtm=((output_dir / f"ahmed_{run_num}.vtm").absolute().as_posix()),
        output_pyg=((output_dir / f"ahmed_{run_num}.pt").absolute().as_posix()),
        model_name=f"ahmed_{run_num}"
    )

    config_path = TASK_DIR / "config.py"
    config_path.write_text(config_content)


def run_pipeline(run_num: int) -> bool:
    """Run main.py for a given run number. Returns True if successful."""
    print(f"\n{'='*60}")
    print(f"Running pipeline for run_{run_num}...")
    print(f"{'='*60}")
    
    log_file = OUTPUT_ROOT / "logs" / f"run_{run_num}.log"
    
    try:
        with open(log_file, 'w') as logf:
            result = subprocess.run(
                [str(PYTHON_EXE), "main.py"],
                capture_output=False,
                text=True,
                timeout=600,  # 10 minutes timeout per run
                stdout=logf,
                stderr=subprocess.STDOUT,
                cwd=str(TASK_DIR)
            )
        
        if result.returncode != 0:
            print(f"  Pipeline failed for run_{run_num} (exit code: {result.returncode})")
            print(f"  See log: {log_file}")
            return False
        
        print(f"  Pipeline succeeded for run_{run_num}")
        return True
    
    except subprocess.TimeoutExpired:
        print(f"  Pipeline timed out for run_{run_num} (>600s)")
        return False
    except Exception as e:
        print(f"  Error running pipeline for run_{run_num}: {e}")
        return False


def validate_output(run_num: int) -> dict:
    """Validate that outputs were created for the given run. Returns stats dict."""
    output_dir = OUTPUT_ROOT / "outputs" / f"run_{run_num}"
    stats = {
        "run": run_num,
        "vtm_exists": False,
        "pt_exists": False,
        "html_exists": False,
        "vtm_size_mb": 0.0,
        "pt_size_mb": 0.0,
    }
    
    vtm_file = output_dir / f"ahmed_{run_num}.vtm"
    pt_file = output_dir / f"ahmed_{run_num}.pt"
    html_file = output_dir / f"ahmed_{run_num}_visualization_interactive.html"
    
    if vtm_file.exists():
        stats["vtm_exists"] = True
        stats["vtm_size_mb"] = vtm_file.stat().st_size / (1024 * 1024)
    
    if pt_file.exists():
        stats["pt_exists"] = True
        stats["pt_size_mb"] = pt_file.stat().st_size / (1024 * 1024)
    
    if html_file.exists():
        stats["html_exists"] = True
    
    return stats


def main():
    """Main batch processing loop."""
    print(f"\n{'='*60}")
    print(f"AhmedML Batch Pipeline Runner (Runs 1-10)")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    # Setup
    setup_batch_results()
    if not validate_input_files():
        print("\nInput validation failed. Exiting.")
        return False
    
    # Process each run
    results = []
    successes = 0
    failures = 0
    
    for run_num in RUNS:
        update_config(run_num)
        success = run_pipeline(run_num)
        
        if success:
            successes += 1
            output_stats = validate_output(run_num)
            results.append({
                "status": "success",
                **output_stats
            })
            print(f"  VTM: {output_stats['vtm_size_mb']:.2f} MB, PT: {output_stats['pt_size_mb']:.2f} MB")
        else:
            failures += 1
            results.append({
                "status": "failed",
                "run": run_num
            })
    
    # Summary report
    print(f"\n{'='*60}")
    print(f"BATCH PROCESSING COMPLETE")
    print(f"{'='*60}")
    print(f"Total runs: {len(RUNS)}")
    print(f"Successes: {successes}")
    print(f"Failures: {failures}")
    print(f"Success rate: {100.0 * successes / len(RUNS):.1f}%")
    
    # Save results to JSON
    results_file = OUTPUT_ROOT / "batch_results.json"
    with open(results_file, 'w') as f:
        json.dump({
                "timestamp": datetime.now().isoformat(),
                "total_runs": len(RUNS),
                "successes": successes,
                "failures": failures,
                "results": results
            }, 
            f,          # The file object to write to 
            indent=2    # Pretty-prints the JSON with 2-space indentation for readability
        )
        
    print(f"\nDetailed results: {results_file}")
    print(f"Logs directory: {(OUTPUT_ROOT / 'logs').absolute()}")
    print(f"Outputs directory: {(OUTPUT_ROOT / 'outputs').absolute()}")
    
    return failures == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
