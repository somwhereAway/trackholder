import io
from itertools import islice
import re
import sys
from typing import Tuple, Dict

from lxml import etree


def merge_kml_files(file1, file2, output_file):
    tree1 = etree.parse(file1)
    root1 = tree1.getroot()
    tree2 = etree.parse(file2)
    root2 = tree2.getroot()

    document1 = root1.find('.//{http://www.opengis.net/kml/2.2}Document')
    document2 = root2.find('.//{http://www.opengis.net/kml/2.2}Document')

    if document1 is None or document2 is None:
        raise ValueError("Оба KML файла должны содержать элемент Document")

    second_file_nsmap = root2.nsmap
    nsmap = root1.nsmap
    print(type(nsmap))
    for prefix, uri in second_file_nsmap.items():
        if prefix not in nsmap:
            nsmap[f'xmlns:{prefix}'] = uri
    print(nsmap)
    root1.nsmap.update(nsmap)
    print(root1)

    for placemark in document2.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
        document1.append(placemark)

    tree1.write(output_file, pretty_print=True,
                xml_declaration=True, encoding='UTF-8')
    print(f"KML файлы успешно объединены и сохранены в {output_file}")


NSMAP_LINE = 2
NAMESPACE_PATTERN = r'xmlns(?:\s*:\s*(\w+))?="([^"]+)"'
FIRST_LINE = '<?xml version="1.0" encoding="UTF-8"?>'
THERD_LINE = "<Document>"
LAST_TWO_LINES = "</Document>\n<kml>"
END_INDEX = 2


def parse_kml_namespaces(kml_string: str) -> Dict[str, str]:
    if not kml_string.startswith('<kml'):
        raise ValueError("Строка должна начинаться с <kml")
    result = {}
    for match in re.finditer(NAMESPACE_PATTERN, kml_string):
        prefix = match.group(1)
        url = match.group(2)
        if prefix:
            result[f'xmlns:{prefix}'] = url
        else:
            result['xmlns'] = url

    return result


def get_line(file_path: str, line_number: int) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        line = next(islice(file, line_number, line_number + 1), None)
    return line


def parse_header(
    file: str, stop_str: str = "<Placemark"
) -> Tuple[Dict[str, str], int]:
    line_count = 0
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            line_count += 1
            if stop_str in line:
                break
    return line_count


def namespaces_to_kml_string(namespaces: Dict[str, str]) -> str:
    kml_string = '<kml '
    for prefix, url in namespaces.items():
        kml_string += f'{prefix}="{url}" '
    kml_string = kml_string.strip() + '>'
    return kml_string


def append_file(output_buffer, file, count):
    with open(file, 'r', encoding='utf-8') as in_file:
        all_lines = in_file.readlines()
        start_index = count - 1
        for i in range(start_index, len(all_lines) - END_INDEX):
            output_buffer.write(all_lines[i])


def pure_merge(file: str, output_file: str = "output.kml") -> None:
    nmspace1, count1 = parse_header(output_file)
    nmspace2, count2 = parse_header(file1)
    nsmap_string = namespaces_to_kml_string(nmspace1 | nmspace2)
    head_lines = (FIRST_LINE, nsmap_string, THERD_LINE)
    output_buffer = io.StringIO()
    for line in head_lines:
        output_buffer.write(line + '\n')
    append_file(output_buffer, file1, count1)
    append_file(output_buffer, file2, count2)
    output_buffer.write(LAST_TWO_LINES)
    output_content = output_buffer.getvalue()
    output_buffer.close()
    return output_content


file1 = "kml_files/file_1.kml"
file2 = "kml_files/file_2.kml"
print(sys.getsizeof(pure_merge(file1, file2))/1024)
