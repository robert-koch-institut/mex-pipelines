from mex.seq_repo.extract import extract_sources


def test_extract_sources() -> None:
    sources = list(extract_sources())
    expected = {
        "project_coordinators": ["max", "mustermann", "yee-haw"],
        "customer_org_unit_id": "FG99",
        "sequencing_date": "2023-08-07",
        "lims_sample_id": "test-sample-id",
        "sequencing_platform": "TEST",
        "species": "Severe acute respiratory syndrome coronavirus 2",
        "project_name": "FG99-ABC-123",
        "customer_sample_name": "test-customer-name-1",
        "project_id": "TEST-ID",
    }
    assert sources[0].model_dump() == expected
