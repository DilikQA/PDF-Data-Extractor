# PDF Data Extractor

This project extracts data from PDF files using Python. It supports different PDF formats and validates extracted data.

## Installation

Follow these steps to install the necessary dependencies:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repository/PDF-Data-Extractor.git
   ```

2. Navigate into the project directory:
   ```bash
   cd PDF-Data-Extractor
   ```

3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

After installation, you can run the script to extract data from a PDF.

Example:
```bash
python extract_data.py <path-to-pdf-file>

## Пример вызова:
pdf_path = '/data/test_task.pdf'
pdf_data = extract_pdf_data(pdf_path)
print(pdf_data)