import os
import numpy as np
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt

# Función para leer una banda de Sentinel-2
def read_band(file_path):
    """Lee una banda raster de un archivo .jp2 o .tif"""
    with rasterio.open(file_path) as dataset:
        band = dataset.read(1)  # Leer la primera capa de la banda
        profile = dataset.profile  # Obtener los metadatos
    return band, profile

# Función para identificar y limpiar áreas problemáticas
def clean_problematic_areas(band, threshold=10000):
    """
    Limpia las áreas problemáticas en la banda de datos usando un valor umbral.
    Las áreas con valores problemáticos se establecen como NaN.
    """
    # Crear una máscara de áreas problemáticas
    mask_problematic = band > threshold  # Definir un valor umbral (ajustable según el caso)
    # Limpiar las áreas problemáticas
    band_cleaned = np.where(mask_problematic, np.nan, band)
    return band_cleaned

# Función para guardar la banda limpia como un archivo .tif
def save_cleaned_band(band, profile, output_path):
    """Guarda una banda limpia en un archivo .tif."""
    # Actualizar el perfil para usar un tipo de datos compatible
    profile.update(dtype=rasterio.uint16, nodata=0)

    # Convertir los valores NaN a 0 (o cualquier otro valor nodata que prefieras)
    band_cleaned = np.where(np.isnan(band), 0, band).astype(rasterio.uint16)

    with rasterio.open(output_path, 'w', **profile) as dst:
        dst.write(band_cleaned, 1)

# Función principal para procesar todas las bandas en la carpeta img_data
def process_img_data(input_dir, output_dir, threshold=10000):
    """Procesa los archivos en la carpeta img_data y los limpia de áreas problemáticas."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith('.jp2'):  # Cambia a .tif si ese es el formato
            file_path = os.path.join(input_dir, filename)
            print(f"Procesando archivo: {file_path}")

            # Leer la banda de datos
            band, profile = read_band(file_path)

            # Limpiar las áreas problemáticas
            band_cleaned = clean_problematic_areas(band, threshold)

            # Guardar la banda limpia
            output_file = os.path.join(output_dir, f"cleaned_{filename.replace('.jp2', '.tif')}")
            save_cleaned_band(band_cleaned, profile, output_file)
            print(f"Banda procesada y guardada en: {output_file}")

# Función para visualizar la banda
def visualize_band(image_path,image_name):
    print(f"Visualizando la banda: {image_path}")
    try:
        with rasterio.open(image_path) as src:
                # Leer la primera banda (puedes ajustar si tienes más de una banda)
                band = src.read(1)

                # Crear una figura de matplotlib para mostrar la imagen
                plt.figure(figsize=(10, 10))
                
                # Mostrar la imagen con un mapa de colores (cmap)
                plt.imshow(band, cmap='gray')  # Puedes cambiar el 'cmap' si quieres un color diferente

                # Agregar título
                plt.title('Visualización de la banda')
                print(f"Visualizando la banda: {image_path}")
                # Mostrar la imagen
                os.makedirs("figures", exist_ok=True)
                output_path = os.path.join("figures", image_name)
                plt.savefig(output_path)
    except rasterio.errors.RasterioIOError as e:
        print(f"Error al abrir el archivo: {e}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
 

# Ejecutar el procesamiento
if __name__ == "__main__":
    input_dir = os.path.join(os.getcwd(), "images")  # Directorio de entrada para las bandas
    output_dir = os.path.join(os.getcwd(), "images_cleaned")  # Directorio de salida para las bandas limpias
    #process_img_data(input_dir, output_dir, threshold=10000)
    visualize_band(os.path.join(output_dir, "cleaned_B02.tif"),"B02")
