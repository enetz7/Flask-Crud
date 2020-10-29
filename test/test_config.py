from config import MixinConfig;
from config import StageConfig;
from config import TestingConfig;
from util.mixin import route;
def test_testing_env():
    assert route(TestingConfig).config.get("TESTING");