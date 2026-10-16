from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "processed"
OUTPUT.mkdir(parents=True, exist_ok=True)

# Connect to the local TransitOps PostgreSQL database.
# Update the password if yours is different.
DATABASE_URL = DATABASE_URL = "postgresql+psycopg2://postgres:Simran%402622@localhost:5432/transitops"

engine = create_engine(DATABASE_URL)

CHECKS = {
    "Duplicate route IDs": """
        SELECT COUNT(*) FROM (
            SELECT route_id
            FROM routes
            GROUP BY route_id
            HAVING COUNT(*) > 1
        ) AS duplicates
    """,
    "Trips referencing unknown routes": """
        SELECT COUNT(*)
        FROM trips t
        LEFT JOIN routes r ON t.route_id = r.route_id
        WHERE r.route_id IS NULL
    """,
    "Stop times referencing unknown trips": """
        SELECT COUNT(*)
        FROM stop_times st
        LEFT JOIN trips t ON st.trip_id = t.trip_id
        WHERE t.trip_id IS NULL
    """,
    "Stop times referencing unknown stops": """
        SELECT COUNT(*)
        FROM stop_times st
        LEFT JOIN stops s ON st.stop_id = s.stop_id
        WHERE s.stop_id IS NULL
    """,
}


def main():
    results = []

    with engine.connect() as connection:
        for check_name, query in CHECKS.items():
            failed_records = connection.execute(text(query)).scalar()

            results.append({
                "check": check_name,
                "failed_records": int(failed_records),
                "status": "PASS" if failed_records == 0 else "REVIEW",
            })

    report = pd.DataFrame(results)
    output_file = OUTPUT / "database_validation_report.csv"
    report.to_csv(output_file, index=False)

    print("\nTRANSITOPS DATABASE VALIDATION")
    print("-" * 50)
    print(report.to_string(index=False))
    print(f"\nReport saved to: {output_file}")


if __name__ == "__main__":
    main()