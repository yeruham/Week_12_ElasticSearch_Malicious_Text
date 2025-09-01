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


    def post_documents(self, index, documents):
        if isinstance(self.es, Elasticsearch):
            for document in documents:
                try:
                    self.es.index(index=index, body=document, refresh=True)
                except Exception as e:
                    print(f"Error during the trial to add document {document} to {index}: {e}")



    def get_all_documents(self, index):
        if isinstance(self.es, Elasticsearch):
            query = {"query": {"match_all": {}}}
            data = self.get_documents(index, query)
            return data



    def get_documents(self, index, query):
        data = []
        if isinstance(self.es, Elasticsearch):
            try:
                query = {"size": 100}
                query.update(query)
                scroll_time = "1m"
                response = self.es.search(index=index, scroll=scroll_time, body=query)
                scroll_id = response["_scroll_id"]
                hits = response["hits"]["hits"]
                print(f"num total value: {response["hits"]["total"]["value"]}")

                while hits:
                    for doc in hits:
                        info = doc["_source"]
                        info.update({"_id": doc["_id"]})
                        data.append(info)

                    response = self.es.scroll(scroll_id=scroll_id, scroll=scroll_time)
                    scroll_id = response["_scroll_id"]
                    hits = response["hits"]["hits"]


            except Exception as e:
                print(f"Error during the trial to get documents from {index}: {e}")

        return data


    def update_document(self, index,  id, new_info: dict):
        if isinstance(self.es, Elasticsearch):
            try:
                body = {"doc": new_info}
                self.es.update(index=index, id=id, body=body, refresh=True)
            except Exception as e:
                print(f"Error during the trial to update document in {index}: {e}")



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
        results = elastic.get_all_documents("malicious_text_test")
        print(results)