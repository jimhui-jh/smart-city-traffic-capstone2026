
WITH counts AS (
    SELECT
        SUM(CASE
            WHEN weather_main = 'Clear'
             AND traffic_volume > 5500
            THEN 1 ELSE 0
        END) AS a,

		SUM(CASE
            WHEN weather_main = 'Clear'
             AND traffic_volume <= 5500
            THEN 1 ELSE 0
        END) AS b,
		
		SUM(CASE
            WHEN weather_main = 'Clouds'
             AND traffic_volume > 5500
            THEN 1 ELSE 0
        END) AS c,

		SUM(CASE
            WHEN weather_main = 'Clouds'
             AND traffic_volume <= 5500
            THEN 1 ELSE 0
        END) AS d
		
FROM Metro_Interstate_Traffic_Volume
)

SELECT
    a AS clear_congestion,
    b AS clear_no_congestion,
    c AS cloudy_congestion,
    d AS cloudy_no_congestion,

    ROUND(
        1.0 * a * d / (b * c),
        3
    ) AS odds_ratio

FROM counts;
