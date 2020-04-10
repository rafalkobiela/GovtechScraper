import yaml


class TikaConfig:

    def __init__(self):

        with open("resources/tika_config.yaml", 'r') as stream:
            try:
                data = yaml.safe_load(stream)["tika"]
            except yaml.YAMLError as exc:
                print(exc)

        self.url = data["url"]
