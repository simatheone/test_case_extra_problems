class Config:
    DBNAME = 'postgres'
    USER = 'postgres'
    PASSWORD = 'postgres'
    HOST = 'localhost'
    PORT = '5432'
    TEST_FILE = '1gb_file.txt'
    NAME_OF_FILE = 0
    TYPE_OF_FILE = 1
    NUMBER_OF_CHUNKS = 5
    RETURN_FILE_FROM_DB = False

    @property
    def database_uri(self):
        return (
            f'postgresql://{self.USER}:{self.PASSWORD}'
            f'@{self.HOST}:{self.PORT}/{self.DBNAME}'
        )


settings = Config()
