import os
from utils import generate_headers
import weaviate


class Connection:
    _instance = None
    WEAVIATE_URL_ENV_VARIABLE: str = "Weaviate_URL"
    WEAVIATE_API_KEY_ENV_VARIABLE: str = "Weaviate_API_KEY"

    def __new__(cls, *args, **kwargs):
        """
        Create a new instance of Connection if it does not exist.

        Returns:
            Connection: The instance of Connection.
        """
        if cls._instance is None:
            print("Creating Connection singleton object")
            cls._instance = super(Connection, cls).__new__(cls)
        return cls._instance

    def __init__(self, environment=os.environ):
        weaviate_url: str = environment.get(self.WEAVIATE_URL_ENV_VARIABLE)
        weaviate_api_key: str = environment.get(self.WEAVIATE_API_KEY_ENV_VARIABLE)
        if weaviate_url is None:
            raise Exception(
                f"Setup environment variable {self.WEAVIATE_URL_ENV_VARIABLE} to use weaviate wrapper."
            )
        if weaviate_api_key is None:
            raise Exception(
                f"Setup environment variable {self.WEAVIATE_API_KEY_ENV_VARIABLE} to use weaviate wrapper."
            )
        client = weaviate.Client(
            url=weaviate_url,
            auth_client_secret=weaviate.auth.AuthApiKey(weaviate_api_key),
            additional_headers=generate_headers(environment),
        )
        self.__client = client

    def get_client(self):
        return self.__client
    