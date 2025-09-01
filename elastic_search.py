from elasticsearch import Elasticsearch


class Elastic:

    def __init__(self, host: str, index: str, mappings: dict):
        self.host = f"http://{host}:9200"
        self.index = index
        self.mappings = mappings
        try:
            self.es = Elasticsearch(self.host)
        except Exception as e:
            raise f"Error during the trial to connect to {self.host}: {e}"
        self._create_index()


    def _create_index(self):
        if isinstance(self.es, Elasticsearch):
            try:
                if not self.es.indices.exists(index=self.index):
                    self.es.indices.create(index=self.index, mappings=self.mappings)
            except Exception as e:
                print(f"Error during the trial to create index in {self.host}: {e}")


    def is_connected(self):
        connected = self.es.ping()
        print(f"connected to {self.host}: {connected}")
        return connected


    def post_document(self, id, document):
        if isinstance(self.es, Elasticsearch):
            try:
                self.es.index(index=self.index, id=id, body=document)
            except Exception as e:
                print(f"Error during the trial to add document to {self.index}: {e}")



    def get_all_documents(self):
        if isinstance(self.es, Elasticsearch):
            try:
                query = {"match_all": {}}
                results =self.es.search(index=self.index, query= query)
            except Exception as e:
                print(f"Error during the trial to get documents from {self.index}: {e}")
                results = None

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
    elastic = Elastic(host, index, mappings)
    connect = elastic.is_connected()
    if connect:
        # document_one = {"text": "first document", "keyword": "123456-789"}
        # id = 1
        # elastic.post_document(id, document_one)
        results = elastic.get_all_documents()
        print(results)