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
LIMIT %(limit)s OFFSET %(offset)s;