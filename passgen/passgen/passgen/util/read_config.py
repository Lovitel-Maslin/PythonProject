import yaml
from passgen.core.config import Config


def get_config_from_yaml(path: str) -> Config:
    with open(path, "r") as f:
        raw_config = yaml.safe_load(f.read())
        return Config(bot=raw_config["bot"],
                      integrations=raw_config["integrations"])
