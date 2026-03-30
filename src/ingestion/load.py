import csv


def load_data_to_database(file, cur):
    """This function ..."""
    table_name = 'staging_' + file.stem.split('_')[1]
    print(f'Loading data into table: {table_name}')

    try:
        with open(file, encoding='utf-8') as f:
            reader = csv.reader(f)
            csv_columns = next(reader)
            column_str = ', '.join(csv_columns)

        # Delete existing data in table
        cur.execute(f'TRUNCATE TABLE {table_name}')  # TODO: Outsource sql?!

        # Copy data from df to table
        with file.open('r', encoding='utf-8') as f:
            copy_sql = f'COPY {table_name} ({column_str}) FROM STDIN WITH (FORMAT CSV, HEADER True)'

            with cur.copy(copy_sql) as copy:
                while data := f.read(8192):
                    copy.write(data)

        print(f'Successfully loaded data from {file} into {table_name}.')

    except Exception as e:
        print(f'Error loading data from {file} into {table_name}: {e}')
        raise
