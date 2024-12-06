from io import BytesIO
from itertools import islice
from typing import Tuple, Dict

from lxml import etree

# from tg_bot.kml_eng.validator import validate_kml


def merge_kml_files(file1, file2, output_file):
    tree1 = etree.parse(file1)
    root1 = tree1.getroot()
    tree2 = etree.parse(file2)
    root2 = tree2.getroot()

    document1 = root1.find(".//{http://www.opengis.net/kml/2.2}Document")
    document2 = root2.find(".//{http://www.opengis.net/kml/2.2}Document")

    if document1 is None or document2 is None:
        raise ValueError("Оба KML файла должны содержать элемент Document")

    second_file_nsmap = root2.nsmap
    nsmap = root1.nsmap
    for prefix, uri in second_file_nsmap.items():
        if prefix not in nsmap:
            nsmap[f"xmlns:{prefix}"] = uri
    print(nsmap)
    root1.nsmap.update(nsmap)
    print(root1)

    for placemark in document2.findall(
        ".//{http://www.opengis.net/kml/2.2}Placemark"
    ):
        document1.append(placemark)

    tree1.write(output_file, pretty_print=True,
                xml_declaration=True, encoding="UTF-8")
    print(f"KML файлы успешно объединены и сохранены в {output_file}")


NSMAP_LINE = 2
NAMESPACE_PATTERN = r'xmlns(:\w+)?="[^"]+"'
FIRST_LINE = '<?xml version="1.0" encoding="UTF-8"?>'
THERD_LINE = "<Document>"
LAST_TWO_LINES = "</Document>\n</kml>"
END_INDEX = 2
SPACE = " "
BEGIN_NSMAP = "<kml "
END_NSMAP = ">"
FOLDER_OPEN = "<Folder>\n"
FOLDER_CLOSE = "</Folder>\n"
NAME_OPEN = "<name>"
NAME_CLOSE = "</name>\n"


def get_nsmap_line(file_path: str, line_number: int = NSMAP_LINE) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        line = next(islice(file, line_number - 1, line_number), None)
    return str(line)


def parse_header(
    file: str,
    stop_str: str = "<Placemark",
    folder_str: str = "<Folder"
) -> Tuple[Dict[str, str], int]:
    line_count = 0
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            line_count += 1
            if folder_str in line:
                line_count += 1
                return line_count, True
            if stop_str in line:
                return line_count, False
    return


def parse_kml_namespaces(kml_string: str) -> list[str]:
    if not kml_string.startswith(BEGIN_NSMAP):
        raise ValueError("Строка должна начинаться с <kml")
    begin_index = len(BEGIN_NSMAP)
    end_index = -(len(END_NSMAP) + 1)
    return kml_string[begin_index:end_index]


def namespaces_to_kml_string(namespaces: set[str]) -> str:
    result_string = BEGIN_NSMAP + " ".join(map(str, namespaces)) + END_NSMAP
    return result_string


def append_file(outfile, file, count, contain_folders, filename):
    with open(file, "r", encoding="utf-8") as in_file:
        all_lines = in_file.readlines()
        start_index = count - 1
        if contain_folders:
            outfile.write(FOLDER_OPEN.encode("utf-8"))
            outfile.write(NAME_OPEN.encode("utf-8"))
            outfile.write(str(filename).encode("utf-8"))
            outfile.write(NAME_CLOSE.encode("utf-8"))
        for i in range(start_index, len(all_lines) - END_INDEX):
            outfile.write(all_lines[i].encode("utf-8"))
        if contain_folders:
            outfile.write(FOLDER_CLOSE.encode("utf-8"))


def merge_kml_files_v2(files: list[tuple]) -> BytesIO:
    namespaces = set()
    for path, filename in files:
        nsmap = parse_kml_namespaces(get_nsmap_line(path))
        namespaces.update(nsmap.split(SPACE))
    nsmap_string = namespaces_to_kml_string(namespaces)
    head_lines = (FIRST_LINE, nsmap_string, THERD_LINE)
    outfile = BytesIO()
    for line in head_lines:
        outfile.write((line + "\n").encode("utf-8"))
    for path, filename in files:
        count, contain_folders = parse_header(path)
        print(count, contain_folders)
        append_file(outfile, path, count, contain_folders, filename)
    outfile.write((LAST_TWO_LINES).encode("utf-8"))
    outfile.seek(0)
    return outfile
