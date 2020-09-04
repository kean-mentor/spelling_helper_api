import os


basedir = os.path.abspath(os.path.dirname(__file__))


class ApiConfig:
    DEBUG = os.environ.get('FLASK_DEBUG') or False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///spelling_api.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False


class WebConfig:
    DEBUG = os.environ.get('FLASK_DEBUG') or False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'


spelling_api_host = os.environ.get('SPELLING_API_HOST', 'localhost')
spelling_api_port = os.environ.get('SPELLING_API_PORT', '5000')
spelling_api_address = "".join(['http://', spelling_api_host, ":", spelling_api_port])
