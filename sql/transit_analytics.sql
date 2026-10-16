
-- 1. Number of trips per route
SELECT
    r.route_id,
    r.route_long_name,
    COUNT(t.trip_id) AS total_trips
FROM routes r
LEFT JOIN trips t
    ON r.route_id = t.route_id
GROUP BY r.route_id, r.route_long_name
ORDER BY total_trips DESC
LIMIT 20;


-- 2. Stops with the most scheduled stop-time events
SELECT
    s.stop_id,
    s.stop_name,
    COUNT(*) AS total_stop_time_events
FROM stops s
JOIN stop_times st
    ON s.stop_id = st.stop_id
GROUP BY s.stop_id, s.stop_name
ORDER BY total_stop_time_events DESC
LIMIT 20;


-- 3. Average number of stops per trip
SELECT
    ROUND(AVG(stop_count), 2) AS average_stops_per_trip
FROM (
    SELECT
        trip_id,
        COUNT(*) AS stop_count
    FROM stop_times
    GROUP BY trip_id
) AS trip_stop_counts;


-- 4. Trips by route type
SELECT
    r.route_type,
    COUNT(t.trip_id) AS total_trips
FROM routes r
LEFT JOIN trips t
    ON r.route_id = t.route_id
GROUP BY r.route_type
ORDER BY total_trips DESC;


-- 5. Routes with the most distinct stops
SELECT
    r.route_id,
    r.route_long_name,
    COUNT(DISTINCT st.stop_id) AS distinct_stops
FROM routes r
JOIN trips t
    ON r.route_id = t.route_id
JOIN stop_times st
    ON t.trip_id = st.trip_id
GROUP BY r.route_id, r.route_long_name
ORDER BY distinct_stops DESC
LIMIT 20;
