
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "raw" / "gtfs"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)


def read_ids(filename, column):
    """Load unique, non-null IDs from a GTFS file."""
    values = pd.read_csv(
        DATA / filename,
        usecols=[column],
        dtype=str
    )[column].dropna()

    return set(values)


def main():
    print("Starting TransitOps referential-integrity checks...")

    # Load reference IDs.
    route_ids = read_ids("routes.txt", "route_id")
    trip_ids = read_ids("trips.txt", "trip_id")
    stop_ids = read_ids("stops.txt", "stop_id")

    # Validate trips against routes.
    trips = pd.read_csv(DATA / "trips.txt", dtype=str)

    trip_count = len(trips)
    invalid_trip_routes = int(
        (~trips["route_id"].isin(route_ids)).sum()
    )

    print(f"DEBUG: trips DataFrame shape = {trips.shape}")
    print(f"DEBUG: trip_count = {trip_count}")

    # Validate stop-time references in chunks.
    stop_time_rows = 0
    invalid_stop_count = 0
    invalid_trip_count = 0

    for chunk in pd.read_csv(
        DATA / "stop_times.txt",
        dtype=str,
        chunksize=100_000
    ):
        chunk_rows = len(chunk)
        stop_time_rows += chunk_rows

        invalid_stop_count += int(
            (~chunk["stop_id"].isin(stop_ids)).sum()
        )
        invalid_trip_count += int(
            (~chunk["trip_id"].isin(trip_ids)).sum()
        )

    print(f"DEBUG: stop_time_rows = {stop_time_rows}")

    # Build the final report.
    results = pd.DataFrame([
        {
            "check": "Trips referencing unknown routes",
            "records_checked": trip_count,
            "failed_records": invalid_trip_routes,
        },
        {
            "check": "Stop times referencing unknown stops",
            "records_checked": stop_time_rows,
            "failed_records": invalid_stop_count,
        },
        {
            "check": "Stop times referencing unknown trips",
            "records_checked": stop_time_rows,
            "failed_records": invalid_trip_count,
        },
    ])

    results["status"] = results["failed_records"].apply(
        lambda count: "PASS" if count == 0 else "REVIEW"
    )

    output_file = OUT / "referential_integrity_report_v2.csv"
    results.to_csv(output_file, index=False)

    # Read back the new report to verify the saved values.
    saved_results = pd.read_csv(output_file)

    print("\nVERIFIED SAVED REPORT")
    print(saved_results.to_string(index=False))

    print("\nREFERENTIAL INTEGRITY REPORT")
    print(results.to_string(index=False))
    print(f"\nReport saved to: {output_file}")


if __name__ == "__main__":
    main()
