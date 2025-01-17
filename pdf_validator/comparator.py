from extractor import extract_pdf_info
from extractor import extract_barcodes_from_pdf

def compare_pdfs(standard_pdf_path, test_pdf_path):
    """
    Сравнивает тестовый PDF с эталонным по ключам.

    Args:
        standard_pdf_path (str): Путь к эталонному PDF.
        test_pdf_path (str): Путь к тестовому PDF.

    Returns:
        dict: Результаты проверки тестового PDF на соответствие эталону по ключам.
    """
    # Используем extract_pdf_info для извлечения данных из PDF
    standard_data = extract_pdf_info(standard_pdf_path)
    test_data = extract_pdf_info(test_pdf_path)

    comparison_result = {}

    # Сравниваем только ключи
    standard_keys = set(standard_data.keys())
    test_keys = set(test_data.keys())

    if standard_keys == test_keys:
        comparison_result['Keys'] = 'All keys matches.'
    else:
        comparison_result['Keys'] = f'Fail: Expected keys {standard_keys}, Got keys {test_keys}'

    return comparison_result




def compare_barcodes(standard_pdf_path, test_pdf_path):
    """
    Сравнивает баркоды из тестового и эталонного PDF.

    Args:
        standard_pdf_path (str): Путь к эталонному PDF.
        test_pdf_path (str): Путь к тестовому PDF.

    Returns:
        dict: Результаты проверки баркодов.
    """
    standard_barcodes = extract_barcodes_from_pdf(standard_pdf_path)
    test_barcodes = extract_barcodes_from_pdf(test_pdf_path)

    barcode_comparison_result = {}

    # Проверка на наличие баркодов
    if standard_barcodes and test_barcodes:
        if set(standard_barcodes) == set(test_barcodes):
            barcode_comparison_result['Barcodes'] = 'Passed. Barcode has been found.'
        else:
            barcode_comparison_result['Barcodes'] = f'Fail: Expected barcodes {standard_barcodes}, Got {test_barcodes}'
    else:
        if not standard_barcodes:
            barcode_comparison_result['Barcodes'] = 'Fail: No barcodes found in the standard PDF'
        if not test_barcodes:
            barcode_comparison_result['Barcodes'] = 'Fail: No barcodes found in the test PDF'

    return barcode_comparison_result



# Пример использования
standard_pdf_file_path = '\standard_pdf.pdf'
test_pdf_file_path = '\test.pdf'


# Сравнение текста
text_comparison = compare_pdfs(standard_pdf_file_path, test_pdf_file_path)
print("Text Comparison Result:")
for field, result in text_comparison.items():
    print(f"{field}: {result}")

# Сравнение баркодов
barcode_comparison = compare_barcodes(standard_pdf_file_path, test_pdf_file_path)
print("\nBarcode Comparison Result:")
for field, result in barcode_comparison.items():
    print(f"{field}: {result}")
