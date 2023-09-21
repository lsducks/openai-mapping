import csv
import yaml
from abc import abstractmethod
from pathlib import Path


class DataExtractor:
    @abstractmethod
    def read(self) -> None:
        pass

    @abstractmethod
    def save(self) -> None:
        pass


class CsvExtractor(DataExtractor):
    def __init__(self, raw_path: Path, extracted_path: Path, sep: str = ','):
        self.raw_path = raw_path
        self.extracted_path = extracted_path
        self.sep = sep
        self.sources_columns = {}
        self.template_columns = None

    def read(self):
        template = self.raw_path.glob('template*.csv')

        with open(template.__next__(), 'r') as f:
            csv_reader = csv.reader(f, delimiter=self.sep)
            self.template_columns = csv_reader.__next__()

        sources = self.raw_path / 'source_tables'

        for file in sources.glob("*.csv"):
            name = file.stem

            with open(file, 'r') as f:
                csv_reader = csv.reader(f, delimiter=self.sep)
                self.sources_columns[name] = csv_reader.__next__()

    def save(self):
        sources_file = self.extracted_path / 'sources_columns.yaml'
        template_file = self.extracted_path / 'template_columns.yaml'

        with open(sources_file, 'w') as f:
            yaml.dump(self.sources_columns, f)

        with open(template_file, 'w') as f:
            yaml.dump(self.template_columns, f)
