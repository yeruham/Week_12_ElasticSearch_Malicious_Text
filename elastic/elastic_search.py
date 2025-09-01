from elasticsearch import Elasticsearch


class Elastic:

    def __init__(self, host: str):
        self.host = f"http://{host}:9200"
        try:
            self.es = Elasticsearch(self.host)
        except Exception as e:
            raise f"Error during the trial to connect to {self.host}: {e}"


    def create_index(self, index, mappings):
        if isinstance(self.es, Elasticsearch):
            try:
                if not self.es.indices.exists(index=index):
                    self.es.indices.create(index=index, mappings=mappings)
            except Exception as e:
                print(f"Error during the trial to create index - {index} in {self.host}: {e}")


    def delete_index(self, index):
        if isinstance(self.es, Elasticsearch):
            try:
                self.es.indices.delete(index=index)
            except Exception as e:
                print(f"Error during the trial to delete index - {index} in {self.host}: {e}")

    def is_connected(self):
        connected = self.es.ping()
        print(f"connected to {self.host}: {connected}")
        return connected


    def post_document(self, index, id, document):
        if isinstance(self.es, Elasticsearch):
            try:
                self.es.index(index=index, id=id, body=document)
            except Exception as e:
                print(f"Error during the trial to add document to {index}: {e}")



    def get_all_documents(self, index):
        if isinstance(self.es, Elasticsearch):
            results = None
            try:
                query = {"match_all": {}}
                results = self.es.search(index=index, query= query)

            except Exception as e:
                print(f"Error during the trial to get documents from {index}: {e}")

            return results


if __name__ == "__main__":
    host = '127.0.0.1'
    index = 'index_test'
    mappings = {"properties":
                {"text":{"type": "text"},
                "number": {"type": "integer"},
                "keyword":{"type": "keyword"}
                 }
            }
    elastic = Elastic(host)
    connect = elastic.is_connected()
    if connect:
        # document_one = {"text": "first document", "keyword": "123456-789"}
        # id = 1
        # elastic.post_document(id, document_one)
        # elastic.delete_index(index)
        # elastic.create_index(index, mappings)
        results = elastic.get_all_documents(index)
        print(results)