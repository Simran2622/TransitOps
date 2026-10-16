
-- 1. Trips per route
CREATE OR REPLACE VIEW vw_trips_per_route AS
SELECT
    r.route_id,
    r.route_long_name,
    COUNT(t.trip_id) AS total_trips
FROM routes r
LEFT JOIN trips t ON r.route_id = t.route_id
GROUP BY r.route_id, r.route_long_name;


-- 2. Scheduled stop-time events per stop
CREATE OR REPLACE VIEW vw_stop_activity AS
SELECT
    s.stop_id,
    s.stop_name,
    COUNT(st.trip_id) AS total_stop_time_events
FROM stops s
LEFT JOIN stop_times st ON s.stop_id = st.stop_id
GROUP BY s.stop_id, s.stop_name;


-- 3. Average stops per trip
CREATE OR REPLACE VIEW vw_average_stops_per_trip AS
SELECT
    ROUND(AVG(stop_count), 2) AS average_stops_per_trip
FROM (
    SELECT trip_id, COUNT(*) AS stop_count
    FROM stop_times
    GROUP BY trip_id
) AS trip_stop_counts;


-- 4. Trips by route type
CREATE OR REPLACE VIEW vw_trips_by_route_type AS
SELECT
    r.route_type,
    COUNT(t.trip_id) AS total_trips
FROM routes r
LEFT JOIN trips t ON r.route_id = t.route_id
GROUP BY r.route_type;


-- 5. Distinct stops served by route
CREATE OR REPLACE VIEW vw_route_stop_coverage AS
SELECT
    r.route_id,
    r.route_long_name,
    COUNT(DISTINCT st.stop_id) AS distinct_stops
FROM routes r
JOIN trips t ON r.route_id = t.route_id
JOIN stop_times st ON t.trip_id = st.trip_id
GROUP BY r.route_id, r.route_long_name;
