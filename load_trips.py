import os
import pandas as pd
from sqlalchemy import create_engine, text

file_path = "data/processed/trips_clean.csv"

df = pd.read_csv(file_path, dtype=str)
print("CSV rows:", len(df))
print("Duplicate trip IDs:", df["trip_id"].duplicated().sum())

engine = create_engine(
    os.environ["DATABASE_URL"]
)

with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE public.trips"))

    df.to_sql(
        "trips",
        conn,
        schema="public",
        if_exists="append",
        index=False,
        chunksize=5000,
        method="multi"
    )

    count = conn.execute(
        text("SELECT COUNT(*) FROM public.trips")
    ).scalar()

print("Rows loaded into PostgreSQL:", count)
