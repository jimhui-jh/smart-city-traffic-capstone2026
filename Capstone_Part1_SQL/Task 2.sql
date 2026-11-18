SELECT name
FROM sqlite_master
WHERE type = 'table'
ORDER BY name;
PRAGMA table_info(Metro_Interstate_Traffic_Volume);