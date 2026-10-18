# TransitOps — Public Transit Data Analytics

## Overview

TransitOps is a data analytics project that processes public transit GTFS data, validates data quality, stores transit records in PostgreSQL, and provides reusable SQL analytics views for Power BI reporting.

## Objectives

- Clean and profile GTFS transit data.
- Store routes, stops, trips, and stop-time records in PostgreSQL.
- Validate record integrity and relationships.
- Build reusable SQL analytics views.
- Visualize scheduled transit activity and route coverage in Power BI.

## Technology Stack

- **Programming:** Python
- **Data Processing:** pandas, NumPy
- **Database:** PostgreSQL
- **Database Connectivity:** SQLAlchemy, psycopg
- **Analytics:** SQL and database views
- **Visualization:** Power BI
- **Source Data:** GTFS transit files

## Data Pipeline

1. Profile the source GTFS data.
2. Clean routes, stops, trips, and stop-time records.
3. Load cleaned datasets into PostgreSQL.
4. Run data-quality and referential-integrity checks.
5. Create SQL analytics views.
6. Connect Power BI to PostgreSQL for reporting.

## Analytics Views

- `vw_trips_per_route` — Trip counts by route.
- `vw_stop_activity` — Scheduled stop-time events by stop.
- `vw_average_stops_per_trip` — Average number of stops per trip.
- `vw_trips_by_route_type` — Trips grouped by GTFS route type.
- `vw_route_stop_coverage` — Distinct stops represented per route.

## Data Quality and Validation

The project includes checks for missing or duplicate identifiers, invalid stop coordinates, invalid stop sequences, and relationships between routes, trips, stops, and stop-time records.

### Verified PostgreSQL Record Counts

| Dataset | Records |
|---|---:|
| Routes | 2,403 |
| Stops | 10,559 |
| Trips | 89,393 |
| Stop-time records | 3,724,320 |

### Validation Results

- Executed route checks found no missing or duplicate route identifiers.
- No trips reference missing routes.
- The total from `vw_trips_per_route` matches the 89,393 records in the `trips` table.
- The independently calculated average stops per trip is **41.66**, matching the analytics view.
- The 10,559 distinct stops referenced in `stop_times` match the number of records in `vw_stop_activity`.

All routes in the current database have GTFS `route_type = 3`. This result has not yet been independently verified against the original GTFS source files.

These checks validate the conditions listed above; they do not establish that every possible data-quality issue has been eliminated.

## Power BI Dashboard

The dashboard presents key public transit metrics and visualizations:

- Total routes
- Total trips
- Average stops per trip
- Stop activity based on scheduled stop-time events
- Route stop coverage
- Trips by route

## Project Structure

```text
TransitOps/
├── data/
│   ├── raw/
│   └── processed/
├── src/
├── sql/
├── reports/
├── powerbi/
├── requirements.txt
└── README.md
```

## Running the Project

1. Install Python 3.11 or a compatible version.
2. Create and activate a virtual environment.
3. Install dependencies using `pip install -r requirements.txt`.
4. Configure PostgreSQL and create the `transitops` database.
5. Run the profiling, cleaning, and loading scripts in the appropriate order.
6. Execute the SQL scripts against PostgreSQL.
7. Open the Power BI report and configure its database connection.

Database credentials should be configured through environment variables rather than hardcoded into scripts.

## Current Status

Python data profiling and cleaning, PostgreSQL loading, data-quality validation, and five SQL analytics views have been implemented. Database record counts and selected SQL calculations have been verified. The Power BI dashboard layout has been arranged.

## Future Improvements

- Add automated tests for data cleaning and validation.
- Improve pipeline logging and error handling.
- Implement incremental data loading.
- Explore cloud deployment and pipeline orchestration.
