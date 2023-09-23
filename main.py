from pathlib import Path

from src.config_loader import ConfigLoader
from src.data_loader import DataLoader
from src.model import OpenAIModel


TEMPLATE = Path(ConfigLoader.get('paths', 'raw_data')) / 'template.csv'
TEMPLATE_DESC = Path(ConfigLoader.get('paths', 'descriptions')) / 'template.yaml'

if __name__ == "__main__":
    # data, filename = DataLoader.read_csv(TEMPLATE)
    template_data = DataLoader.read_yaml(TEMPLATE_DESC)
    source_dir = Path(ConfigLoader.get('paths', 'raw_data')) / "source_tables"

    model = OpenAIModel()

    example_data = DataLoader.read_csv(source_dir / 'table_A.csv')

    model.get_response("similar_columns", example_data, template_descriptions=template_data)

    # for filepath in source_dir.iterdir():
    #     source_data = DataLoader.read_csv(filepath)
    #
    #     model.get_response('similar_columns', source_data, template_descriptions=template_data)


