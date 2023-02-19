import os

import psycopg2

from config import settings


def connect_to_db():
    """
    Create a connection to database.

    If there are no errors, prints information about the
    server and returns the connection object. If there
    are some prints error message.
    """
    conn = None
    try:
        conn = psycopg2.connect(
            dsn=settings.database_uri
        )
        print('Информация о сервере PostgreSQL:\n')
        print(conn.get_dsn_parameters())
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print('ОШИБКА. Невозможно подключиться к Базе данных. \n')
        print(error)


def create_table(conn):
    """
    Creates a new table in database if not exists.

    Table fields:
    - `file_id`: an id of the file in table;
    - `file_name`: the name of file;
    - `file_type`: the extension of file;
    - `file_chunk_1`: the first chunk of file's data;
    - `file_chunk_2`: the second chunk of file's data;
    - `file_chunk_3`: the third chunk of file's data;
    - `file_chunk_4`: the fourth chunk of file's data;
    - `file_chunk_5`: the fifth chunk of file's data.
    """
    with conn.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS large_file (
                file_id int GENERATED ALWAYS AS IDENTITY NOT NULL,
                file_name varchar(128) NOT NULL,
                file_type varchar(16) NOT NULL,
                file_chunk_1 bytea,
                file_chunk_2 bytea,
                file_chunk_3 bytea,
                file_chunk_4 bytea,
                file_chunk_5 bytea,

                CONSTRAINT pk_large_file_file_id PRIMARY KEY(file_id));
            """
        )
        conn.commit()


def get_file_size(filename):
    """Return information about file size in bytes."""
    return os.path.getsize(filename)


def read_file_and_split_into_chunks(filename):
    """
    Read file and split into chunks and
    save in list with type `psycopg2.Binary()`.

    The number of chunks sets in variable `NUMBER_OF_CHUNKS`.

    `NUMBER_OF_CHUNKS - 1` will store equal amount of data.
    The last chunk will store the rest file's data.
    """
    file_size = get_file_size(filename)
    with open(filename, 'rb') as file:
        chunk_size = file_size // settings.NUMBER_OF_CHUNKS
        all_chunks_data = []
        file_data = file.read()

        for number in range(settings.NUMBER_OF_CHUNKS):
            start_point = number * chunk_size
            end_point = start_point + chunk_size

            if number == settings.NUMBER_OF_CHUNKS - 1:
                end_point = file_size
            chunk_data = psycopg2.Binary(file_data[start_point:end_point])
            all_chunks_data.append(chunk_data)
        return all_chunks_data


def insert_data_into_table(conn, file_name, file_type, all_chunks_data):
    """Insert file name and data to the table."""
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO large_file (
                file_name, file_type, file_chunk_1, file_chunk_2
            )
            VALUES (%s, %s, %s, %s);
            """,
            (file_name, file_type, *all_chunks_data[:2]),
        )
        conn.commit()

        cursor.execute(
            """
            UPDATE large_file
            SET file_chunk_3 = %s, file_chunk_4 = %s
            WHERE file_id = 1;
            """,
            (*all_chunks_data[2:4],),
        )
        conn.commit()

        cursor.execute(
            """
            UPDATE large_file
            SET file_chunk_5 = %s
            WHERE file_id = 1;
            """,
            (all_chunks_data[4],),
        )
        conn.commit()
    all_chunks_data.clear()


def get_data_from_db(conn):
    """
    Retrieve data from the database.

    Chunks with data fetches sequentially and saves in variable `chunks`.
    """
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT file_name,
                   file_type,
                   file_chunk_1,
                   file_chunk_2
            FROM large_file
            WHERE file_id = 1;
            """
        )
        fetched_data_1 = cursor.fetchone()
        file_name, file_type, *chunks = fetched_data_1

        cursor.execute(
            """
            SELECT file_chunk_3,
                   file_chunk_4
            FROM large_file
            WHERE file_id = 1;
            """
        )
        fetched_data_2 = cursor.fetchone()
        chunks.extend(fetched_data_2)

        cursor.execute(
            """
            SELECT file_chunk_5
            FROM large_file
            WHERE file_id = 1;
            """
        )
        fetched_data_3 = cursor.fetchone()
        chunks.extend(fetched_data_3)
        return file_name, file_type, chunks


def write_in_file_retrieved_data_from_db(file_name, file_type, chunks):
    """
    Create file from information retrieved from database.

    The name of the file consist of:
        - `file_name` - retrieved file name from database;
        - `_from_db.` - additional tag for the file name;
        - `file_type` - retrieved file type from database.
    """
    retrieved_file_name = file_name + '_from_db.' + file_type
    file_data = bytes()
    for chunk in chunks:
        file_data += chunk

    with open(retrieved_file_name, 'wb') as file:
        file.write(file_data)
    chunks.clear()


if __name__ == '__main__':
    if not os.path.exists(settings.TEST_FILE):
        print(
            'Запустите скрипт по созданию 1Гб файла.\n'
            'Либо перенесите свой файл в директорию "problem_4/" '
            'и укажите его название в файле "config.py" -> '
            '"TEST_FILE = ..."'
        )
        exit()
    conn = connect_to_db()
    if conn is not None:
        splitted_file_name = settings.TEST_FILE.split('.')
        file_name = ''.join(splitted_file_name[settings.NAME_OF_FILE])
        file_type = ''.join(splitted_file_name[settings.TYPE_OF_FILE])
        with conn:
            create_table(conn)
            all_chunks_data = read_file_and_split_into_chunks(
                settings.TEST_FILE
            )
            insert_data_into_table(conn, file_name, file_type, all_chunks_data)

            if settings.RETURN_FILE_FROM_DB:
                file_name, file_type, chunks = get_data_from_db(conn)
                write_in_file_retrieved_data_from_db(file_name,
                                                     file_type,
                                                     chunks)
        conn.close()
        print('Соединение с Базой данных закрыто.')
