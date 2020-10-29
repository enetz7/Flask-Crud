
if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

from config import MixinConfig
from util.mixin import route

app = route(config_object=MixinConfig, name=__name__)
