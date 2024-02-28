from pathlib import Path

from slam.data_manager.factory.data_reader_ABC import DataReader


def test_is_file_valid():
    tmp_dir = Path("/tmp")

    # Test with non-existent file
    non_existent_file = tmp_dir / "non_existent_file.txt"
    assert not DataReader.is_file_valid(non_existent_file)

    # Test with empty file
    empty_file = tmp_dir / "empty_file.txt"
    empty_file.touch()
    assert not DataReader.is_file_valid(empty_file)

    # Test with non-empty file
    non_empty_file = tmp_dir / "non_empty_file.txt"
    non_empty_file.write_text("Some data")
    assert DataReader.is_file_valid(non_empty_file)
