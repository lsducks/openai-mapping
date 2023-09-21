from pathlib import Path

from src.extract_columns import CsvExtractor


if __name__ == "__main__":

    example = CsvExtractor(raw_path=Path('./data'), extracted_path=Path('./conf/columns'))
    example.read()
    example.save()
