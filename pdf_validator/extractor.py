import pdfplumber
import pyzbar.pyzbar as pyzbar
from PIL import Image
import io
import re

def extract_pdf_info(pdf_file_path):
    """
    Читает PDF файл, извлекает информацию и возвращает ее в виде словаря.

    Args:
        pdf_file_path (str): Путь к PDF файлу для обработки.

    Returns:
        dict: Словарь с извлеченной информацией из PDF файла.
    """
    try:
        # Открываем PDF и извлекаем текст
        with pdfplumber.open(pdf_file_path) as pdf:
            text_data = "".join(page.extract_text() for page in pdf.pages)

        # Регулярные выражения для извлечения данных
        key_patterns = {
            'PN': r'PN:\s*(\S*)',
            'SN': r'SN:\s*(\S*)',
            'Description': r'DESCRIPTION:\s*(.+?)\n',
            'Location': r'LOCATION:\s*(\S*)',
            'CONDITION': r'CONDITION:\s*(\S*)',
            'Receiver#': r'RECEIVER#:\s*(\d*)',
            'UOM': r'UOM:\s*(\S*)',
            'EXP DATE': r'EXP DATE:\s*(\S*)',
            'PO': r'PO:\s*(\S*)',
            'CERT SOURCE': r'CERT SOURCE:\s*(\S*)',
            'REC.DATE': r'REC\.DATE:\s*(\S*)',
            'MFG': r'MFG:\s*(\S*)',
            'BATCH#': r'BATCH#\s*:\s*(\S*)',
            'DOM': r'DOM:\s*(\S*)',
            'REMARK': r'REMARK:\s*(.*?)\n(?=LOT#:)',  # Завершается перед LOT#
            'LOT#': r'LOT#\s*:\s*(\S*)',
            'TAGGED BY': r'TAGGED BY:\s*(.*?)(?=\n|Qty:)',  # Захватываем TAGGED BY до нового поля или Qty
            'Qty': r'Qty:\s*(\S*)',
            'NOTES': r'NOTES:\s*([^Q]*)',  # Захватываем NOTES до 'Qty' или конца строки
        }

        # Инициализируем словарь с пустыми значениями для всех ключей
        data = {key: " " for key in key_patterns}

        # Извлечение данных с помощью регулярных выражений
        for key, pattern in key_patterns.items():
            match = re.search(pattern, text_data, re.DOTALL)
            if match:
                # Если найдено значение, проверяем на пустое значение
                value = match.group(1).strip() if match.group(1).strip() else " "

                # Специальная проверка для 'TAGGED BY' чтобы не было 'NOTES:' в случае отсутствия значения
                if key == 'TAGGED BY' and value == 'NOTES:':
                    value = " "

                data[key] = value
            else:
                # Если нет совпадений, возвращаем пустое значение
                data[key] = " "

        # Возвращаем корректные данные
        return data

    except Exception as e:
        print(f"Ошибка при обработке PDF файла: {e}")
        return {}


def extract_barcodes_from_pdf(pdf_file_path):
    """
    Извлекает баркоды из PDF и возвращает их в виде списка строк.

    Args:
        pdf_file_path (str): Путь к PDF файлу.

    Returns:
        list: Список строк с извлеченными баркодами.
    """
    barcodes = []

    try:
        with pdfplumber.open(pdf_file_path) as pdf:
            for page in pdf.pages:
                # Преобразуем страницу в изображение
                im = page.to_image()
                img = im.original  # Преобразуем в изображение PIL
                img_byte_array = io.BytesIO()
                img.save(img_byte_array, format='PNG')

                # Декодируем баркоды из изображения
                img_byte_array.seek(0)
                img = Image.open(img_byte_array)
                decoded_barcodes = pyzbar.decode(img)

                for barcode in decoded_barcodes:
                    barcodes.append(barcode.data.decode('utf-8'))

        return barcodes

    except Exception as e:
        print(f"Ошибка при извлечении баркодов: {e}")
        return []