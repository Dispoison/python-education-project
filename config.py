class Config:
    DEBUG = False
    SECRET_KEY = 'gk8V4MspZKC6jg8w0MGyjvF5b9BnUEwq'
    RESTX_MASK_SWAGGER = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True

    DB_USER = 'postgres'
    DB_PASSWORD = 'postgres_password'
    DB_HOST = 'localhost'
    DB_PORT = '5432'
    DB_NAME = 'movie_library'

    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
