from typing import Any

from mex.common.models import MAPPING_MODEL_BY_EXTRACTED_CLASS_NAME, AnyExtractedModel
from mex.extractors.mapping.types import AnyMappingModel


def transform_mapping_data_to_model(
    raw_data: dict[str, Any], extracted_model: type[AnyExtractedModel]
) -> AnyMappingModel:
    """Transform raw mapping data to a mapping model with default values.

    Args:
        raw_data: raw mapping data
        extracted_model: extracted model corresponding to the mapping

    Returns:
        mapping model with default value data
    """
    model = MAPPING_MODEL_BY_EXTRACTED_CLASS_NAME[extracted_model.__name__]
    return model.model_validate(raw_data)


def transform_mapping_data_to_models(
    raw_data: list[dict[str, Any]], extracted_model: type[AnyExtractedModel]
) -> list[AnyMappingModel]:
    """Transform a list of raw mapping data to mapping models with default values.

    Args:
        raw_data: list of raw mapping data
        extracted_model: extracted model corresponding to the mapping

    Returns:
        list of mapping models with default value data
    """
    return [transform_mapping_data_to_model(r, extracted_model) for r in raw_data]
