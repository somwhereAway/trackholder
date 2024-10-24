import asyncio
import aiofiles
from io import BytesIO
from lxml import etree
from pykml import parser


async def parse_kml_file(filepath: str) -> etree.Element:
    """
    Асинхронно парсит KML файл и возвращает корневой элемент <Document>.

    :param filepath: Путь до KML файла.
    :return: Корневой элемент <Document> или None.
    """
    try:
        async with aiofiles.open(filepath, 'rb') as f:
            kml_data = await f.read()
            kml_stream = BytesIO(kml_data)
            kml_tree = parser.parse(kml_stream)

            return kml_tree.getroot().Document
    except Exception as e:
        print(f"Ошибка при обработке файла {filepath}: {e}")
        return None


async def merge_kml_files_parallel(filepaths: list[str]) -> BytesIO:
    """
    Объединяет KML файлы, используя асинхронную обработку.

    :param filepaths: Список путей до KML файлов.
    :return: Поток с объединенным KML файлом (BytesIO).
    """
    kml_namespace = '{http://www.opengis.net/kml/2.2}'
    new_kml_doc = etree.Element(f"{kml_namespace}kml")
    new_document = etree.SubElement(new_kml_doc, f"{kml_namespace}Document")
    tasks = [parse_kml_file(filepath) for filepath in filepaths]
    results = await asyncio.gather(*tasks)

    for document in results:
        if document is not None:
            for placemark in document.Placemark:
                new_document.append(placemark)

    result_kml = BytesIO()
    result_kml.write(
        etree.tostring(
            new_kml_doc,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8'
        )
    )
    result_kml.seek(0)

    return result_kml
