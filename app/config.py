
import yaml

class config:
    def __init__(self):
        with open("config.yml", 'r') as stream:
            try:
                self.config = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                sys.exit(0)

    def __getattr__(self, attr):
        return self.config[attr]

    def __getitem__(self, attr):
        return self.config[attr]
