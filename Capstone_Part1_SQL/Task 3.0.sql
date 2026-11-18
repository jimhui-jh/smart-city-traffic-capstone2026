
WITH stats AS (
    SELECT
        COUNT(*) AS n,
        SUM(temp) AS sum_x,
        SUM(traffic_volume) AS sum_y,
        SUM(temp * traffic_volume) AS sum_xy,
        SUM(temp * temp) AS sum_x2,
        SUM(traffic_volume * traffic_volume) AS sum_y2
    FROM Metro_Interstate_Traffic_Volume	
WHERE temp IS NOT NULL
      AND traffic_volume IS NOT NULL
)
SELECT
    ROUND(
        (n * sum_xy - sum_x * sum_y) /
        SQRT(
            (n * sum_x2 - sum_x * sum_x) *
            (n * sum_y2 - sum_y * sum_y)
        ),3) AS correlation_coefficient
FROM stats;

