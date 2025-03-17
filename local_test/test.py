import geopandas as gpd
from shapely.geometry import Polygon, box
import numpy as np
from pyproj import Transformer


def generate_grid(polygon, grid_size=10, epsg_utm=32618):
    """
    Divides a polygon into a grid of 10m x 10m cells.

    :param polygon: Shapely Polygon in EPSG:4326 (lat/lon)
    :param grid_size: Size of each grid cell in meters (default: 10m)
    :param epsg_utm: UTM zone for projecting the polygon
    :return: List of grid cells in EPSG:4326
    """
    # Convert the polygon to UTM for accurate distance calculations
    transformer_to_utm = Transformer.from_crs("EPSG:4326", f"EPSG:{epsg_utm}", always_xy=True)
    transformer_to_wgs = Transformer.from_crs(f"EPSG:{epsg_utm}", "EPSG:4326", always_xy=True)

    # Convert lat/lon polygon to UTM
    utm_coords = [transformer_to_utm.transform(x, y) for x, y in polygon.exterior.coords]
    utm_polygon = Polygon(utm_coords)

    # Get the polygon bounds in UTM coordinates
    min_x, min_y, max_x, max_y = utm_polygon.bounds

    # Generate the grid cells
    grid_cells = []
    x_coords = np.arange(min_x, max_x, grid_size)
    y_coords = np.arange(min_y, max_y, grid_size)

    for x in x_coords:
        for y in y_coords:
            cell = box(x, y, x + grid_size, y + grid_size)
            if utm_polygon.intersects(cell):  # Keep only cells that intersect the polygon
                # Convert the cell back to lat/lon
                wgs_coords = [
                    transformer_to_wgs.transform(
                        px, py) for px, py in cell.exterior.coords]
                grid_cells.append(Polygon(wgs_coords))

    return grid_cells


# ** Base polygon in lat/lon coordinates **
polygon_coords = [
    (-72.91135, 11.55135),
    (-72.91135, 11.54865),
    (-72.90865, 11.54865),
    (-72.90865, 11.55135),
    (-72.91135, 11.55135)
]
polygon = Polygon(polygon_coords)

# Generate the 10m x 10m grid
grid_cells = generate_grid(polygon)

# Save the base polygon as a GeoJSON file
polygon_gdf = gpd.GeoDataFrame(geometry=[polygon], crs="EPSG:4326")
polygon_gdf.to_file("polygon.geojson", driver="GeoJSON")

# Save the grid as a GeoJSON file
grid_gdf = gpd.GeoDataFrame(geometry=grid_cells, crs="EPSG:4326")
grid_gdf.to_file("grid_10m.geojson", driver="GeoJSON")

print(f"✅ File 'polygon.geojson' saved with the base polygon.")
print(f"✅ File 'grid_10m.geojson' saved with {len(grid_cells)} 10m x 10m cells.")
