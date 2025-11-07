SELECT 
    DISTINCT 
    YEAR(created_at) AS year,
    MONTH(created_at) AS month,
    DATE_FORMAT(created_at, '%M %Y') AS month_year_label
FROM microplastic_zones
ORDER BY year ASC, month ASC;