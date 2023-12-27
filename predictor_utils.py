from typing import List
from zip_utils import unzip_to_directory
from tempfile import mkdtemp
from model_types import ModelGroup, ModelType

import pickle
import shutil
import pandas as pd

def load_predictor(model_type: ModelType, model_data: bytes):
    if model_type.group == ModelGroup.GLUON:
        return TempGluonPredictor(model_type.model_class, model_data) 
    elif model_type.group == ModelGroup.SKLEARN:
        return TempSKPredictor(model_data)
    else:
        raise ValueError(f'There is no loader for {model_type}')

class TempSKPredictor:
    def __init__(self, model_pickle: bytes):
        self.predictor = pickle.loads(model_pickle)

    def predict(self, data: pd.DataFrame) -> List[float]:
        return self.predictor.predict(data)

    def features(self) -> List[str]:
        return list(self.predictor.feature_names_in_)

# due to implementation details of autogluon is it needed for the tmpdir to keep existing.
# only when the predictor goes out of scope it can (and should) be deleted.
class TempGluonPredictor:
    def __init__(self, model, model_zip):
        self.tmpdir = mkdtemp()
        unzip_to_directory(model_zip, self.tmpdir)
        self.predictor = model.load(self.tmpdir)

    def predict(self, data) -> List[float]:
        return self.predictor.predict(data)

    def features(self) -> List[str]:
        return self.predictor.features()

    def __del__(self):
        shutil.rmtree(self.tmpdir)

