import re

from src.shared.constants import BANDS_MAP

def get_band_name(filename):
    """Extracts the band name from the filename."""
    match = re.search(r"_B(\d{2})_", filename)
    if match:
        band_code = f"B{match.group(1)}"
        return BANDS_MAP.get(band_code, band_code)
    return None