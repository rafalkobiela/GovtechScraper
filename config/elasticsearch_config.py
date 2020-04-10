import yaml


class ElasticSearchConfig:

    def __init__(self):

        with open("resources/elasticsearch_config.yaml", 'r') as stream:
            try:
                data = yaml.safe_load(stream)["es"]
            except yaml.YAMLError as exc:
                print(exc)

        self.url = data["url"]
        self.port = data["port"]
        self.index = data["index"]
