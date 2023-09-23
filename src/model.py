import openai
import pandas as pd
import time
from pathlib import Path
from tqdm.notebook import tqdm

from src.config_loader import ConfigLoader
from src.data_loader import DataLoader


class OpenAIModel:
    def __init__(self):
        openai.api_key = ConfigLoader.get("openai", "api_key")

    def get_response(self, task: str, data: pd.DataFrame, template_descriptions: dict | None = None):
        if task == 'description':
            descriptions = self._get_descriptions(data)
            DataLoader.save(Path(ConfigLoader.get('paths', 'descriptions')) / 'template.yaml', descriptions)
        elif task == 'similar_columns':
            columns_mapping = self._get_similar_columns(data, template_descriptions)
            DataLoader.save(Path(ConfigLoader.get('paths', 'descriptions')) / 'mapping.yaml', columns_mapping)
        else:
            raise "Unknown task"

    def _get_single_response(self, message):
        response = openai.ChatCompletion.create(model=ConfigLoader.get("openai", "model"),
                                                temperature=ConfigLoader.get("openai", "temperature"),
                                                max_tokens=ConfigLoader.get("openai", "max_tokens"),
                                                messages=[
                                                    {"role": "user", "content": message}
                                                ]
                                                )
        return response["choices"][0]["message"]["content"]

    def _get_descriptions(self, data: pd.DataFrame):
        columns = data.columns
        descriptions = {}

        for col in tqdm(columns):
            message = ConfigLoader.get("messages", "descriptions") + "\n" + col + "\n" + "\n".join(data[col].apply(str))
            descriptions[col] = self._get_single_response(message)

            time.sleep(ConfigLoader.get('openai', 'time_sleep'))

        return descriptions

    def _get_similar_columns(self, source_data: pd.DataFrame, template_data: dict):
        descriptions = self._get_descriptions(source_data)
        mapping = {}

        for col in tqdm(template_data.keys()):
            single_desc = template_data[col]
            message = ConfigLoader.get("messages", "similar_columns") + "\n" \
                      + single_desc + "\n" + "Словарь:" + str(descriptions)

            mapping[col] = self._get_single_response(message)

            time.sleep(ConfigLoader.get('openai', 'time_sleep'))

        return mapping
