from weaviate_model import WeaviateModel

class User(WeaviateModel):
    identification: int
    name: str = "Jane Doe"
    vectorizer: str = "text2vec-openai"

User.register_class()
