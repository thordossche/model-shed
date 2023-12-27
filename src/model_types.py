from enum import Enum
from autogluon.tabular import TabularPredictor

class ModelGroup(Enum):
    GLUON = "gluon"
    SKLEARN = "sklearn"

class ModelType(Enum):
    TABULAR_PREDICTOR = {
        "model_name": "TabularPredictor",
        "group": ModelGroup.GLUON,
        "model_class": TabularPredictor
    }
    MLP_REGRESSOR = {
        "model_name": "MLPRegressor",
        "group": ModelGroup.SKLEARN,
    }

    def __init__(self, details):
        self.model_name = details["model_name"]
        self.group = details["group"]
        self.model_class = details.get("model_class")

    @classmethod
    def from_name(cls, model_name):
        for member in cls:
            if member.model_name == model_name:
                return member
        raise ValueError(f"No ModelType with model_name '{model_name}' found.")

