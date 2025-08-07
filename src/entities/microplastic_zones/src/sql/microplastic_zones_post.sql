INSERT INTO microplastic_zones (
    polygon_id,
    polygon_geom,
    NDVI,
    NDWI,
    NDCI,
    FDI,
    NDPI,
    pred_linear,
    pred_forest,
    pred_neural
) VALUES (
    %s,
    ST_GeomFromText(%s, 4326),
    %s, %s, %s, %s, %s, %s, %s, %s
);