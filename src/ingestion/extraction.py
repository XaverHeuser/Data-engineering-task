from pathlib import Path


def extract_data(folder_path_str: str):
    """This function gets all csv files fron given folder path."""
    print(f'Processing folder: {folder_path_str}')

    # Clean folder path
    clean_path = folder_path_str.strip().strip('"')
    folder_path = Path(clean_path)

    if not folder_path.exists():
        print(f'Error: The directory {folder_path} does not exist.')
        return

    # Iterate through folder path dir and get all csv files
    files = []
    for file in folder_path.iterdir():
        if file.is_file() and file.suffix == '.csv':
            print(file)
            files.append(file)

    print(f'Found {len(files)} CSV files in the directory.')
    return files
