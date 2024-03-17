from pydantic import BaseModel
from connection import Connection
import os
from typing import ClassVar
import weaviate
import warnings


class WeaviateModel(BaseModel):
    client: ClassVar = Connection().get_client()

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
            if field_name == "model_config":
                warnings.warn(
                    """Model config is used to configure model typing inference.
                    Ignore this warning if used to configure typing, else do note
                    that this field will not be pushed to weaviate and consider
                    renaming it.
                    """
                )
                continue
            data_type = "text"  # Default data type
            if field_name == "vectorizer":
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
                "name": field_name,
            }
            weaviate_class_definition["properties"].append(property_definition)

        return weaviate_class_definition

    @classmethod
    def register_class(cls):
        weaviate_creation_json = cls._convert_to_weaviate_json()
        if not cls.client.schema.exists(cls.__name__):
            cls.client.schema.create_class(weaviate_creation_json)

    def save(self):
        weaviate_object = vars(self)
        if "vectorizer" not in weaviate_object:
            raise Exception(
                "Need to set vectorizer field to specify which vectorizer to user"
            )
        del weaviate_object["vectorizer"]
        self.client.data_object.create(
            weaviate_object,
            self.__class__.__name__,
            consistency_level=weaviate.data.replication.ConsistencyLevel.ALL,
        )
