
WITH holiday_data AS (
    SELECT
        CAST(strftime('%Y', date_time) AS INTEGER) AS year,
        CASE
            WHEN date(date_time) IN (
                '2015-01-01',
                '2016-01-01',
                '2017-01-01'
            )
            THEN 'New Year''s Day'

            WHEN date(date_time) IN (
                '2015-09-07',
                '2016-09-05',
                '2017-09-04'
            )
            THEN 'Labor Day'
        END AS holiday_name,
        temp,
        traffic_volume
    FROM Metro_Interstate_Traffic_Volume
    WHERE date(date_time) IN (
        '2015-01-01',
        '2016-01-01',
        '2017-01-01',
        '2015-09-07',
        '2016-09-05',
        '2017-09-04'
    )
)
SELECT
    year,
    holiday_name,
    ROUND(AVG(temp), 2) AS average_temperature_kelvin,
    ROUND(AVG(temp) - 273.15, 2) AS average_temperature_celsius,
    ROUND(MIN(temp) - 273.15, 2) AS minimum_temperature_celsius,
    ROUND(MAX(temp) - 273.15, 2) AS maximum_temperature_celsius,
    ROUND(AVG(traffic_volume), 2) AS average_traffic_volume,
    COUNT(*) AS recorded_hours
FROM holiday_data
GROUP BY year, holiday_name
ORDER BY holiday_name, year;
