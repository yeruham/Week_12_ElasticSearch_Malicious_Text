from elastic.elastic_search import Elastic
from file_handling.loader import Loader
import config
from processor.sentiment import Sentiment


def load_data_from_csv():
    documents = Loader.load_csv_to_dict(config.TWEETS_PATH)
    return documents[:10]



class Process_manager:


    def __init__(self):
        self.es = Elastic(config.HOST)
        self.index = config.INDEX_NAME
        self.es.create_index(config.INDEX_NAME, config.MAPPINGS)


    def post_data_to_elastic(self, documents):
        self.es.post_documents(self.index, documents)


    def get_documents_from_elastic(self):
        documents = self.es.get_all_documents(self.index)
        return documents


    def update_documents_with_sentiment(self, documents, id_key, update_key):
        for document in documents:
            id = document[id_key]
            update_info = {update_key: document[update_key]}
            self.es.update_document(config.INDEX_NAME, id, update_info)


    @staticmethod
    def sentiments_by_id(documents):
        sentiments_by_id = []
        sentiment = {}
        for document in documents:
            text = document['text']
            sentiment["sentiment"] = Sentiment.find_sentiment(text)
            sentiment["_id"] = document["_id"]
            sentiments_by_id.append(sentiment.copy())
        print(sentiments_by_id)
        return sentiments_by_id


    def run_process(self):
        print(f"start to load data from csv and post him to elastic {config.HOST} - {config.INDEX_NAME}")
        initial_documents = load_data_from_csv()
        self.post_data_to_elastic(documents=initial_documents)

        print(f"get initial_documents from elastic and start to analysis him")
        documents = self.es.get_all_documents(config.INDEX_NAME)
        sentiments = Process_manager.sentiments_by_id(documents)

        print(f"analysis end. start to send update-documents to elastic")
        self.update_documents_with_sentiment(sentiments, "_id", "sentiment")

        print(f"second pull from elastic - documents with sentiment")
        documents = self.es.get_all_documents(config.INDEX_NAME)
        return documents













