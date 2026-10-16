import os
import pandas as pd
from sqlalchemy import create_engine, text

file_path = "data/processed/stop_times_clean.csv"

engine = create_engine(
    os.environ["DATABASE_URL"]
)

with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE public.stop_times"))

    total_rows = 0

    for chunk in pd.read_csv(file_path, dtype=str, chunksize=50000):
        chunk["stop_sequence"] = pd.to_numeric(
            chunk["stop_sequence"], errors="raise"
        ).astype(int)

        chunk.to_sql(
            "stop_times",
            conn,
            schema="public",
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1000
        )
        total_rows += len(chunk)
        print(f"Loaded {total_rows:,} rows")

    count = conn.execute(
        text("SELECT COUNT(*) FROM public.stop_times")
    ).scalar()

print("Rows loaded into PostgreSQL:", count)
