# TODO: Add tests to git workflow
from pathlib import Path

from src.ingestion.extraction import extract_data


class TestExtractionClass:
    def test_extraction_folder_path_not_exists(self, capsys):
        """Test function if folder path does not exist."""
        input_folder = 'test/not_existing_folder'
        files = extract_data(input_folder)

        assert files is None

        captured = capsys.readouterr()
        input_folder_path = Path(input_folder)
        expected_message = f'Error: The directory {input_folder_path} does not exist.'

        assert expected_message in captured.out


    def test_extraction_no_files_in_folder(self, tmp_path, capsys):
        """Test function if no csv files in folder."""
        # Create empty folder
        empty_folder = tmp_path / 'empty_folder'
        empty_folder.mkdir()

        files = extract_data(str(empty_folder))
        assert files == []

        captured = capsys.readouterr()
        expected_message = 'Found 0 CSV files in the directory.'
        assert expected_message in captured.out


    def test_extraction(self, tmp_path, capsys):
        """Test function if everything is as expected."""
        # Create temp folder and test files
        temp_folder = tmp_path / 'temp_folder'
        temp_folder.mkdir()

        file_1 = temp_folder / 'file1.csv'
        file_1.touch()
        file_2 = temp_folder / 'file2.csv'
        file_2.touch()
        file_3 = temp_folder / 'file3.csv'
        file_3.touch()

        non_csv_file = temp_folder / 'file3.txt'
        non_csv_file.touch()

        files = extract_data(str(temp_folder))
        assert len(files) == 3
        assert file_1 in files
        assert file_2 in files
        assert file_3 in files

        captured = capsys.readouterr()
        expected_message = 'Found 3 CSV files in the directory.'
        assert expected_message in captured.out
