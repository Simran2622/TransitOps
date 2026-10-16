import os
from sqlalchemy import create_engine, text

engine = create_engine(
    os.environ["DATABASE_URL"]
)

tables = ["routes", "stops", "trips", "stop_times"]

with engine.connect() as conn:
    print("\nTRANSITOPS DATABASE VALIDATION")
    print("-" * 40)

    for table in tables:
        count = conn.execute(
            text(f"SELECT COUNT(*) FROM public.{table}")
        ).scalar()
        print(f"{table:<15} {count:>12,} rows")

