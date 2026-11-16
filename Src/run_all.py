
import subprocess
import sys
from pathlib import Path

# Folder containing this script (Src)
script_dir = Path(__file__).resolve().parent

# Main FreshFlow project folder
project_dir = script_dir.parent

# Folder containing all CSV files
data_dir = project_dir / "datasets"

scripts = [
    "generate_operations.py",
    "data_dictionary.py",
    "data_audit.py",
    "data_cleaning.py",
    "metric_calculations.py",
    "statistical_analysis.py",
    "trend_anomaly_analysis.py",
    "discount_analysis.py",
    "anomaly_register.py",
    "scenario_analysis.py",
    "validation_tests.py",
    "final_report.py"
]

print("=" * 65)
print("FRESHFLOW JUICE COMPANY")
print("COMPLETE BUSINESS ANALYTICS PROJECT")
print("=" * 65)

# Check required folders
if not data_dir.exists():
    print("ERROR: datasets folder not found!")
    sys.exit(1)

# Run every script in order
for number, script in enumerate(scripts, start=1):

    script_path = script_dir / script

    print("\n" + "=" * 65)
    print(f"STEP {number}/{len(scripts)}: RUNNING {script}")
    print("=" * 65)

    if not script_path.exists():
        print(f"ERROR: {script} was not found!")
        sys.exit(1)

    try:
        subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(data_dir),
            check=True
        )

        print(f"\nSUCCESS: {script} completed!")

    except subprocess.CalledProcessError as error:
        print(f"\nERROR: {script} failed!")
        print(f"Exit code: {error.returncode}")
        print("Execution stopped.")
        sys.exit(error.returncode)

print("\n" + "=" * 65)
print("ALL PROJECT SCRIPTS EXECUTED SUCCESSFULLY!")
print("=" * 65)

print("\nFinal report:")
print(data_dir / "freshflow_final_report.txt")

print("\nFRESHFLOW BUSINESS ANALYTICS PROJECT COMPLETED!")
