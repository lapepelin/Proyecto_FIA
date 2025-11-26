import csv
import datetime
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

BASE_DIR = Path(__file__).parent
EXCEL_BASE_DATE = datetime.datetime(1899, 12, 30)
DATE_COLUMNS = {"fecha", "fecha_alta"}


def col_to_index(col: str) -> int:
    idx = 0
    for char in col:
        idx = idx * 26 + (ord(char.upper()) - 64)
    return idx - 1


def read_xlsx(path: Path):
    zf = zipfile.ZipFile(path)
    ns = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

    shared_strings = []
    if "xl/sharedStrings.xml" in zf.namelist():
        root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
        shared_strings = [t.text or "" for t in root.findall(".//a:si/a:t", ns)]

    sheet = ET.fromstring(zf.read("xl/worksheets/sheet1.xml"))
    rows = []
    for row in sheet.findall(".//a:sheetData/a:row", ns):
        values = []
        for cell in row.findall("a:c", ns):
            ref = cell.attrib.get("r", "")
            col_letters = "".join(filter(str.isalpha, ref))
            idx = col_to_index(col_letters)
            while len(values) < idx:
                values.append("")

            raw_value = cell.find("a:v", ns)
            value = raw_value.text if raw_value is not None else ""
            if cell.attrib.get("t") == "s":
                value = shared_strings[int(value)] if value else ""
            values.append(value)
        rows.append(values)
    return rows


def excel_date_to_iso(value: str) -> str:
    try:
        days = float(value)
    except (TypeError, ValueError):
        return value
    date_value = EXCEL_BASE_DATE + datetime.timedelta(days=days)
    return date_value.date().isoformat()


def normalize_value(column: str, value: str) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    if text == "":
        return ""

    if column in DATE_COLUMNS:
        return excel_date_to_iso(text)

    try:
        number = float(text)
        if number.is_integer():
            return str(int(number))
        return str(number)
    except ValueError:
        return text


def write_csv_from_xlsx(filename: str):
    rows = read_xlsx(BASE_DIR / filename)
    if not rows:
        return
    header = rows[0]
    width = len(header)
    cleaned_rows = []
    for row in rows[1:]:
        padded = row + [""] * (width - len(row))
        cleaned_rows.append([normalize_value(header[idx], padded[idx]) for idx in range(width)])

    output_path = BASE_DIR / f"{Path(filename).stem}.csv"
    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(cleaned_rows)
    return output_path


def main():
    files = ["Clientes.xlsx", "Productos.xlsx", "Ventas.xlsx", "Detalle_ventas.xlsx"]
    for file in files:
        csv_path = write_csv_from_xlsx(file)
        if csv_path:
            print(f"Generado: {csv_path}")


if __name__ == "__main__":
    main()
