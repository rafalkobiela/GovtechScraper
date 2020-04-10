import yaml


class GovTechFTPConfig:

    def __init__(self):

        with open("resources/govtech_fpt_config.yaml", 'r') as stream:
            try:
                data = yaml.safe_load(stream)["ftp"]
            except yaml.YAMLError as exc:
                print(exc)

        self.host = data["host"]
        self.username = data["username"]
        self.password = data["password"]