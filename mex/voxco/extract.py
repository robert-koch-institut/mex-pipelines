from mex.drop import DropApiConnector
from mex.voxco.model import VoxcoVariable


def extract_voxco_variables() -> dict[str, list[VoxcoVariable]]:
    """Extract voxco variables by loading data from mex-drop source json file.

    Returns:
        lists of voxco variables by json file name
    """
    connector = DropApiConnector.get()
    files = connector.list_files("voxco")
    data = {
        file_name: connector.get_file("voxco", file_name)
        for file_name in files
        if "test_" not in file_name
    }
    return {
        file_name: [VoxcoVariable.model_validate(item) for item in file_rows["value"]]
        for file_name, file_rows in data.items()
    }
