from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigReader(BaseSettings):
    """
    ConfigReader class to read the configuration from the .env file and validate the data types of the configuration

    Attributes:
        model_config: SettingsConfigDict: Configuration for the settings
        ROOT_PATH: str: Root path of the project
        TM_SECRET: str: MVS API key
        NOSQL_URL: str: NoSQL URL
        NOSQL_DB: str: NoSQL database
        NOSQL_USER: str: NoSQL user
        NOSQL_PWD: str: NoSQL password
    """
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    ROOT_PATH: str = ''
    TM_SECRET: str

    NOSQL_URL: str
    NOSQL_PORT: int
    NOSQL_DB: str
    NOSQL_USER: str
    NOSQL_PWD: str

    AUTH_TOKEN_EXPIRY: int


config = ConfigReader()
