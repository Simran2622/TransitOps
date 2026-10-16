
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "raw" / "gtfs"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)


def main():
    print("Starting trip-sequence validation...")

    # Load only the columns needed for validation.
    stop_times = pd.read_csv(
        DATA / "stop_times.txt",
        usecols=["trip_id", "stop_sequence"],
        dtype={"trip_id": str},
    )

    stop_times["stop_sequence"] = pd.to_numeric(
        stop_times["stop_sequence"], errors="coerce"
    )

    results = []

    # Check whether a trip has duplicate stop-sequence numbers.
    duplicate_mask = stop_times.duplicated(
        subset=["trip_id", "stop_sequence"],
        keep=False,
    )

    duplicate_count = int(duplicate_mask.sum())

    results.append({
        "check": "Duplicate stop sequence within trip",
        "records_checked": len(stop_times),
        "failed_records": duplicate_count,
        "status": "PASS" if duplicate_count == 0 else "REVIEW",
    })

    # Check that each trip has at least one stop-time record.
    stops_per_trip = stop_times.groupby("trip_id").size()
    trips_without_stops = int((stops_per_trip == 0).sum())

    results.append({
        "check": "Trips without stop-time records",
        "records_checked": stops_per_trip.size,
        "failed_records": trips_without_stops,
        "status": "PASS" if trips_without_stops == 0 else "REVIEW",
    })

    # Check for gaps in each trip's stop sequence.
    # GTFS sequences can start at values other than 1, so we check
    # consecutive ordering rather than requiring a sequence to start at 1.
    ordered = stop_times.sort_values(
        ["trip_id", "stop_sequence"],
        na_position="last",
    )

    sequence_diffs = ordered.groupby("trip_id")["stop_sequence"].diff()

    # A gap is a difference greater than 1 between adjacent sequence values.
    gap_mask = sequence_diffs > 1
    gap_count = int(gap_mask.sum())

    results.append({
        "check": "Gaps in stop sequence",
        "records_checked": len(stop_times),
        "failed_records": gap_count,
        "status": "PASS" if gap_count == 0 else "REVIEW",
    })

    report = pd.DataFrame(results)

    output_file = OUT / "trip_sequence_validation_report.csv"
    report.to_csv(output_file, index=False)

    print("\nTRIP-SEQUENCE VALIDATION REPORT")
    print(report.to_string(index=False))
    print(f"\nReport saved to: {output_file}")


if __name__ == "__main__":
    main()
