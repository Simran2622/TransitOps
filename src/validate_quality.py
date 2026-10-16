
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "raw" / "gtfs"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)


def main():
    print("Starting TransitOps data-quality checks...")

    results = []

    # 1. Check missing and duplicate IDs.
    id_checks = [
        ("routes.txt", "route_id"),
        ("stops.txt", "stop_id"),
        ("trips.txt", "trip_id"),
        ("stop_times.txt", "trip_id"),
    ]

    for filename, column in id_checks:
        df = pd.read_csv(DATA / filename, usecols=[column], dtype=str)

        missing = int(df[column].isna().sum())
        duplicates = int(df[column].duplicated().sum())

        results.append({
            "file": filename,
            "check": f"Missing {column}",
            "records_checked": len(df),
            "failed_records": missing,
            "status": "PASS" if missing == 0 else "REVIEW",
        })

        # Duplicate IDs are expected in stop_times because a trip
        # appears once for each stop. Check uniqueness only for
        # routes, stops, and trips.
        if filename != "stop_times.txt":
            results.append({
                "file": filename,
                "check": f"Duplicate {column}",
                "records_checked": len(df),
                "failed_records": duplicates,
                "status": "PASS" if duplicates == 0 else "REVIEW",
            })

    # 2. Validate stop coordinates.
    stops = pd.read_csv(
        DATA / "stops.txt",
        usecols=["stop_lat", "stop_lon"]
    )

    lat = pd.to_numeric(stops["stop_lat"], errors="coerce")
    lon = pd.to_numeric(stops["stop_lon"], errors="coerce")

    invalid_coordinates = (
        lat.isna()
        | lon.isna()
        | ~lat.between(-90, 90)
        | ~lon.between(-180, 180)
    )

    results.append({
        "file": "stops.txt",
        "check": "Invalid coordinates",
        "records_checked": len(stops),
        "failed_records": int(invalid_coordinates.sum()),
        "status": "PASS" if not invalid_coordinates.any() else "REVIEW",
    })

    # 3. Check stop sequence values.
    sequences = pd.read_csv(
        DATA / "stop_times.txt",
        usecols=["stop_sequence"],
        dtype=str
    )

    sequence_values = pd.to_numeric(
        sequences["stop_sequence"], errors="coerce"
    )

    invalid_sequences = (
        sequence_values.isna() | (sequence_values < 0)
    )

    results.append({
        "file": "stop_times.txt",
        "check": "Invalid stop sequence",
        "records_checked": len(sequences),
        "failed_records": int(invalid_sequences.sum()),
        "status": "PASS" if not invalid_sequences.any() else "REVIEW",
    })

    report = pd.DataFrame(results)
    output_file = OUT / "data_quality_validation_report.csv"
    report.to_csv(output_file, index=False)

    print("\nDATA-QUALITY VALIDATION REPORT")
    print(report.to_string(index=False))
    print(f"\nReport saved to: {output_file}")


if __name__ == "__main__":
    main()
