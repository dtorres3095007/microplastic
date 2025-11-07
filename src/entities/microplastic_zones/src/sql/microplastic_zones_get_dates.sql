SELECT 
    DISTINCT 
    YEAR(created_at) AS year,
    MONTH(created_at) AS month
FROM microplastic_zones
ORDER BY year ASC, month ASC;