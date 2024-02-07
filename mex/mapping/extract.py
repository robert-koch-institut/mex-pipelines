import yaml
from pydantic import BaseModel

from mex.common.models.mapping import MAPPING_MODEL_BY_EXTRACTED_CLASS_NAME
from mex.common.types import AssetsPath


def extract_mapping_model(path: AssetsPath, model_type: type[BaseModel]) -> BaseModel:
    """Return a mapping model with default values.

    Args:
        path: path to mapping json
        model_type: model type of BaseModel to be extracted

    Returns:
        BaseModel with default values
    """
    model = MAPPING_MODEL_BY_EXTRACTED_CLASS_NAME[model_type.__name__]
    with open(path, "r", encoding="utf-8") as f:
        yaml_model = yaml.safe_load(f)
    return model.model_validate(yaml_model)
