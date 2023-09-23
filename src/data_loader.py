import pandas as pd
import yaml
from pathlib import Path
from src.config_loader import ConfigLoader


class DataLoader:
    @staticmethod
    def read_csv(path: Path, csv_sep: str = ','):
        if path.suffix == ".csv":
            data = pd.read_csv(path, sep=csv_sep, nrows=ConfigLoader.get("data", "nrows"))
        else:
            raise "Unknown format of file"

        return data

    @staticmethod
    def read_yaml(path:Path):
        with open(path, 'r') as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    @staticmethod
    def save(path: Path, data: dict):
        with open(path, 'w') as f:
            yaml.dump(data, f, allow_unicode=True)
