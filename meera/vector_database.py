# Import the Pinecone library
from pinecone import Pinecone
from meera.types import Vector
from meera.meera_exceptions import (EmbeddingsException,
                                    VectorInsertException,
                                    EmbeddingsQueryException
                                    )

# Initialize a Pinecone client with your API key
pc = Pinecone(api_key="pcsk_378Mq6_TsnU4CkMbMbVCfxoYhZnuhF1RMcyTWV6rkwH1uHBVnbkt1atvcYKjtCRtpvULKB")

# Create a dense index with integrated embedding

class MeeraDB:
    def __init__(self,
                 index_name:str="dense-index",
                 namespace:str="example-namespace"):
        self.index_name = index_name
        self.create_index()
        self.namespace = namespace

    def namespace_exists(self):
        namespaces = self.index_name.describe_index_stats()['namespaces']
        return self.namespace in namespaces

    def create_index(self):
        if not pc.has_index(self.index_name):
            pc.create_index_for_model(
                name=self.index_name,
                cloud="aws",
                region="us-east-1",
                embed={
                    "model": "llama-text-embed-v2",
                    "field_map": {"text": "chunk_text"}
                }
            )

    def emmbed_data(self, data:list[Vector]):
        """

        :param data:
        :return:
            returns a list of vector embeddings.
            @returns list[Vector]

        """
        try:
            embeddings = pc.inference.embed(
                model="multilingual-e5-large",
                inputs=[d["text"] for d in data],
                parameters={
                    "input_type": "passage",
                    "truncate": "END"
                }
            )
            return embeddings.embeddings_list
        except:
            raise EmbeddingsException

    def upsert_embeddings(self, data:list[Vector]):
        """
        :param data:
        :param namespace = userid:[documentType]:[documentName]:
        eg yelpoea@gmail.com:pdf:document5
            yelpoea@gmail.com:link:video3
        :return:
        """
        try:
            dense_index = pc.Index(name=self.index_name)
            print("response", "", 'type=>', type(data), "namespace", self.namespace)

            ## Error Starts from here
            response = dense_index.upsert_records(namespace=self.namespace, records=data)
            return response
        except Exception as e:
            print(e)
            raise VectorInsertException(e)

    def query_embeddings(self, query:str, limit:int=10) ->str:
        """
        This takes a query embed the query, search the database.
        Return a string list of the topk vectors.
        :param query:
        :return:
        """
        try:
            dense_index = pc.Index(self.index_name)
            results = dense_index.search(
                namespace=self.namespace,
                query={
                    "top_k": limit,
                    "inputs": {
                        'text': query
                    }

                },

                rerank={
                    "model": "bge-reranker-v2-m3",
                    "top_n": 10,
                    "rank_fields": ["chunk_text"]
                }
            )
            result_array = results.get("result").get("hits")

            return  "\n".join([chunk.get("fields").get("chunk_text") for chunk in result_array])
        except:
            raise EmbeddingsQueryException


if __name__ == "__main__":
    import uuid
    import uuid

    transcript_chunks = [
        {"id": str(uuid.uuid4()), "source_name": "YouTube Video",
         "chunk_text": "Welcome back to the channel. Today, we're talking about the fundamentals of deep learning."},
        {"id": str(uuid.uuid4()), "source_name": "YouTube Video",
         "chunk_text": "Deep learning is a subset of machine learning that focuses on neural networks with many layers."},
        {"id": str(uuid.uuid4()), "source_name": "YouTube Video",
         "chunk_text": "One key component of deep learning is backpropagation, which helps the network adjust its weights."},
        {"id": str(uuid.uuid4()), "source_name": "YouTube Video",
         "chunk_text": "Training deep learning models requires large datasets and significant computational power."},
        {"id": str(uuid.uuid4()), "source_name": "YouTube Video",
         "chunk_text": "Overfitting can be a problem, so techniques like dropout and regularization are often used."},
        {"id": str(uuid.uuid4()), "source_name": "YouTube Video",
         "chunk_text": "If you found this video helpful, don't forget to like and subscribe for more AI content!"}
    ]

    # Print to verify
    for chunk in transcript_chunks:
        print(chunk)

    pine = MeeraDB(namespace="example-namespace")
    # vectors = pine.emmbed_data(transcript_chunks)
    my_query = "what is deep learning ?"

    # res = pine.upsert_embeddings(transcript_chunks)
    if True:
        print(pine.query_embeddings(my_query, limit=5))