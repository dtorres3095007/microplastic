SELECT 
polygon_id, 
ST_AsText(polygon_geom) AS polygon_geom, 
NDVI, 
NDWI, 
NDCI, 
FDI, 
NDPI, 
BLUE, 
GREEN, 
RED, 
REDEDGE1, 
REDEDGE2, 
REDEDGE3, 
NIR_10m, 
NIR_20m, 
SWIR1, 
SWIR2, 
pred_linear, 
pred_forest, 
pred_neural, 
DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') AS created_at
FROM microplastic_zones
WHERE (
        (%(pred_min)s IS NULL AND %(pred_max)s IS NULL) OR
        (%(pred_min)s IS NOT NULL AND %(pred_max)s IS NOT NULL AND pred_forest BETWEEN %(pred_min)s AND %(pred_max)s) OR
        (%(pred_min)s IS NOT NULL AND %(pred_max)s IS NULL AND pred_forest >= %(pred_min)s) OR
        (%(pred_min)s IS NULL AND %(pred_max)s IS NOT NULL AND pred_forest <= %(pred_max)s)
    )
    AND (%(month)s IS NULL OR MONTH(created_at) = %(month)s)
    AND (%(year)s IS NULL OR YEAR(created_at) = %(year)s)
LIMIT %(limit)s OFFSET %(offset)s;