import os
import shutil
import tempfile
from pathlib import Path
import numpy as np

import joblib


class NewsClassifier:
    def __init__(self):
        self.model = {}

    def transform_preprocessing(self, prediction):
        preprocessed_data = self.model['transformer'].transform(prediction)
        return preprocessed_data

    def classify_article(self, data, category_count):
        if isinstance(data, str):
            data = [data]  # Convert single string to list

        preprocessed_data = self.transform_preprocessing(data)

        # get probabilities instead of predicted labels, since we want to collect top 3
        probs = self.model['model'].predict_proba(preprocessed_data)

        # GET TOP K PREDICTIONS BY PROB - note these are just index
        best_n = np.argsort(probs, axis=1)[:, -category_count:]

        # GET CATEGORY OF PREDICTIONS
        predictions = [[self.model['model'].classes_[predicted_cat]
                        for predicted_cat in prediction] for prediction in best_n]

        predictions = [item[::-1] for item in predictions]

        return predictions

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

            transformer_file_name = 'transformer.pkl'
            transformer_file_path = os.path.join(tmp_model_dir_path, transformer_file_name)
            self.model['transformer'] = joblib.load(transformer_file_path)

        return self
