
SELECT
    COUNT(*) AS total_records,

    SUM(CASE
        WHEN traffic_volume > 5500 THEN 1
        ELSE 0
    END) AS congestion_records,

    ROUND(
        1.0 * SUM(CASE
            WHEN traffic_volume > 5500 THEN 1
            ELSE 0
        END) / COUNT(*),
        4
    ) AS probability_congestion,

    SUM(
        CASE
            WHEN weather_main = 'Clear' THEN 1
            ELSE 0
        END
    ) AS clear_records,

    ROUND(
        1.0 * SUM(
            CASE
                WHEN weather_main = 'Clear' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        3
    ) AS probability_clear,

    SUM(
        CASE
            WHEN traffic_volume > 5500
             AND weather_main = 'Clear'
            THEN 1
            ELSE 0
        END
    ) AS congestion_and_clear_records,

    ROUND(
        1.0 * SUM(
            CASE
                WHEN traffic_volume > 5500
                 AND weather_main = 'Clear'
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        3
    ) AS probability_congestion_and_clear,
	
 SUM(
        CASE
             WHEN weather_main = 'Clear'
             OR  traffic_volume > 5500
            THEN 1
            ELSE 0
        END
    ) AS clear_or_congestion_records,

    ROUND(
        1.0 * SUM(
            CASE
                WHEN weather_main = 'Clear'
                 OR traffic_volume > 5500
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        3
    ) AS probability_clear_or_congestion,

 SUM(
        CASE
             WHEN temp > 292
             OR  traffic_volume > 5500
            THEN 1
            ELSE 0
        END
    ) AS temp_or_congestion_records,

    ROUND(
        1.0 * SUM(
            CASE
                WHEN temp > 292
                 OR traffic_volume > 5500
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        3
    ) AS probability_temp_or_congestion
	
FROM Metro_Interstate_Traffic_Volume;
