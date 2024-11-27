from io import BytesIO


from lxml import etree
from pykml.parser import parse


def validate_kml(file: BytesIO):
    try:
        file.seek(0)
        tree = etree.parse(file)
        file.seek(0)
        parse(file)
    except etree.XMLSyntaxError as xml_error:
        return f"XML syntax error: {xml_error}"
    except Exception as kml_error:
        return f"KML validation error: {kml_error}"

    return False


if __name__ == '__main__':

    path = "C:/Users/андрей/Desktop/кмл для телеграмим/all_merged.kml"

    def f(path):
        with open(path, 'rb') as f:
            file_data = BytesIO(f.read())
            print(validate_kml(file_data))

    f(path)
