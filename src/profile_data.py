
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw" / "gtfs"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FILES = [
    "routes.txt",
    "stops.txt",
    "trips.txt",
    "stop_times.txt",
    "calendar.txt",
]


def profile_file(file_name):
    path = DATA_DIR / file_name
    total_rows = 0
    missing_counts = None

    for chunk in pd.read_csv(path, chunksize=100_000):
        total_rows += len(chunk)
        counts = chunk.isna().sum()

        if missing_counts is None:
            missing_counts = counts
        else:
            missing_counts = missing_counts.add(counts, fill_value=0)

    results = []

    for column, count in missing_counts.items():
        count = int(count)
        results.append({
            "table": file_name.replace(".txt", ""),
            "column": column,
            "row_count": total_rows,
            "missing_count": count,
            "missing_percentage": round(count / total_rows * 100, 2),
        })

    return results


def main():
    all_results = []

    for file_name in FILES:
        print(f"Checking {file_name}...")
        all_results.extend(profile_file(file_name))

    report = pd.DataFrame(all_results)
    output_path = OUTPUT_DIR / "missing_values_report.csv"
    report.to_csv(output_path, index=False)

    issues = report[report["missing_count"] > 0].sort_values(
        "missing_percentage", ascending=False
    )

    print("\nMISSING-VALUE SUMMARY")
    if issues.empty:
        print("No missing values found.")
    else:
        print(issues[
            ["table", "column", "missing_count", "missing_percentage"]
        ].to_string(index=False))

    print(f"\nReport saved to: {output_path}")


if __name__ == "__main__":
    main()
