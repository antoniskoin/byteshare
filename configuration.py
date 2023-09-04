import configparser


def load_config() -> dict:
    config = configparser.ConfigParser()
    config.read("configuration.cfg")
    username = config.get("DATABASE", "USERNAME")
    password = config.get("DATABASE", "PASSWORD")
    database = config.get("DATABASE", "DATABASE")
    storage_collection = config.get("DATABASE", "STORAGE_COLLECTION")
    account_collection = config.get("DATABASE", "ACCOUNT_COLLECTION")
    config = {"username": username, "password": password, "database": database,
              "storage_collection": storage_collection,
              "account_collection": account_collection}
    return config
