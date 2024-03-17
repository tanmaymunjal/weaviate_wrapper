from weaviate_model import WeaviateModel
from list_weaviate_model import ListWeaviateModel

class User(WeaviateModel):
    identification: int
    name: str = "Jane Doe"
    vectorizer: str = "text2vec-openai"


User.register_class()
user = User(identification=1)
users = ListWeaviateModel([user])
users.insert_many()
