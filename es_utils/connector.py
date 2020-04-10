from typing import Dict

from elasticsearch import Elasticsearch
from config.elasticsearch_config import ElasticSearchConfig


class ElasticConnector:

    connection: Elasticsearch

    def __init__(self) -> None:
        self.config = ElasticSearchConfig()
        self.host = self.config.url
        self.port = self.config.port

    def connect(self):
        self.connection = Elasticsearch([{'host': self.host, 'port': self.port}], timeout=10000)

        if not self.connection.ping():
            raise Exception("Could not connect to Elasticsearch!")

    def add_document(self, doc: Dict[str, str]):
        res = self.connection.index(index=self.config.index, body=doc)
        if res['result'] != 'created':
            print(f"failed to index document for file {doc['path']} - {doc['filename']}")
