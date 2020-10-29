
if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

from config import TestingConfig
from util.mixin import route

app = route(config_object=TestingConfig, name=__name__)
