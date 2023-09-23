import os


class Config:
    """Parent configuration class."""

    API_DOCS_URL = "/doc/"
    SQLALCHEMY_POOL_RECYCLE = 3600
    SQLALCHEMY_POOL_SIZE = 40
    SQLALCHEMY_MAX_OVERFLOW = 0
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""

    HOST = "localhost"
    USER = "postgres"
    PASSWORD = "pass"
    PORT = 3306
    DB = "test"

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("TEST_DATABASE_URL")
        or f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
    )


class LocalConfig(Config):
    """Configurations for Testing, with a separate test database."""

    TESTING = True
    DEBUG = True
    HOST = "localhost"
    USER = "postgres"
    PASSWORD = "password"
    PORT = 5432
    DB = "postgres"

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("LOCAL_DATABASE_URL")
        or f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
    )


class DevelopmentConfig(Config):
    """Configurations for Development."""

    DEBUG = True
    HOST = "database-1.cxfrkunk9j5y.ap-northeast-2.rds.amazonaws.com"
    USER = "postgres"
    PASSWORD = "password"
    PORT = 5432
    DB = "postgres"

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("PRODUCTION_DATABASE_URL")
        or f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
    )


class StagingConfig(Config):
    """Configurations for Staging."""

    DEBUG = True
    HOST = ""
    USER = "postgres"
    PASSWORD = "pass"
    PORT = 5432
    DB = "postgres"

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("STAGING_DATABASE_URL")
        or f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
    )


class EducationConfig(Config):
    """Configurations for Education."""

    # Setting this variable to false disables the docs on education
    API_DOCS_URL = False

    HOST = ""
    USER = "postgres"
    PASSWORD = "pass"
    PORT = 5432
    DB = "postgres"

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("STAGING_DATABASE_URL")
        or f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
    )


class ProductionConfig(Config):
    """Configurations for Production."""

    # Setting this variable to false disables the docs on education
    API_DOCS_URL = False

    HOST = "database-1.cxfrkunk9j5y.ap-northeast-2.rds.amazonaws.com"
    USER = "postgres"
    PASSWORD = "password"
    PORT = 5432
    DB = "postgres"

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("PRODUCTION_DATABASE_URL")
        or f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
    )


db_config = {
    "test": TestingConfig,
    "local": LocalConfig,
    "dev": DevelopmentConfig,
    "stg": StagingConfig,
    "edu": EducationConfig,
    "prod": ProductionConfig,
}
