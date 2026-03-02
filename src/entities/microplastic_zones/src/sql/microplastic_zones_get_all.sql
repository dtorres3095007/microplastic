SELECT 
polygon_id, 
ST_AsText(polygon_geom) AS polygon_geom,
pred_forest
FROM microplastic_zones
WHERE (
        (%(pred_min)s IS NULL AND %(pred_max)s IS NULL) OR
        (%(pred_min)s IS NOT NULL AND %(pred_max)s IS NOT NULL AND pred_forest BETWEEN %(pred_min)s AND %(pred_max)s) OR
        (%(pred_min)s IS NOT NULL AND %(pred_max)s IS NULL AND pred_forest >= %(pred_min)s) OR
        (%(pred_min)s IS NULL AND %(pred_max)s IS NOT NULL AND pred_forest <= %(pred_max)s)
    )
    AND (%(month)s IS NULL OR MONTH(created_at) = %(month)s)
    AND (%(year)s IS NULL OR YEAR(created_at) = %(year)s)
    AND (
        (%(start)s IS NULL AND %(end)s IS NULL) OR
        (%(start)s IS NOT NULL AND %(end)s IS NOT NULL AND created_at BETWEEN %(start)s AND %(end)s) OR
        (%(start)s IS NOT NULL AND %(end)s IS NULL AND created_at >= %(start)s) OR
        (%(start)s IS NULL AND %(end)s IS NOT NULL AND created_at <= %(end)s)
    )
LIMIT %(limit)s OFFSET %(offset)s;