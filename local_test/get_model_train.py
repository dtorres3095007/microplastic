
import re

if __name__ == "__main__":

    filename = "T18PYT_20250127T152659_B04_10m.jp2"
    match = re.search(r"_B(\d{2}A?)", filename)
    if match:
        print("Match encontrado:", match.group(1))
    else:
        print("No se encontró ningún match")
