-- 1. Check duplicate route IDs
SELECT COUNT(*) AS duplicate_route_ids
FROM (
    SELECT route_id
    FROM routes
    GROUP BY route_id
    HAVING COUNT(*) > 1
) AS duplicates;

-- 2. Check trips with invalid route IDs
SELECT COUNT(*) AS invalid_trip_routes
FROM trips t
LEFT JOIN routes r ON t.route_id = r.route_id
WHERE r.route_id IS NULL;

-- 3. Check stop times with invalid trip IDs
SELECT COUNT(*) AS invalid_trip_references
FROM stop_times st
LEFT JOIN trips t ON st.trip_id = t.trip_id
WHERE t.trip_id IS NULL;

-- 4. Check stop times with invalid stop IDs
SELECT COUNT(*) AS invalid_stop_references
FROM stop_times st
LEFT JOIN stops s ON st.stop_id = s.stop_id
WHERE s.stop_id IS NULL;