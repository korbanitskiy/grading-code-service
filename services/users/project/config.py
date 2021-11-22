class BaseConfig:
    pass


class DevelopmentConfig(BaseConfig):
    TESTING = False


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    TESTING = False
