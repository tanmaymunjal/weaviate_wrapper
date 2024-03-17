from pydantic import BaseModel
import os
import weaviate
from typing import ClassVar

class WeaviateModel(BaseModel):
    WEAVIATE_URL_ENV_VARIABLE: ClassVar[str] = "Weaviate_URL"
    WEAVIATE_API_KEY_ENV_VARIABLE: ClassVar[str] = "Weaviate_API_KEY"
    WEAVIATE_OPENAI_CREDS: ClassVar[str] = "X-OpenAI-Api"
    weaviate_url: ClassVar[str] = os.getenv(WEAVIATE_URL_ENV_VARIABLE)
    weaviate_api_key: ClassVar[str] = os.getenv(WEAVIATE_API_KEY_ENV_VARIABLE)
    if weaviate_url is None:
        raise Exception(
            f"Setup environment variable {WEAVIATE_URL_ENV_VARIABLE} to use weaviate wrapper."
        )
    if weaviate_api_key is None:
        raise Exception(
            f"Setup environment variable {WEAVIATE_API_KEY_ENV_VARIABLE} to use weaviate wrapper."
        )
    client: ClassVar = weaviate.Client(
        url=weaviate_url,
        auth_client_secret=weaviate.auth.AuthApiKey(weaviate_api_key),
        # headers={"X-OpenAI-Api": os.getenv(WEAVIATE_OPENAI_CREDS)},
    )

    @classmethod
    def _convert_to_weaviate_json(cls):
        """
        Generate Weaviate class definition from Pydantic model.

        Returns:
            Dict[str, Any]: Weaviate class definition.
        """
        # Initialize the Weaviate class definition
        weaviate_class_definition = {
            "class": cls.__name__,
            "description": f"{cls.__name__} class description",
            "properties": [],
            "vectorizer": None,
        }

        # Iterate over the fields of the Pydantic model
        for field_name, field_info in cls.model_fields.items():
            data_type = "text"  # Default data type
            if field_name=="vectorizer":
                weaviate_class_definition["vectorizer"] = field_info.default
                continue
            # Additional mappings can be added here for specific types if needed
            if field_info.annotation == int:
                data_type = "int"
            elif field_info.annotation == str:
                data_type = "text"
            elif field_info.annotation == float:
                data_type = "number"
            elif field_info.annotation == bool:
                data_type = "boolean"
            elif issubclass(field_info.type_, List):
                inner_type = field_info.sub_fields[0].type_
                data_type = inner_type.__name__.lower()

            # Add property to Weaviate class definition
            property_definition = {
                "dataType": [data_type],
                "description": f"Description of {field_name}",
                "name": field_name
            }
            weaviate_class_definition["properties"].append(property_definition)

        return weaviate_class_definition

    @classmethod
    def register_class(cls):
        weaviate_creation_json = cls._convert_to_weaviate_json()
        if not cls.client.schema.exists(cls.__name__):
            cls.client.schema.create_class(weaviate_creation_json)
    
    def save(self):
        pass

