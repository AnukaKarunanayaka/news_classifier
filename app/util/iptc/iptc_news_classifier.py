import json
import os
import shutil
import tempfile
from pathlib import Path

import joblib


class IptcNewsClassifier:
    def __init__(self):
        self.model = {}

    def _transform_prediction(self, prediction):
        prediction_set = self.model['mlb'].inverse_transform(prediction)[0]
        transformed_prediction = []
        for e in prediction_set:
            level_number = self.model['levels_mapping'][e]
            if level_number == 2:
                top_level = self.model['named_inversed_second_mapping'][e]
                transformed_label = f'{top_level} > {e}'

                output = {
                    'class': transformed_label,
                    'iptc_subject_code': self.model['named_label_to_iptc_code'][e]
                }
            else:
                output = {
                    'class': e,
                    'iptc_subject_code': self.model['named_label_to_iptc_code'][e]
                }
            transformed_prediction.append(output)
        return transformed_prediction

    def classify_article(self, text, language='en'):
        if language != 'en':
            raise ValueError(f'{language} is not currently supported!')
        prediction = self.model['model'].predict([text])
        prediction = self._transform_prediction(prediction)
        return prediction

    def load(self, path):

        path = Path(path).absolute()
        file_name = path.name

        with tempfile.TemporaryDirectory() as tmp_dir_path:
            tmp_zip_path = Path(tmp_dir_path) / (file_name + '.zip')
            tmp_zip_path = tmp_zip_path.absolute()
            shutil.copyfile(path, tmp_zip_path)
            shutil.unpack_archive(tmp_zip_path, extract_dir=tmp_dir_path)

            tmp_model_dir_path = Path(tmp_dir_path)

            model_file_name = 'model.pkl'
            model_file_path = os.path.join(tmp_model_dir_path, model_file_name)
            self.model['model'] = joblib.load(model_file_path)
            mlb_file_name = 'mlb.pkl'
            mlb_file_path = os.path.join(tmp_model_dir_path, mlb_file_name)
            self.model['mlb'] = joblib.load(mlb_file_path)

            with open(os.path.join(tmp_model_dir_path, 'named_inversed_second_mapping.json'), 'r') as file:
                self.model['named_inversed_second_mapping'] = json.load(file)

            with open(os.path.join(tmp_model_dir_path, 'label_to_code_mapping.json'), 'r') as file:
                self.model['named_label_to_iptc_code'] = json.load(file)

            with open(os.path.join(tmp_model_dir_path, 'levels_mapping.json')) as file:
                self.model['levels_mapping'] = json.load(file)

        return self
