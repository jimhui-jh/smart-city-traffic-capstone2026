
WITH ordered_traffic AS (
    SELECT
        traffic_volume,
        ROW_NUMBER() OVER (
            ORDER BY traffic_volume
        ) AS row_num,
        COUNT(*) OVER () AS total_rows
    FROM Metro_Interstate_Traffic_Volume
    WHERE traffic_volume IS NOT NULL
),

median_result AS (
    SELECT
        AVG(traffic_volume * 1.0) AS median_traffic_volume
    FROM ordered_traffic
    WHERE row_num IN (
        (total_rows + 1) / 2,
        (total_rows + 2) / 2
    )
),

statistics AS (
    SELECT
        COUNT(*) AS observation_count,
        AVG(traffic_volume * 1.0) AS mean_traffic_volume,
        AVG(traffic_volume * traffic_volume * 1.0)
            - AVG(traffic_volume * 1.0)
              * AVG(traffic_volume * 1.0)
            AS population_variance,
        MIN(traffic_volume) AS minimum_traffic_volume,
        MAX(traffic_volume) AS maximum_traffic_volume
    FROM Metro_Interstate_Traffic_Volume
    WHERE traffic_volume IS NOT NULL
)

SELECT
    observation_count,
    ROUND(mean_traffic_volume, 2) AS mean,
    ROUND(median_traffic_volume, 2) AS median,
    ROUND(SQRT(population_variance), 2) AS standard_deviation,
    ROUND(population_variance, 2) AS variance,
    minimum_traffic_volume AS minimum,
    maximum_traffic_volume AS maximum,
    maximum_traffic_volume - minimum_traffic_volume AS traffic_range
FROM statistics
CROSS JOIN median_result;
