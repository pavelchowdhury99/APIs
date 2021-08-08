import pytest

def test_validate_yaml():
    with pytest.raises(FileNotFoundError):
        read_yaml(file_path="source/data/non_existing_file.yaml")

    with pytest.raises(yaml.scanner.ScannerError):
        # only show the first error
        read_yaml(file_path="source/data/sample_invalid.yaml")

    with pytest.raises(yaml.parser.ParserError):
        # only show the first error
        read_yaml(file_path="source/data/sample_invalid.yaml")
