
WITH probability AS (
    SELECT
        COUNT(*) AS total_records,

        SUM(CASE
            WHEN weather_main = 'Clear'
            THEN 1 ELSE 0
        END) AS clear_records,

        SUM(CASE
            WHEN traffic_volume > 5500
            THEN 1 ELSE 0
        END) AS congestion_records,

       SUM(CASE
            WHEN weather_main = 'Clear'
             AND traffic_volume > 5500
            THEN 1 ELSE 0
        END) AS clear_and_congestion_records

    FROM Metro_Interstate_Traffic_Volume
)

SELECT
    ROUND(1.0 * clear_records / total_records, 3)
        AS p_clear,

    ROUND(1.0 * congestion_records / total_records, 3)
        AS p_congestion,

    ROUND(1.0 * clear_and_congestion_records / total_records, 3)
        AS p_clear_and_congestion,

    ROUND(
        (1.0 * clear_records / total_records) *
        (1.0 * congestion_records / total_records),3) AS p_clear_times_p_congestion

FROM probability;

