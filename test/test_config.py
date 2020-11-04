
from app import load_app
from config import MixinConfig, StageConfig, TestingConfig


def test_development_config():
    """Development config."""
    assert load_app(config_object=StageConfig).config.get('DEBUG')
    assert load_app(config_object=StageConfig).config.get('ENV') == 'development'
    assert not load_app(config_object=StageConfig).config.get('TESTING')


def test_production_config():
    """Production config."""
    assert load_app(config_object=MixinConfig).config.get('ENV') == 'production'
    assert not load_app(config_object=MixinConfig).config.get('DEBUG')
    assert not load_app(config_object=MixinConfig).config.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    assert not load_app(config_object=MixinConfig).config.get('TESTING')


def test_testing_config():
    """Testing config."""
    assert load_app(config_object=TestingConfig).config.get('ENV') == 'testing'
    assert load_app(config_object=TestingConfig).config.get('TESTING')
    assert not load_app(config_object=TestingConfig).config.get('DEBUG')
