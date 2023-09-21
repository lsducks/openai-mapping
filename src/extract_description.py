import pandas as pd
import yaml
from pathlib import Path


class DescriptionExtractor:
    def __init__(self, raw_path: Path, extracted_path: Path, n_rows: int, sep: str = ','):
        self.raw_path = raw_path
        self.extracted_path = extracted_path
        self.n_rows = n_rows
        self.sep = sep
        self.template_columns = self.__get_columns('template_columns.yaml')
        self.sources_columns = self.__get_columns('sources_columns.yaml')
        self.template_descriptions = {}
        self.sources_descriptions = {}

    def __get_columns(self, filename):
        path = self.extracted_path / 'columns' / filename

        with open(path, 'r') as f:
            columns = yaml.load(f, Loader=yaml.FullLoader)

        return columns

    def extract_descriptions(self):
        template = self.raw_path.glob('template*.csv')

        data = pd.read_csv(template.__next__(), sep=self.sep, nrows=self.n_rows)

        for col in self.template_columns:
            column_data = data[col]
            description = ...

            self.template_descriptions[col] = description

        sources = self.raw_path / 'source_tables'

        for file in sources.glob("*.csv"):
            name = file.stem
            self.sources_descriptions[name] = {}

            data = pd.read_csv(file, sep=self.sep, nrows=self.n_rows)

            for col in self.sources_columns[name]:
                column_data = data[col]
                description = ...

                self.sources_descriptions[name][col] = description

    def save(self):
        sources_file = self.extracted_path / 'descriptions' / 'sources_descriptions.yaml'
        template_file = self.extracted_path / 'descriptions' / 'template_columns.yaml'

        with open(sources_file, 'w') as f:
            yaml.dump(self.sources_descriptions, f)

        with open(template_file, 'w') as f:
            yaml.dump(self.template_descriptions, f)



