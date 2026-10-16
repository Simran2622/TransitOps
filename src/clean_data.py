
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "gtfs"
PROCESSED = ROOT / "data" / "processed"

PROCESSED.mkdir(parents=True, exist_ok=True)


def load_csv(filename):
    """Load a GTFS CSV file."""
    return pd.read_csv(RAW / filename, low_memory=False)


def clean_routes():
    df = load_csv("routes.txt")

    # Remove duplicate route IDs and rows without a route ID.
    df = df.dropna(subset=["route_id"])
    df = df.drop_duplicates(subset=["route_id"])

    # Keep route IDs as strings and standardize route names.
    df["route_id"] = df["route_id"].astype(str).str.strip()

    if "route_long_name" in df.columns:
        df["route_long_name"] = (
            df["route_long_name"].astype("string").str.strip()
        )

    # route_short_name is missing in this source, so don't invent values.
    return df


def clean_stops():
    df = load_csv("stops.txt")

    df = df.dropna(subset=["stop_id"])
    df = df.drop_duplicates(subset=["stop_id"])

    df["stop_id"] = df["stop_id"].astype(str).str.strip()

    # Convert coordinates to numeric values.
    df["stop_lat"] = pd.to_numeric(df["stop_lat"], errors="coerce")
    df["stop_lon"] = pd.to_numeric(df["stop_lon"], errors="coerce")

    # Remove rows with invalid coordinates.
    valid_coordinates = (
        df["stop_lat"].between(-90, 90)
        & df["stop_lon"].between(-180, 180)
    )
    df = df.loc[valid_coordinates].copy()

    if "stop_name" in df.columns:
        df["stop_name"] = df["stop_name"].astype("string").str.strip()

    return df


def clean_trips():
    df = load_csv("trips.txt")

    df = df.dropna(subset=["trip_id", "route_id"])
    df = df.drop_duplicates(subset=["trip_id"])

    # IDs are identifiers, not numbers.
    for column in ["trip_id", "route_id", "service_id"]:
        if column in df.columns:
            df[column] = df[column].astype(str).str.strip()

    return df


def clean_stop_times():
    df = load_csv("stop_times.txt")

    df = df.dropna(subset=["trip_id", "stop_id", "stop_sequence"])

    df["trip_id"] = df["trip_id"].astype(str).str.strip()
    df["stop_id"] = df["stop_id"].astype(str).str.strip()

    df["stop_sequence"] = pd.to_numeric(
        df["stop_sequence"], errors="coerce"
    )

    df = df.dropna(subset=["stop_sequence"])
    df = df[df["stop_sequence"] >= 0]

    # Remove duplicate trip/sequence combinations.
    df = df.drop_duplicates(
        subset=["trip_id", "stop_sequence"]
    )

    # Sort stops in their sequence within each trip.
    df = df.sort_values(
        ["trip_id", "stop_sequence"]
    ).reset_index(drop=True)

    return df


def save_dataset(df, filename):
    output_path = PROCESSED / filename
    df.to_csv(output_path, index=False)
    print(f"Saved {filename}: {len(df):,} rows")


def main():
    print("Starting TransitOps cleaning pipeline...\n")

    routes = clean_routes()
    stops = clean_stops()
    trips = clean_trips()
    stop_times = clean_stop_times()

    save_dataset(routes, "routes_clean.csv")
    save_dataset(stops, "stops_clean.csv")
    save_dataset(trips, "trips_clean.csv")
    save_dataset(stop_times, "stop_times_clean.csv")

    print("\nCleaning pipeline completed.")
    print(f"Processed files are saved in: {PROCESSED}")


if __name__ == "__main__":
    main()
