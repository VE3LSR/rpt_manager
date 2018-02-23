
import yaml

class config:
    def __init__(self):
        with open("config.yml", 'r') as stream:
            try:
                self.config = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                sys.exit(0)

        # TODO: Take config and build cross references
        # Cross Reference NodeID to different controllers and repeaters
        # Might be worth asking plugins todo this?

    def __getattr__(self, attr):
        return self.config[attr]

    def __getitem__(self, attr):
        return self.config[attr]
