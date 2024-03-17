from weaviate_model import WeaviateModel
from connection import Connection


class ListWeaviateModel(list):
    client = Connection().get_client()

    def insert_many(self):
        weaviate_models = []
        class_name = None
        for item in self.__iter__():
            if class_name is None:
                class_name = item.__class__.__name__
            else:
                if class_name!=item.__class__.__name__:
                    raise Exception("Can only batch insert elements from a single collection")
            weaviate_model_dict = vars(item)
            del weaviate_model_dict["vectorizer"]
            weaviate_models.append(weaviate_model_dict)
        with collection.batch.dynamic() as batch:
            for data_row in weaviate_models:
                batch.add_object(
                    properties=data_row
                )


