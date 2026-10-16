# TransitOps — Public Transit Data Analytics

## Overview
TransitOps is a data analytics project that processes public transit GTFS data, validates data quality, stores transit records in PostgreSQL, and provides reusable SQL analytics views for reporting in Power BI.

## Objectives
- Build a structured data-cleaning and validation workflow.
- Store transit routes, stops, trips, and stop-time records in PostgreSQL.
- Validate record integrity and key relationships.
- Create reusable SQL views for operational analysis.
- Visualize route activity and stop coverage in Power BI.

## Technology Stack
- **Language:** Python
- **Data Processing:** pandas, NumPy
- **Database:** PostgreSQL
- **Database Connectivity:** SQLAlchemy, psycopg2
- **Analytics:** SQL, reusable database views
- **Visualization:** Power BI
- **Source Data:** GTFS transit files

## Data Pipeline
1. Load and profile the source GTFS data.
2. Clean routes, stops, trips, and stop-time records.
3. Load the cleaned records into PostgreSQL.
4. Run data-quality and referential-integrity checks.
5. Create SQL views for route activity, stop activity, and route coverage.
6. Connect Power BI to PostgreSQL to build an analytics dashboard.

## Analytics Views
- `vw_trips_per_route` — trip counts by route.
- `vw_stop_activity` — scheduled stop-time events by stop.
- `vw_average_stops_per_trip` — average number of stops per trip.
- `vw_trips_by_route_type` — trips grouped by GTFS route type.
- `vw_route_stop_coverage` — distinct stops served by each route.

## Data Quality
The validation workflow checks missing or duplicate identifiers, invalid stop coordinates, invalid stop sequences, and relationships between trips, routes, stops, and stop times.

The current source data has limitations, including missing route short names and missing trip shape identifiers. These are source-data limitations and are not artificially filled.

## Project Structure
```text
TransitOps/
├── data/
│   ├── raw/
│   └── processed/
├── src/
├── sql/
├── tests/
├── docs/
├── powerbi/
├── requirements.txt
└── README.md
```

## Running the Project
1. Install Python 3.11 or compatible.
2. Create and activate a virtual environment.
3. Install dependencies using `pip install -r requirements.txt`.
4. Configure PostgreSQL locally and create the `transitops` database.
5. Run the profiling, cleaning, loading, and validation scripts in the appropriate order.
6. Execute the SQL scripts in pgAdmin or another PostgreSQL client.
7. Open the Power BI report and connect it to your PostgreSQL database.

## Current Status
Python data profiling, cleaning, PostgreSQL loading, validation, and SQL analytics views have been implemented. The Power BI dashboard is being finalized.

## Future Improvements
- Add automated tests and pipeline orchestration.
- Add incremental data loading and monitoring.
- Explore cloud data storage and deployment.
