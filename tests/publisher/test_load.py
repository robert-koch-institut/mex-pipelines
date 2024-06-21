from mex.publisher.load import write_merged_items


def test_write_merged_items(ndjson_path) -> None:
    content = [{"Test": 1, "NochNTest": 2}, {"bla": "blub", "foo": "bar"}]
    write_merged_items(ndjson_path, content)
    assert (
        ndjson_path.read_text(encoding="utf-8")
        == '{"Test": 1, "NochNTest": 2}\n{"bla": "blub", "foo": "bar"}\n'
    )
