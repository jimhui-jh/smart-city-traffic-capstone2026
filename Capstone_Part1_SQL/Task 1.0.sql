WITH yearly_traffic AS (
    SELECT
        CAST(strftime('%Y', date_time) AS INTEGER) AS year,
        SUM(traffic_volume) AS total_traffic_volume,
        COUNT(*) AS recorded_hours
    FROM Metro_Interstate_Traffic_Volume
    WHERE strftime('%Y', date_time) IN (
        '2012', '2013', '2014',
        '2015', '2016', '2017'
    )
    GROUP BY strftime('%Y', date_time)
),

yearly_comparison AS (
    SELECT
        year,
        total_traffic_volume,
        recorded_hours,
        LAG(total_traffic_volume) OVER (
            ORDER BY year
        ) AS previous_year_volume
    FROM yearly_traffic
)

SELECT
    year,
    total_traffic_volume,
    recorded_hours,
    previous_year_volume,
    total_traffic_volume - previous_year_volume AS volume_change,

ROUND(
        100.0 * (total_traffic_volume - previous_year_volume)
        / NULLIF(previous_year_volume, 0),
        2
    ) AS percentage_change,
    CASE
        WHEN previous_year_volume IS NULL THEN 'No previous year'
        WHEN total_traffic_volume > previous_year_volume THEN 'Increase'
        WHEN total_traffic_volume < previous_year_volume THEN 'Decrease'
        ELSE 'No change'
    END AS trend
FROM yearly_comparison
ORDER BY year;
